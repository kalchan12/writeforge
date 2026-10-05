"""Abstract base class and test mock implementation for local LLM providers."""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract interface for local inference engines."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a completion for the provided prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check whether the underlying inference service is operational and reachable."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """Deterministic mock provider for offline pipelines and automated unit testing."""

    def __init__(
        self,
        canned_response: str | None = None,
        available: bool = True,
        fail_with_error: str | None = None,
    ) -> None:
        self.canned_response = canned_response
        self.available = available
        self.fail_with_error = fail_with_error
        self.last_prompt: str | None = None
        self.last_system_prompt: str | None = None
        self.call_count: int = 0

    def is_available(self) -> bool:
        return self.available

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        self.call_count += 1
        self.last_prompt = prompt
        self.last_system_prompt = system_prompt

        if self.fail_with_error is not None:
            raise RuntimeError(self.fail_with_error)

        if self.canned_response is not None:
            return self.canned_response

        # Default fallback response
        return "The analytical engine weaves patterns. Mathematical truths require discipline."
