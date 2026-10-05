"""Unit tests for the Desktop Launcher utility."""

from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.desktop_launcher import DesktopLauncher, is_port_in_use, wait_for_service


def test_is_port_in_use_unbound():
    """Unbound random high port should return False."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        free_port = s.getsockname()[1]
    # Once closed, port is unbound
    assert is_port_in_use("127.0.0.1", free_port) is False


def test_is_port_in_use_bound():
    """Actively listening socket should return True."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        bound_port = s.getsockname()[1]
        assert is_port_in_use("127.0.0.1", bound_port) is True


def test_launcher_command_generation():
    """Verify generated commands for dev and standalone modes."""
    launcher = DesktopLauncher(host="127.0.0.1", api_port=8080, web_port=3030, mode="dev")
    api_cmd = launcher.build_api_command()
    assert sys.executable in api_cmd
    assert "--port" in api_cmd
    assert "8080" in api_cmd
    assert "--reload" in api_cmd

    web_cmd = launcher.build_web_command()
    assert web_cmd == ["npm", "run", "dev", "--prefix", str(launcher.project_root / "apps" / "web")]

    launcher_prod = DesktopLauncher(mode="standalone")
    assert "--reload" not in launcher_prod.build_api_command()
    assert launcher_prod.build_web_command() == ["npm", "run", "start", "--prefix", str(launcher.project_root / "apps" / "web")]


def test_launcher_shutdown_process_handling():
    """Test graceful and forced termination during shutdown."""
    launcher = DesktopLauncher()
    mock_api = MagicMock(spec=subprocess.Popen)
    mock_api.poll.return_value = None
    mock_web = MagicMock(spec=subprocess.Popen)
    mock_web.poll.return_value = None

    launcher.api_process = mock_api
    launcher.web_process = mock_web

    launcher.shutdown()

    mock_api.terminate.assert_called_once()
    mock_web.terminate.assert_called_once()
    assert launcher._terminated is True

    # Calling shutdown again is idempotent
    launcher.shutdown()
    assert mock_api.terminate.call_count == 1


def test_launcher_shutdown_timeout_fallback():
    """Test timeout fallback to force kill during shutdown."""
    launcher = DesktopLauncher()
    mock_api = MagicMock(spec=subprocess.Popen)
    mock_api.poll.return_value = None
    mock_api.wait.side_effect = subprocess.TimeoutExpired(cmd="uvicorn", timeout=3.0)

    launcher.api_process = mock_api
    launcher.shutdown()

    mock_api.terminate.assert_called_once()
    mock_api.kill.assert_called_once()


def test_launcher_browser_launch_flag():
    """Test browser launch obeys --no-browser flag."""
    launcher_no_browser = DesktopLauncher(no_browser=True)
    with patch("webbrowser.open") as mock_open:
        launcher_no_browser.launch_browser()
        mock_open.assert_not_called()

    launcher_browser = DesktopLauncher(no_browser=False, host="127.0.0.1", web_port=3000)
    with patch("webbrowser.open") as mock_open:
        launcher_browser.launch_browser()
        mock_open.assert_called_once_with("http://127.0.0.1:3000")


def test_wait_for_service_timeout():
    """Polling a non-existent URL should return False after timeout."""
    # Use an invalid/unbound port with a short timeout
    result = wait_for_service("http://127.0.0.1:59999/health", timeout=0.2, interval=0.05)
    assert result is False
