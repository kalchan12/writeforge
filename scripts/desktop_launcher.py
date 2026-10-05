#!/usr/bin/env python3
"""
RightForge Desktop Launcher
===========================
Orchestrates offline, standalone local execution of the RightForge API
and Web Dashboard with automatic browser/webview dispatch and graceful shutdown.
"""

from __future__ import annotations

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path
from typing import Optional


def is_port_in_use(host: str, port: int) -> bool:
    """Check if a TCP port is currently open and bound on the host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def wait_for_service(url: str, timeout: float = 20.0, interval: float = 0.5) -> bool:
    """Poll an HTTP URL until it returns a 200 OK or timeout expires."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RightForgeLauncher/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status in (200, 304):
                    return True
        except Exception:
            pass
        time.sleep(interval)
    return False


class DesktopLauncher:
    """Manages the lifecycle of backend API and frontend web services."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        api_port: int = 8000,
        web_port: int = 3000,
        no_browser: bool = False,
        mode: str = "dev",
        db_path: Optional[str] = None,
        project_root: Optional[Path] = None,
    ) -> None:
        self.host = host
        self.api_port = api_port
        self.web_port = web_port
        self.no_browser = no_browser
        self.mode = mode
        self.db_path = db_path
        self.project_root = project_root or Path(__file__).resolve().parent.parent

        self.api_process: Optional[subprocess.Popen] = None
        self.web_process: Optional[subprocess.Popen] = None
        self._terminated = False

    def build_api_command(self) -> list[str]:
        """Construct command to launch FastAPI backend."""
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "apps.api.main:app",
            "--host",
            self.host,
            "--port",
            str(self.api_port),
        ]
        if self.mode == "dev":
            cmd.append("--reload")
        return cmd

    def build_web_command(self) -> list[str]:
        """Construct command to launch Next.js frontend."""
        script = "dev" if self.mode == "dev" else "start"
        return ["npm", "run", script, "--prefix", str(self.project_root / "apps" / "web")]

    def start_api(self) -> None:
        """Start FastAPI service in subprocess with env configuration."""
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{self.project_root}:{self.project_root / 'engine'}:{self.project_root / 'apps' / 'api'}"
        if self.db_path:
            env["RIGHTFORGE_DB_PATH"] = self.db_path

        cmd = self.build_api_command()
        print(f"[DesktopLauncher] Starting API on http://{self.host}:{self.api_port} ...")
        self.api_process = subprocess.Popen(
            cmd,
            cwd=str(self.project_root),
            env=env,
        )

    def start_web(self) -> None:
        """Start Next.js frontend in subprocess."""
        env = os.environ.copy()
        env["PORT"] = str(self.web_port)
        env["NEXT_PUBLIC_API_URL"] = f"http://{self.host}:{self.api_port}"

        cmd = self.build_web_command()
        print(f"[DesktopLauncher] Starting Web UI on http://{self.host}:{self.web_port} ({self.mode} mode) ...")
        self.web_process = subprocess.Popen(
            cmd,
            cwd=str(self.project_root),
            env=env,
        )

    def launch_browser(self) -> None:
        """Open browser window to RightForge Dashboard."""
        if self.no_browser:
            print("[DesktopLauncher] Browser launch skipped (--no-browser active)")
            return

        url = f"http://{self.host}:{self.web_port}"
        print(f"[DesktopLauncher] Opening {url} in local browser ...")
        webbrowser.open(url)

    def shutdown(self) -> None:
        """Gracefully terminate child processes."""
        if self._terminated:
            return
        self._terminated = True
        print("\n[DesktopLauncher] Shutting down RightForge services...")

        for name, proc in [("API", self.api_process), ("Web UI", self.web_process)]:
            if proc and proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=3.0)
                    print(f"[DesktopLauncher] Stopped {name}.")
                except subprocess.TimeoutExpired:
                    proc.kill()
                    print(f"[DesktopLauncher] Force killed {name}.")
                except Exception as e:
                    print(f"[DesktopLauncher] Error stopping {name}: {e}")

        print("[DesktopLauncher] All services terminated.")

    def run(self) -> int:
        """Run the complete launcher lifecycle with signal trapping."""
        def handle_signal(sig, frame):
            self.shutdown()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        # Check port collisions
        if is_port_in_use(self.host, self.api_port):
            print(f"[DesktopLauncher] Warning: Port {self.api_port} is already bound.")
        if is_port_in_use(self.host, self.web_port):
            print(f"[DesktopLauncher] Warning: Port {self.web_port} is already bound.")

        try:
            self.start_api()
            self.start_web()

            # Wait for API readiness
            api_health_url = f"http://{self.host}:{self.api_port}/health"
            api_ready = wait_for_service(api_health_url, timeout=15.0)
            if api_ready:
                print("[DesktopLauncher] API Service is healthy and responsive.")
            else:
                print("[DesktopLauncher] Note: API did not respond to health check within timeout.")

            # Wait for Web readiness and launch browser
            web_url = f"http://{self.host}:{self.web_port}"
            web_ready = wait_for_service(web_url, timeout=20.0)
            if web_ready:
                print("[DesktopLauncher] Web UI is accessible.")
            self.launch_browser()

            print("==========================================================")
            print(f" RightForge Desktop is active:")
            print(f"   - Web Dashboard: http://{self.host}:{self.web_port}")
            print(f"   - API Service:   http://{self.host}:{self.api_port}")
            print(" Press Ctrl+C to stop services and exit.")
            print("==========================================================")

            # Block until child processes exit or signal received
            while True:
                time.sleep(1.0)
                if self.api_process and self.api_process.poll() is not None:
                    print("[DesktopLauncher] API process terminated unexpectedly.")
                    break
                if self.web_process and self.web_process.poll() is not None:
                    print("[DesktopLauncher] Web UI process terminated unexpectedly.")
                    break

        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

        return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RightForge Standalone Desktop Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    parser.add_argument("--api-port", type=int, default=8000, help="Port for FastAPI backend")
    parser.add_argument("--web-port", type=int, default=3000, help="Port for Next.js frontend")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open web browser")
    parser.add_argument("--mode", choices=["dev", "standalone"], default="dev", help="Execution mode")
    parser.add_argument("--db-path", default=None, help="Custom SQLite database path")

    args = parser.parse_args()

    launcher = DesktopLauncher(
        host=args.host,
        api_port=args.api_port,
        web_port=args.web_port,
        no_browser=args.no_browser,
        mode=args.mode,
        db_path=args.db_path,
    )
    sys.exit(launcher.run())


if __name__ == "__main__":
    main()
