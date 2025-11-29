"""
Reusable Skills implementing P+Q+P Pattern (Persona + Questions + Principles)

Each skill is a class that:
1. Defines a persona (who the AI should act as)
2. Specifies questions to understand context
3. Lists principles to apply when generating responses
"""

from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod


@dataclass
class SkillContext:
    """Context for applying a skill."""
    user_level: str = "intermediate"  # beginner, intermediate, advanced
    programming_languages: list[str] = None
    robotics_experience: bool = False
    learning_goals: list[str] = None
    
    def __post_init__(self):
        if self.programming_languages is None:
            self.programming_languages = []
        if self.learning_goals is None:
            self.learning_goals = []


class BaseSkill(ABC):
    """Base class for all skills."""
    
    name: str = "base-skill"
    version: str = "1.0.0"
    category: str = "general"
    
    @property
    @abstractmethod
    def persona(self) -> str:
        """Define who the AI should act as."""
        pass
    
    @property
    @abstractmethod
    def principles(self) -> list[str]:
        """List of principles to apply."""
        pass
    
    def build_prompt(self, context: SkillContext, task: str) -> str:
        """Build a prompt using the P+Q+P pattern."""
        principles_text = "\n".join(f"- {p}" for p in self.principles)
        
        return f"""## Persona
{self.persona}

## Context
- User Level: {context.user_level}
- Programming Languages: {', '.join(context.programming_languages) or 'Not specified'}
- Robotics Experience: {'Yes' if context.robotics_experience else 'No'}
- Learning Goals: {', '.join(context.learning_goals) or 'General learning'}

## Principles to Apply
{principles_text}

## Task
{task}
"""


class RoboticsExplainerSkill(BaseSkill):
    """Skill for explaining robotics concepts at appropriate levels."""
    
    name = "robotics-explainer"
    version = "1.0.0"
    category = "education"
    
    @property
    def persona(self) -> str:
        return """You are an expert robotics instructor with 15+ years of experience 
teaching ROS 2, simulation, and AI-powered robotics. You excel at explaining 
complex concepts in simple terms using real-world analogies."""
    
    @property
    def principles(self) -> list[str]:
        return [
            "Adapt explanations to user's level (beginner: analogies, advanced: optimization tips)",
            "Use real-world analogies: nodes=workers, topics=bulletin boards, services=phone calls",
            "Always include runnable code examples with comments",
            "Connect concepts to actual robots (TurtleBot, Spot, etc.)",
            "Reference official documentation for accuracy",
        ]
    
    def get_level_adaptation(self, level: str) -> str:
        """Get specific adaptations for each level."""
        adaptations = {
            "beginner": "Use simple analogies, avoid jargon, provide step-by-step explanations",
            "intermediate": "Balance theory and practice, include common pitfalls",
            "advanced": "Focus on optimization, edge cases, and performance considerations",
        }
        return adaptations.get(level, adaptations["intermediate"])


class ContentPersonalizerSkill(BaseSkill):
    """Skill for personalizing content based on user background."""
    
    name = "content-personalizer"
    version = "1.0.0"
    category = "personalization"
    
    @property
    def persona(self) -> str:
        return """You are an adaptive learning specialist who customizes educational 
content based on learner profiles. You understand cognitive load theory and can 
adjust complexity, examples, and pacing to match individual needs."""
    
    @property
    def principles(self) -> list[str]:
        return [
            "For beginners: Add 'Why This Matters' sections, include more analogies",
            "For intermediate: Add 'Pro Tips', mention common pitfalls",
            "For advanced: Remove basic explanations, add performance considerations",
            "Preserve all code blocks exactly as-is",
            "Match examples to user's known programming languages",
        ]


class CodeTranslatorSkill(BaseSkill):
    """Skill for translating code between languages and frameworks."""
    
    name = "code-translator"
    version = "1.0.0"
    category = "development"
    
    @property
    def persona(self) -> str:
        return """You are a polyglot developer expert in ROS 2 development across 
Python and C++. You can translate code between languages while maintaining 
idiomatic patterns and best practices."""
    
    @property
    def principles(self) -> list[str]:
        return [
            "Preserve functionality exactly when translating",
            "Use idiomatic patterns for the target language",
            "Add comments explaining language-specific differences",
            "Handle memory management differences (Python GC vs C++ RAII)",
            "Maintain ROS 2 API consistency across languages",
        ]

