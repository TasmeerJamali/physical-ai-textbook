"""Personalization service for adapting content to user level."""
import google.generativeai as genai

from app.config import get_settings


class PersonalizationService:
    """Service for personalizing textbook content based on user background."""

    def __init__(self):
        self.settings = get_settings()
        # Use Gemini for personalization (frees up OpenAI quota for RAG)
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def adapt_content(
        self,
        content: str,
        user_level: str = "intermediate",
        user_background: dict | None = None
    ) -> dict:
        """
        Adapt content based on user's experience level and background.
        
        For beginners: Add more analogies, simplify jargon
        For advanced: Add optimization tips, edge cases
        """
        adaptations = []
        
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
        
        # Level-specific instructions
        level_instructions = {
            "beginner": """
Adapt this content for a beginner:
- Replace jargon with simple explanations
- Add real-world analogies
- Break down complex concepts step-by-step
- Add "Why this matters" sections
- Include more code comments""",
            "intermediate": """
Adapt this content for an intermediate learner:
- Keep technical terms but ensure they're explained
- Add practical tips and common pitfalls
- Include "Pro tips" where relevant""",
            "advanced": """
Adapt this content for an advanced user:
- Be more concise, skip basic explanations
- Add performance optimization tips
- Include edge cases and advanced patterns
- Reference related advanced topics"""
        }
        
        system_prompt = f"""You are an expert technical writer adapting robotics content.
{background_context}

{level_instructions.get(user_level, level_instructions['intermediate'])}

Preserve all code blocks exactly. Only adapt the explanatory text.
Return the adapted content in the same markdown format."""

        # Use Gemini for content adaptation
        prompt = f"{system_prompt}\n\nAdapt this content:\n\n{content}"
        response = self.model.generate_content(prompt)

        adaptations.append(f"Adapted for {user_level} level")

        return {
            "content": response.text,
            "adaptations": adaptations
        }

