"""Prompt generation and template formatting for style-conditioned revision."""

from rightforge.models.revision import RevisionPlan


class RevisionPromptBuilder:
    """Constructs disciplined prompts transforming RevisionPlan diagnostics into strict LLM instructions."""

    def build_system_prompt(self, target_author: str | None = None) -> str:
        """Create system prompt establishing deterministic behavioral constraints."""
        author_instruction = (
            f" Align the stylistic voice and syntactic cadence with author '{target_author}'."
            if target_author
            else ""
        )
        return (
            "You are RightForge's Controlled Stylistic Revision Engine."
            f"{author_instruction}\n"
            "Your objective is to revise user text strictly adhering to designated stylometric, "
            "cadence, and grammatical goals.\n\n"
            "MANDATORY OPERATING RULES:\n"
            "1. Preserve all factual claims, core ideas, arguments, and meaning of the original text.\n"
            "2. Never alter technical terminology or distort intended semantic nuances.\n"
            "3. Output ONLY the revised text. Do NOT include conversational filler, greetings, explanations, "
            "or meta-commentary (such as 'Here is the revised text:' or 'I hope this helps!').\n"
            "4. Strictly satisfy the sentence-level interventions and global metric goals provided below."
        )

    def build_user_prompt(self, text: str, plan: RevisionPlan) -> str:
        """Construct user prompt combining source text, global metric goals, and sentence targets."""
        sections: list[str] = []

        # 1. Global Goals Section
        if plan.goals:
            goals_text = ["### GLOBAL STYLISTIC DIRECTIVES:"]
            for g in plan.goals:
                goals_text.append(
                    f"- Metric: {g.metric_name} | Goal: {g.direction.upper()} to ~{g.target_value} "
                    f"(Current: {g.current_value}) | Priority: {g.severity.upper()}\n"
                    f"  Guidance: {g.description}"
                )
            sections.append("\n".join(goals_text))

        # 2. Granular Sentence Targets Section
        if plan.sentence_targets:
            targets_text = ["### SENTENCE-LEVEL INTERVENTIONS:"]
            for t in plan.sentence_targets:
                targets_text.append(
                    f"- Sentence {t.sentence_index + 1} [{t.issue_type.replace('_', ' ').title()}]:\n"
                    f"  Original: \"{t.original_text}\"\n"
                    f"  Prescription: {t.suggestion}"
                )
            sections.append("\n".join(targets_text))

        # 3. Source Text
        sections.append(
            "### SOURCE TEXT TO REVISE:\n"
            "```text\n"
            f"{text.strip()}\n"
            "```\n\n"
            "Return ONLY the complete revised text below:"
        )

        return "\n\n".join(sections)
