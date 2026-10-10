"""Antigravity CLI provider for Gemini inference."""

import os
import shutil
import subprocess
from rightforge.llm.base import BaseLLMProvider


class AntigravityCLIProvider(BaseLLMProvider):
    """Executes prompt completions using the Antigravity CLI ('agy') with Gemini models."""

    def __init__(
        self,
        model: str = "gemini-3.8-flash-low",
        cli_path: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.model = model
        self.timeout = timeout
        self.cli_path = (
            cli_path
            or os.environ.get("AGY_PATH")
            or shutil.which("agy")
            or os.path.expanduser("~/.local/bin/agy")
        )

    def is_available(self) -> bool:
        """Verify that the agy binary exists and is executable."""
        if not self.cli_path:
            return False
        return os.path.isfile(self.cli_path) and os.access(self.cli_path, os.X_OK)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Call 'agy -p' non-interactively to generate revised prose with Gemini."""
        if not self.is_available():
            raise RuntimeError(f"Antigravity CLI ('agy') binary not found at '{self.cli_path}'.")

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt.strip()}\n\n{prompt.strip()}"

        cmd = [
            self.cli_path,
            "-p",
            full_prompt,
            "--model",
            self.model,
            "--disable-slash-commands",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"Antigravity CLI execution timed out after {self.timeout}s.") from exc

        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"Antigravity CLI failed (exit {result.returncode}): {err_msg}")

        output = result.stdout.strip()
        # Strip code fences if LLM wrapped markdown
        if output.startswith("```") and output.endswith("```"):
            lines = output.splitlines()
            if len(lines) >= 3:
                output = "\n".join(lines[1:-1]).strip()

        return output
