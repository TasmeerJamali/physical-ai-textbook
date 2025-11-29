"""
Reusable Intelligence Module

This module implements the Spec-Kit Plus Reusable Intelligence pattern:
- Skills: Reusable prompt patterns following P+Q+P (Persona + Questions + Principles)
- Subagents: Specialized agents that orchestrate skills for specific tasks

Skills and Subagents are loaded from .specify/ folder and implemented as callable classes.
"""

from .skills import (
    RoboticsExplainerSkill,
    ContentPersonalizerSkill,
    CodeTranslatorSkill,
)

from .subagents import (
    QAAgent,
    PersonalizationAgent,
    TranslationAgent,
)

__all__ = [
    # Skills
    "RoboticsExplainerSkill",
    "ContentPersonalizerSkill", 
    "CodeTranslatorSkill",
    # Subagents
    "QAAgent",
    "PersonalizationAgent",
    "TranslationAgent",
]

