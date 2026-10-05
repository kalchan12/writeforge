"""Local LLM provider implementation for Ollama HTTP daemon."""

from typing import Any
import httpx

from rightforge.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """Integrates with a locally running Ollama daemon (zero cloud telemetry)."""

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.3,
        timeout: float = 30.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout

    def is_available(self) -> bool:
        """Query the local daemon to verify availability."""
        try:
            with httpx.Client(timeout=2.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except (httpx.RequestError, Exception):
            return False

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Call Ollama /api/generate endpoint with stream=False."""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
            },
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(f"{self.base_url}/api/generate", json=payload)
                if res.status_code != 200:
                    raise RuntimeError(
                        f"Ollama generation failed with HTTP status {res.status_code}: {res.text}"
                    )
                data = res.json()
                return data.get("response", "").strip()
        except httpx.RequestError as err:
            raise RuntimeError(
                f"Failed to connect to local Ollama daemon at {self.base_url}: {err}"
            ) from err
