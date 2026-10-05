"""Unit tests for local LLM providers and prompt engineering."""

import pytest
from rightforge.llm.base import MockLLMProvider
from rightforge.llm.ollama import OllamaProvider
from rightforge.llm.prompts import RevisionPromptBuilder
from rightforge.models.revision import RevisionGoal, RevisionPlan, SentenceRevisionTarget


def test_mock_llm_provider_behavior():
    """Verify MockLLMProvider returns canned response and tracks calls."""
    canned = "Clean, concise sentences represent clear thought."
    provider = MockLLMProvider(canned_response=canned)

    assert provider.is_available() is True
    assert provider.call_count == 0

    result = provider.generate("Revise this text.", system_prompt="System rules.")
    assert result == canned
    assert provider.call_count == 1
    assert provider.last_prompt == "Revise this text."
    assert provider.last_system_prompt == "System rules."


def test_mock_llm_provider_error_simulation():
    """Verify MockLLMProvider properly simulates provider failure."""
    provider = MockLLMProvider(fail_with_error="Inference server overloaded")
    with pytest.raises(RuntimeError) as exc_info:
        provider.generate("Prompt")

    assert "Inference server overloaded" in str(exc_info.value)


def test_revision_prompt_builder():
    """Verify prompt builder formats goals, sentence targets, and source text."""
    builder = RevisionPromptBuilder()

    system_prompt = builder.build_system_prompt(target_author="Hemingway")
    assert "Hemingway" in system_prompt
    assert "MANDATORY OPERATING RULES" in system_prompt
    assert "Output ONLY the revised text" in system_prompt

    plan = RevisionPlan(
        document_id="doc-123",
        target_author="Hemingway",
        goals=[
            RevisionGoal(
                metric_name="sentence_length_mean",
                description="Reduce average sentence length",
                current_value=25.0,
                target_value=12.0,
                direction="decrease",
                severity="high",
            )
        ],
        sentence_targets=[
            SentenceRevisionTarget(
                sentence_index=0,
                original_text="This is an excessively long and elaborate run-on sentence.",
                issue_type="excessive_length",
                suggestion="Partition into two concise statements.",
                priority=1,
            )
        ],
        total_suggestions=1,
        summary="Revision plan summary.",
    )

    source_text = "This is an excessively long and elaborate run-on sentence."
    user_prompt = builder.build_user_prompt(source_text, plan)

    assert "GLOBAL STYLISTIC DIRECTIVES" in user_prompt
    assert "sentence_length_mean" in user_prompt
    assert "SENTENCE-LEVEL INTERVENTIONS" in user_prompt
    assert "Partition into two concise statements." in user_prompt
    assert "SOURCE TEXT TO REVISE" in user_prompt
    assert source_text in user_prompt


def test_ollama_provider_offline_handling():
    """Verify OllamaProvider handles an unreachable host gracefully without crashing."""
    # Point to a deliberately unreachable port/host
    provider = OllamaProvider(base_url="http://127.0.0.1:59999", timeout=1.0)
    assert provider.is_available() is False

    with pytest.raises(RuntimeError) as exc_info:
        provider.generate("Test prompt")

    assert "Failed to connect to local Ollama daemon" in str(exc_info.value)
