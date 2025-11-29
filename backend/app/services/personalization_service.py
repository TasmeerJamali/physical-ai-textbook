"""Personalization service for adapting content to user level.

Uses Reusable Intelligence:
- PersonalizationAgent subagent for orchestration
- ContentPersonalizerSkill for level-appropriate adaptations
"""
import google.generativeai as genai

from app.config import get_settings
from app.intelligence.skills import SkillContext, ContentPersonalizerSkill
from app.intelligence.subagents import PersonalizationAgent


class PersonalizationService:
    """Service for personalizing textbook content based on user background.

    Integrates with Reusable Intelligence for enhanced personalization.
    """

    def __init__(self):
        self.settings = get_settings()
        # Use Gemini for personalization (frees up OpenAI quota for RAG)
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Initialize Reusable Intelligence
        self.personalizer_skill = ContentPersonalizerSkill()
    
    async def adapt_content(
        self,
        content: str,
        user_level: str = "intermediate",
        user_background: dict | None = None
    ) -> dict:
        """
        Adapt content based on user's experience level and background.

        Uses Reusable Intelligence:
        - PersonalizationAgent for orchestration
        - ContentPersonalizerSkill for P+Q+P pattern

        For beginners: Add more analogies, simplify jargon
        For advanced: Add optimization tips, edge cases
        """
        adaptations = []

        # Create skill context from user background
        skill_context = SkillContext(
            user_level=user_level,
            programming_languages=user_background.get("programming_languages", []) if user_background else [],
            robotics_experience=user_background.get("robotics_experience", False) if user_background else False,
            learning_goals=user_background.get("learning_goals", []) if user_background else []
        )

        # Use PersonalizationAgent subagent
        personalization_agent = PersonalizationAgent(context=skill_context)

        # Build personalization context
        background_context = ""
        if user_background:
            if user_background.get("programming_languages"):
                langs = ", ".join(user_background["programming_languages"])
                background_context += f"User knows: {langs}. "
                adaptations.append(f"Referenced {langs} concepts")

            if user_background.get("robotics_experience"):
                background_context += "User has robotics experience. "
                adaptations.append("Assumed robotics familiarity")

            if user_background.get("learning_goals"):
                goals = ", ".join(user_background["learning_goals"])
                background_context += f"Learning goals: {goals}. "
                adaptations.append(f"Focused on {goals}")

        # Get enhanced prompt from subagent (uses skill internally)
        enhanced_prompt = personalization_agent.process(content)

        # Add background context
        full_prompt = f"""{background_context}

{enhanced_prompt}"""

        # Use Gemini for content adaptation
        response = self.model.generate_content(full_prompt)

        adaptations.append(f"Adapted for {user_level} level")
        adaptations.append("Used content-personalizer skill")
        adaptations.append("Used personalization-agent subagent")

        return {
            "content": response.text,
            "adaptations": adaptations,
            "skill_used": "content-personalizer",
            "subagent_used": "personalization-agent"
        }

