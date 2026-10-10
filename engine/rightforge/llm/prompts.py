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
            "You are WriteForge's State-of-the-Art Humanizing and Stylistic Rewriting Engine."
            f"{author_instruction}\n"
            "Your objective is to thoroughly humanize text so that it completely eludes AI detectors "
            "(Turnitin, GPTZero, CopyLeaks) by eliminating all structural, lexical, and statistical AI markers.\n\n"
            "MANDATORY OPERATING RULES:\n"
            "1. RADICAL CADENCE BURSTINESS: Strictly alternate between short (3-8 words), medium, and longer descriptive sentences. "
            "Never write consecutive sentences of similar length. Include occasional fragments or direct punchy statements.\n"
            "2. TOTAL BAN ON AI FINGERPRINTS: NEVER use these words or patterns: 'delve', 'tapestry', 'testament', 'multifaceted', "
            "'beacon', 'pivotal', 'paramount', 'leverage', 'foster', 'underscore', 'intricate', 'seamlessly', 'transformative', "
            "'furthermore', 'moreover', 'consequently', 'additionally', 'in conclusion', 'in today's world', 'plays a key role'.\n"
            "3. NATURAL CONVERSATIONAL FLOW: Use genuine human idioms, natural conjunctions ('and', 'but', 'so', 'yet'), "
            "and concrete active verbs rather than stiff nominalizations.\n"
            "4. RETAIN 100% OF MEANING: Rewrite every single concept, claim, and sentence from the original draft. Do not summarize or drop details.\n"
            "5. OUTPUT PURITY: Output ONLY the revised text. Never output quotation marks around the text, explanations, or notes."
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
