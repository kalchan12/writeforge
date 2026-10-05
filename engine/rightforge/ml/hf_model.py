"""HuggingFace transformer wrapper for causal LM perplexity evaluation."""

from typing import Any
from rightforge.ml.probability import BaseProbabilityModel


class HuggingFaceProbabilityModel(BaseProbabilityModel):
    """Transformer-based causal language model scorer utilizing HuggingFace transformers.

    Lazy-loads PyTorch and Transformers to avoid heavyweight overhead or dependency
    failures when only deterministic statistical analysis is required.
    """

    def __init__(self, model_name: str = "gpt2", device: str | None = None) -> None:
        self.model_name = model_name
        self._device = device
        self._model: Any = None
        self._tokenizer: Any = None
        self._torch: Any = None

    def _load_model(self) -> None:
        if self._model is not None:
            return

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as err:
            raise ImportError(
                "HuggingFaceProbabilityModel requires 'torch' and 'transformers' packages. "
                "Install them via 'pip install torch transformers' or use NgramProbabilityModel."
            ) from err

        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_name)

        if self._device:
            self._model.to(self._device)
        elif torch.cuda.is_available():
            self._model.to("cuda")
        self._model.eval()

    def score_tokens(self, tokens: list[str]) -> list[float]:
        """Compute conditional log-probabilities using transformer logits."""
        if not tokens:
            return []

        self._load_model()
        torch = self._torch
        text = " ".join(tokens)
        encodings = self._tokenizer(text, return_tensors="pt")
        input_ids = encodings.input_ids.to(self._model.device)

        if input_ids.shape[1] == 0:
            return []

        with torch.no_grad():
            outputs = self._model(input_ids)
            logits = outputs.logits  # shape: (1, seq_len, vocab_size)

        # Log softmax along vocab dimension
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)

        token_logprobs: list[float] = []
        seq_len = input_ids.shape[1]

        # First token gets unconditioned logprob from position 0
        first_token_id = input_ids[0, 0].item()
        token_logprobs.append(float(log_probs[0, 0, first_token_id].item()))

        for i in range(1, seq_len):
            target_id = input_ids[0, i].item()
            # Probability of token i given context 0..i-1
            logprob = log_probs[0, i - 1, target_id].item()
            token_logprobs.append(float(logprob))

        return token_logprobs
