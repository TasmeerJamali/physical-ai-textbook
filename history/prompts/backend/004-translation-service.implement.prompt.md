# Prompt History Record: Translation Service

**Type**: Implementation Prompt  
**Date**: 2025-11-28  
**Phase**: Implement  
**Status**: ✅ Successful

---

## Context

Implementing Urdu translation service that translates technical content while preserving code blocks and maintaining technical term accuracy.

## Prompt Used

```
Create a TranslationService that:
1. Translates technical content to Urdu
2. Preserves all code blocks in English
3. Keeps technical terms accurate
4. Handles RTL layout considerations
5. Maintains markdown formatting
```

## Implementation Details

### Translation Strategy

1. **Identify code blocks** - Regex to find ```...``` sections
2. **Replace with placeholders** - [CODE_BLOCK_1], [CODE_BLOCK_2]
3. **Translate text** - Send to GPT-4 with Urdu instruction
4. **Restore code blocks** - Replace placeholders back

### Technical Term Handling

Some terms kept in English with Urdu transliteration:
- ROS 2 → ROS 2 (آر او ایس ٹو)
- Node → نوڈ
- Topic → ٹاپک
- Publisher → پبلشر

### Service Implementation

```python
class TranslationService:
    async def translate(
        self, 
        content: str, 
        target_lang: str = "ur"
    ) -> str:
        # Extract code blocks
        code_blocks, text = self._extract_code(content)
        
        # Translate text
        translated = await self._translate_text(text, target_lang)
        
        # Restore code blocks
        final = self._restore_code(translated, code_blocks)
        
        return final
```

### System Prompt for Urdu

```
Translate the following technical content to Urdu.
- Keep code blocks exactly as they are (marked with placeholders)
- Maintain technical accuracy
- Use proper Urdu technical terminology where established
- Keep English terms that have no Urdu equivalent
- Preserve markdown formatting
```

## Outcome

✅ Translation service working:
- Accurate Urdu translation
- Code blocks preserved
- Technical terms handled properly
- Markdown structure maintained

## RTL Considerations

Frontend handles RTL with CSS:
```css
[dir="rtl"] {
  text-align: right;
}
[dir="rtl"] pre, [dir="rtl"] code {
  direction: ltr;
  text-align: left;
}
```

## Reusability

Extend for other languages:
1. Add language code to translate method
2. Update technical term dictionary
3. Adjust system prompt for target language

