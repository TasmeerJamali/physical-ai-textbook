# PHR-002: Backend Implementation

## Metadata
- **Date**: 2024-11-29
- **Phase**: Implement
- **Spec Reference**: specs/001-physical-ai-textbook/spec.md
- **Task Reference**: specs/001-physical-ai-textbook/tasks.md - Epic 2

## Prompt Evolution

### Initial Prompt
```
Create a FastAPI backend with:
1. RAG chatbot using OpenAI Agents SDK
2. Qdrant vector database integration
3. Authentication endpoints
4. Personalization and translation services
```

### Refined Prompt
```
Implement the backend following the architecture in plan.md:
- FastAPI with async support
- Pydantic settings for configuration
- Modular router structure
- Service layer for business logic
- OpenAI GPT-4o-mini for cost efficiency
```

## Key Decisions Made

### 1. Model Selection
- **Decision**: Use GPT-4o-mini instead of GPT-4
- **Rationale**: Cost-effective for educational content, sufficient quality
- **Trade-off**: Slightly less sophisticated responses

### 2. Vector Database
- **Decision**: Qdrant Cloud free tier
- **Rationale**: Free, easy setup, good Python SDK
- **Alternative Considered**: Pinecone (more complex setup)

### 3. Authentication
- **Decision**: JWT-based auth compatible with Better-Auth
- **Rationale**: Stateless, easy to integrate with frontend
- **Note**: In-memory store for demo, use database in production

## Implementation Details

### Files Created
1. `backend/app/main.py` - FastAPI application
2. `backend/app/config.py` - Pydantic settings
3. `backend/app/routers/chat.py` - RAG chat endpoints
4. `backend/app/routers/auth.py` - Authentication endpoints
5. `backend/app/routers/personalize.py` - Personalization endpoints
6. `backend/app/services/rag_service.py` - RAG implementation
7. `backend/app/services/personalization_service.py` - Content adaptation
8. `backend/app/services/translation_service.py` - Urdu translation

### API Endpoints
- `POST /api/chat/ask` - Ask question with RAG
- `POST /api/chat/explain` - Explain selected text
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/personalize/adapt` - Personalize content
- `POST /api/personalize/translate` - Translate to Urdu

## Lessons Learned

1. **Code preservation in translation**: Must extract code blocks before translation
2. **User level adaptation**: Three levels (beginner/intermediate/advanced) sufficient
3. **RAG context building**: Combine selected text + chapter context + vector search

## Next Steps
1. Create frontend ChatWidget component
2. Integrate with Docusaurus
3. Set up Qdrant collection and index textbook content
4. Deploy to Railway/Render

## Reusable Patterns

### P+Q+P Pattern for RAG
```
Persona: Expert robotics instructor
Questions: What is user's level? What context is available?
Principles: Adapt language, cite sources, admit uncertainty
```

