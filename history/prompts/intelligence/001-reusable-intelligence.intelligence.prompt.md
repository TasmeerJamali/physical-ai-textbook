# PHR-003: Reusable Intelligence Creation

## Metadata
- **Date**: 2024-11-29
- **Phase**: Intelligence
- **Spec Reference**: specs/001-physical-ai-textbook/spec.md
- **Bonus Feature**: +50 points for Claude Code Subagents and Agent Skills

## Prompt Evolution

### Initial Prompt
```
Create reusable AI components for the textbook that can be used across
different features (chatbot, personalization, translation).
```

### Refined Prompt
```
Following the P+Q+P pattern from Spec-Kit Plus, create:
1. Skills - Reusable prompt patterns with Persona, Questions, Principles
2. Subagents - Specialized agents that use skills for specific tasks
3. Document everything for grader verification
```

## Skills Created

### 1. robotics-explainer.skill.md
- **Purpose**: Explain robotics concepts at different levels
- **P+Q+P**:
  - Persona: Expert robotics instructor
  - Questions: User level, background, goals
  - Principles: Adapt to level, use analogies, provide examples

### 2. code-translator.skill.md
- **Purpose**: Translate content while preserving code
- **P+Q+P**:
  - Persona: Technical translator
  - Questions: Target language, preserve code?
  - Principles: Never translate code, handle RTL

### 3. content-personalizer.skill.md
- **Purpose**: Adapt content to user background
- **P+Q+P**:
  - Persona: Adaptive learning specialist
  - Questions: Experience level, programming background
  - Principles: Level-specific adaptations

## Subagents Created

### 1. qa-agent.subagent.md
- **Skills Used**: robotics-explainer
- **Purpose**: Answer textbook questions
- **Handoffs**: To translation-agent, personalization-agent

### 2. translation-agent.subagent.md
- **Skills Used**: code-translator
- **Purpose**: Translate to Urdu/other languages
- **Handoffs**: To qa-agent, personalization-agent

### 3. personalization-agent.subagent.md
- **Skills Used**: content-personalizer, robotics-explainer
- **Purpose**: Adapt content to user level
- **Handoffs**: To qa-agent, translation-agent

## Two-Output Philosophy

This implementation demonstrates the SDD-RI two-output philosophy:

1. **Working Code**: Backend services that use these patterns
2. **Intelligence Artifacts**: Documented skills and subagents

## Reusability Demonstration

The skills can be reused in:
- RAG chatbot responses
- Content personalization
- Urdu translation
- Quiz feedback
- Error explanations

## Lessons Learned

1. **P+Q+P is powerful**: Structured prompts produce consistent results
2. **Skills compose well**: Subagents can use multiple skills
3. **Documentation is key**: Graders need to see the thought process

## Verification Checklist

- [x] Skills follow P+Q+P pattern
- [x] Subagents reference skills
- [x] Handoff conditions defined
- [x] Usage examples provided
- [x] PHR documents the process

