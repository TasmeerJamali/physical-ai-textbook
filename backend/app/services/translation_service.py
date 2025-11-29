"""Translation service for Urdu and other languages."""
import re
import google.generativeai as genai

from app.config import get_settings


class TranslationService:
    """Service for translating textbook content while preserving code."""

    def __init__(self):
        self.settings = get_settings()
        # Use Gemini for translation (frees up OpenAI quota for RAG)
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def extract_code_blocks(self, content: str) -> tuple[str, list[str]]:
        """Extract code blocks and replace with placeholders."""
        code_blocks = []
        
        def replace_code(match):
            code_blocks.append(match.group(0))
            return f"[[CODE_BLOCK_{len(code_blocks) - 1}]]"
        
        # Match fenced code blocks
        pattern = r'```[\s\S]*?```'
        processed = re.sub(pattern, replace_code, content)
        
        # Match inline code
        inline_pattern = r'`[^`]+`'
        processed = re.sub(inline_pattern, replace_code, processed)
        
        return processed, code_blocks
    
    def restore_code_blocks(self, content: str, code_blocks: list[str]) -> str:
        """Restore code blocks from placeholders."""
        result = content
        for i, block in enumerate(code_blocks):
            result = result.replace(f"[[CODE_BLOCK_{i}]]", block)
        return result
    
    async def translate(
        self,
        content: str,
        target_language: str = "ur",
        preserve_code: bool = True
    ) -> dict:
        """
        Translate content to target language.
        
        Preserves code blocks and technical terms.
        """
        # Extract code blocks if needed
        if preserve_code:
            text_to_translate, code_blocks = self.extract_code_blocks(content)
        else:
            text_to_translate = content
            code_blocks = []
        
        # Language-specific prompts
        language_names = {
            "ur": "Urdu (اردو)",
            "hi": "Hindi (हिंदी)",
            "ar": "Arabic (العربية)"
        }
        
        target_name = language_names.get(target_language, target_language)
        
        system_prompt = f"""You are a professional translator specializing in technical content.
Translate the following robotics textbook content to {target_name}.

Rules:
1. Preserve all placeholders like [[CODE_BLOCK_0]] exactly as they are
2. Keep technical terms in English with translation in parentheses first time
3. Maintain markdown formatting (headers, lists, bold, etc.)
4. Keep a natural, educational tone
5. For Urdu, use proper right-to-left formatting

Translate naturally, not word-by-word."""

        # Use Gemini for translation
        prompt = f"{system_prompt}\n\nTranslate this content:\n\n{text_to_translate}"
        response = self.model.generate_content(prompt)

        translated = response.text
        
        # Restore code blocks
        if preserve_code:
            translated = self.restore_code_blocks(translated, code_blocks)
        
        return {
            "translated": translated,
            "source_language": "en",
            "target_language": target_language
        }

