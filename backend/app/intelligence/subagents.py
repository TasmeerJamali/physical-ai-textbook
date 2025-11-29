"""
Subagents - Specialized agents that orchestrate skills for specific tasks.

Each subagent:
1. Has a specific purpose (Q&A, personalization, translation)
2. Uses one or more skills
3. Can hand off to other subagents when needed
"""

from typing import Optional
from abc import ABC, abstractmethod
from .skills import (
    BaseSkill,
    SkillContext,
    RoboticsExplainerSkill,
    ContentPersonalizerSkill,
    CodeTranslatorSkill,
)


class BaseSubagent(ABC):
    """Base class for all subagents."""
    
    name: str = "base-subagent"
    version: str = "1.0.0"
    skills: list[BaseSkill] = []
    
    def __init__(self, context: Optional[SkillContext] = None):
        self.context = context or SkillContext()
        self._initialize_skills()
    
    def _initialize_skills(self):
        """Initialize skill instances."""
        pass
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Define the subagent's system prompt."""
        pass
    
    @abstractmethod
    def process(self, input_text: str) -> str:
        """Process input and return enhanced prompt."""
        pass


class QAAgent(BaseSubagent):
    """Q&A Agent for answering questions about the textbook."""
    
    name = "qa-agent"
    version = "1.0.0"
    
    def _initialize_skills(self):
        self.explainer = RoboticsExplainerSkill()
    
    @property
    def system_prompt(self) -> str:
        return """You are the Q&A Agent for the Physical AI & Humanoid Robotics textbook.

Your role:
1. Answer questions about ROS 2, Gazebo, NVIDIA Isaac, and VLA models
2. Use the textbook content as your primary source
3. Adapt explanations to the user's level
4. Cite sources when possible

When answering:
- For beginners: Use analogies (nodes=workers, topics=bulletin boards)
- For intermediate: Balance theory and practice
- For advanced: Focus on optimization and edge cases

Always be helpful, accurate, and encouraging."""
    
    def process(self, question: str) -> str:
        """Build enhanced prompt for Q&A."""
        skill_prompt = self.explainer.build_prompt(self.context, question)
        
        return f"""{self.system_prompt}

{skill_prompt}

Please answer the question using the context provided. If the context doesn't contain 
the answer, say so and provide general guidance based on your knowledge."""


class PersonalizationAgent(BaseSubagent):
    """Agent for personalizing content based on user profile."""
    
    name = "personalization-agent"
    version = "1.0.0"
    
    def _initialize_skills(self):
        self.personalizer = ContentPersonalizerSkill()
    
    @property
    def system_prompt(self) -> str:
        return """You are the Personalization Agent for the Physical AI textbook.

Your role:
1. Adapt content complexity to match user's experience level
2. Add relevant examples based on user's programming background
3. Include "Why This Matters" sections for beginners
4. Add "Pro Tips" for intermediate users
5. Focus on optimization for advanced users

IMPORTANT: Preserve all code blocks exactly as they appear."""
    
    def process(self, content: str) -> str:
        """Build enhanced prompt for personalization."""
        skill_prompt = self.personalizer.build_prompt(self.context, content)
        
        level_instructions = {
            "beginner": """
Add these sections:
- 🎯 Why This Matters: Explain real-world relevance
- 💡 Simple Analogy: Use everyday comparisons
- ⚠️ Common Confusion: Address typical misunderstandings""",
            "intermediate": """
Add these sections:
- 💡 Pro Tip: Share practical insights
- ⚠️ Common Pitfall: Warn about typical mistakes
- 🔗 Related Concepts: Connect to other topics""",
            "advanced": """
Add these sections:
- ⚡ Performance Note: Optimization considerations
- 🔧 Edge Cases: Handle unusual scenarios
- 📊 Benchmarks: When relevant, mention performance data"""
        }
        
        return f"""{self.system_prompt}

{skill_prompt}

{level_instructions.get(self.context.user_level, level_instructions["intermediate"])}

Personalize the following content:
{content}"""


class TranslationAgent(BaseSubagent):
    """Agent for translating content to Urdu."""
    
    name = "translation-agent"
    version = "1.0.0"
    
    def _initialize_skills(self):
        self.translator = CodeTranslatorSkill()
    
    @property
    def system_prompt(self) -> str:
        return """You are the Translation Agent for the Physical AI textbook.

Your role:
1. Translate English content to Urdu
2. Preserve all technical terms in English (ROS 2, Gazebo, etc.)
3. Keep all code blocks unchanged
4. Maintain the original formatting and structure
5. Use formal Urdu suitable for educational content

Translation guidelines:
- Technical terms: Keep in English with Urdu transliteration if helpful
- Code: Never translate code or commands
- Headers: Translate but keep structure
- Examples: Translate explanations, keep code"""
    
    def process(self, content: str) -> str:
        """Build enhanced prompt for translation."""
        return f"""{self.system_prompt}

Translate the following content to Urdu:

{content}

Remember:
- Keep all code blocks exactly as they are
- Keep technical terms like ROS 2, Gazebo, Isaac Sim in English
- Use formal educational Urdu"""

