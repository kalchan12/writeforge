"""Revision execution engine orchestrating LLM generation and post-revision verification."""

from rightforge.analysis.basic import BasicTextAnalyzer
from rightforge.analysis.lexical import LexicalAnalyzer
from rightforge.llm.base import BaseLLMProvider, MockLLMProvider
from rightforge.llm.prompts import RevisionPromptBuilder
from rightforge.models.document import Document
from rightforge.models.execution import RevisionExecutionResult
from rightforge.models.profile import AuthorProfile
from rightforge.models.revision import RevisionPlan
from rightforge.profiles.comparator import ProfileComparator
from rightforge.revision.planner import RevisionPlanner


class RevisionExecutor:
    """Executes style-conditioned revisions via local LLM and verifies metric shifts."""

    def __init__(
        self,
        provider: BaseLLMProvider | None = None,
        planner: RevisionPlanner | None = None,
        prompt_builder: RevisionPromptBuilder | None = None,
        comparator: ProfileComparator | None = None,
    ) -> None:
        self.provider = provider if provider is not None else MockLLMProvider()
        self.planner = planner if planner is not None else RevisionPlanner()
        self.prompt_builder = prompt_builder if prompt_builder is not None else RevisionPromptBuilder()
        self.comparator = comparator if comparator is not None else ProfileComparator()
        self.basic_analyzer = BasicTextAnalyzer()
        self.lexical_analyzer = LexicalAnalyzer()

    def execute(
        self,
        target: Document | str,
        profile: AuthorProfile | None = None,
        plan: RevisionPlan | None = None,
        outlier_threshold: float = 2.0,
    ) -> RevisionExecutionResult:
        """Run controlled revision and assess empirical consistency shifts."""
        text = target.text if isinstance(target, Document) else target
        doc_id = target.id if isinstance(target, Document) else None

        if not text or not text.strip():
            empty_plan = (
                plan
                if plan is not None
                else self.planner.generate_plan(target="", profile=profile)
            )
            return RevisionExecutionResult(
                document_id=doc_id,
                original_text=text,
                revised_text="",
                plan=empty_plan,
                success=False,
                error_message="Document text is empty; cannot execute revision.",
            )

        # 1. Ensure revision plan is available
        active_plan = (
            plan
            if plan is not None
            else self.planner.generate_plan(
                target=target, profile=profile, outlier_threshold=outlier_threshold
            )
        )

        # 2. Extract baseline metrics and consistency prior to revision
        metrics_before = self._extract_snapshot_metrics(text)
        consistency_before: float | None = None
        if profile is not None:
            pre_report = self.comparator.compare(
                profile=profile, target=text, outlier_threshold=outlier_threshold
            )
            consistency_before = pre_report.consistency_score

        # 3. Formulate prompts
        target_author = profile.author_name if profile else None
        system_prompt = self.prompt_builder.build_system_prompt(target_author=target_author)
        user_prompt = self.prompt_builder.build_user_prompt(text=text, plan=active_plan)

        # 4. Invoke LLM generation
        try:
            revised_text = self.provider.generate(
                prompt=user_prompt, system_prompt=system_prompt
            ).strip()
        except Exception as err:
            return RevisionExecutionResult(
                document_id=doc_id,
                original_text=text,
                revised_text="",
                plan=active_plan,
                consistency_before=consistency_before,
                consistency_after=None,
                metrics_before=metrics_before,
                metrics_after={},
                success=False,
                error_message=f"LLM generation failed: {err}",
            )

        # 5. Extract metrics and consistency post-revision
        metrics_after = self._extract_snapshot_metrics(revised_text)
        consistency_after: float | None = None
        if profile is not None and revised_text:
            post_report = self.comparator.compare(
                profile=profile, target=revised_text, outlier_threshold=outlier_threshold
            )
            consistency_after = post_report.consistency_score

        return RevisionExecutionResult(
            document_id=doc_id,
            original_text=text,
            revised_text=revised_text,
            plan=active_plan,
            consistency_before=consistency_before,
            consistency_after=consistency_after,
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            success=True,
            error_message=None,
        )

    def _extract_snapshot_metrics(self, text: str) -> dict[str, float]:
        """Collect fundamental surface and linguistic metric values for before/after comparison."""
        if not text.strip():
            return {}

        basic = self.basic_analyzer.analyze(text)
        lexical = self.lexical_analyzer.analyze(text)

        metrics: dict[str, float] = {}
        for m in basic.metrics.values():
            if m.name in ("word_count", "sentence_count", "avg_words_per_sentence"):
                metrics[m.name] = m.value

        for m in lexical:
            if m.name in ("type_token_ratio", "long_word_ratio"):
                metrics[m.name] = m.value

        return metrics
