# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook  
**Created**: 2025-11-28  
**Status**: Approved  
**Spec Reference**: `specs/001-physical-ai-textbook/spec.md`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (GitHub Pages)                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Docusaurus 3.x + React                    │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │
│  │  │ Module 1 │ │ Module 2 │ │ Module 3 │ │ Module 4 │        │    │
│  │  │  ROS 2   │ │ Gazebo   │ │  Isaac   │ │   VLA    │        │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │    │
│  │  ┌──────────────────────────────────────────────────┐       │    │
│  │  │ Custom Components: ChatWidget, Personalize, Urdu │       │    │
│  │  └──────────────────────────────────────────────────┘       │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ API Calls
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND (Railway/Render)                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    FastAPI + Python 3.11                     │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │
│  │  │  /chat   │ │  /auth   │ │/personal │ │/translate│        │    │
│  │  │   RAG    │ │Better-Auth│ │  ize    │ │   Urdu   │        │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │    │
│  │  ┌──────────────────────────────────────────────────┐       │    │
│  │  │         OpenAI Agents SDK (GPT-4 + RAG)          │       │    │
│  │  └──────────────────────────────────────────────────┘       │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐              ┌──────────────────────┐
│   Qdrant Cloud       │              │   Neon Postgres      │
│   (Vector DB)        │              │   (User Data)        │
│   - Embeddings       │              │   - Users            │
│   - Semantic Search  │              │   - Profiles         │
└──────────────────────┘              │   - Sessions         │
                                      └──────────────────────┘
```

---

## Implementation Phases

### Phase 1: Frontend Foundation (Days 1-2)
1. Initialize Docusaurus with TypeScript
2. Configure theme and navigation
3. Create folder structure for 4 modules
4. Add placeholder content for all chapters
5. Deploy to GitHub Pages

### Phase 2: Backend Foundation (Days 2-3)
1. Initialize FastAPI project
2. Set up Neon Postgres connection
3. Set up Qdrant Cloud connection
4. Create database models (User, ChatSession)
5. Deploy to Railway/Render

### Phase 3: RAG Chatbot (Days 3-5)
1. Embed textbook content into Qdrant
2. Implement OpenAI Agents SDK integration
3. Create /chat endpoint with context retrieval
4. Build ChatWidget React component
5. Implement text selection → chat trigger

### Phase 4: Authentication (Days 5-6)
1. Integrate Better-Auth
2. Create signup/signin pages
3. Implement user profiling questions
4. Store user preferences in Neon

### Phase 5: Personalization (Days 6-7)
1. Create PersonalizeButton component
2. Implement /personalize endpoint
3. Create 3 content variants per chapter
4. Cache personalized content

### Phase 6: Urdu Translation (Days 7-8)
1. Create TranslateButton component
2. Implement /translate endpoint
3. Handle RTL layout
4. Preserve code blocks in English

### Phase 7: Content & Polish (Days 8-10)
1. Write complete chapter content
2. Add code examples and exercises
3. Test all user journeys
4. Performance optimization

---

## API Contracts

### POST /api/chat
```json
Request:
{
  "message": "What is a ROS 2 node?",
  "context": "Selected text from chapter...",
  "chapter_id": "ros2-nodes",
  "user_id": "optional-user-id"
}

Response:
{
  "response": "A ROS 2 node is...",
  "sources": ["Chapter 1.2: ROS 2 Nodes"],
  "confidence": 0.95
}
```

### POST /api/auth/signup
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword",
  "profile": {
    "experience_level": "beginner|intermediate|advanced",
    "hardware_access": ["jetson", "rtx4070", "none"],
    "learning_goals": "Build autonomous robot"
  }
}
```

### POST /api/personalize
```json
Request:
{
  "chapter_id": "ros2-nodes",
  "user_id": "user-123"
}

Response:
{
  "content": "Personalized markdown content...",
  "level": "beginner"
}
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OpenAI API rate limits | Implement caching, use smaller model for simple queries |
| Qdrant free tier limits | Optimize embedding size, prioritize key content |
| Translation quality | Use GPT-4 for translation, human review key terms |
| Time constraints | Prioritize P1 features, bonus features if time permits |

---

## ADR References

- ADR-001: Technology Stack (`history/adr/001-technology-stack.md`)

