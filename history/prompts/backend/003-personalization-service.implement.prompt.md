# Prompt History Record: Personalization Service

**Type**: Implementation Prompt  
**Date**: 2025-11-28  
**Phase**: Implement  
**Status**: ✅ Successful

---

## Context

Implementing content personalization that adapts textbook content to the user's skill level (beginner, intermediate, advanced).

## Prompt Used

```
Create a PersonalizationService that:
1. Accepts content and user skill level
2. Uses GPT-4 to adapt content complexity
3. Maintains technical accuracy
4. Preserves code examples
5. Returns personalized content
```

## Implementation Details

### P+Q+P Pattern Applied

**Persona:**
> You are an expert educator who adapts technical content for different skill levels while maintaining accuracy.

**Questions:**
> - What is the user's current skill level?
> - What technical concepts need simplification/expansion?
> - Which analogies would resonate with this level?

**Principles:**
> - Never sacrifice accuracy for simplicity
> - Add more examples for beginners
> - Add optimization tips for advanced users
> - Keep code examples intact

### Level Adaptations

| Level | Approach |
|-------|----------|
| Beginner | More analogies, step-by-step, basic terms |
| Intermediate | Standard explanations, practical examples |
| Advanced | Optimization tips, edge cases, internals |

### Service Implementation

```python
class PersonalizationService:
    async def personalize(
        self, 
        content: str, 
        level: str
    ) -> str:
        prompt = self._build_prompt(content, level)
        response = await openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
```

## Outcome

✅ Personalization working:
- Three distinct content levels
- Technical accuracy maintained
- Code blocks preserved
- Fast response (<3 seconds)

## Reusability

Use this pattern for any adaptive learning system:
1. Define clear skill levels
2. Create level-specific prompts
3. Preserve critical content (code, formulas)
4. Cache personalized versions for performance

