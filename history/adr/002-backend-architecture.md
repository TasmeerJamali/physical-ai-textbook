# ADR-002: Backend Architecture

## Status
Accepted

## Date
2024-11-29

## Context
We need a backend to power the RAG chatbot, authentication, and personalization features for the Physical AI textbook.

## Decision

### Framework: FastAPI
**Chosen**: FastAPI with Python 3.11+

**Rationale**:
- Native async support for concurrent requests
- Automatic OpenAPI documentation
- Pydantic integration for validation
- Excellent performance

**Alternatives Considered**:
- Flask: Less async support
- Django: Overkill for API-only backend
- Express.js: Would require separate language from AI/ML code

### AI Model: GPT-4o-mini
**Chosen**: OpenAI GPT-4o-mini

**Rationale**:
- Cost-effective ($0.15/1M input tokens)
- Sufficient quality for educational Q&A
- Fast response times
- Easy integration with OpenAI SDK

**Alternatives Considered**:
- GPT-4: More expensive, overkill for this use case
- Claude: Good but OpenAI Agents SDK required
- Open source (Llama): Requires hosting infrastructure

### Vector Database: Qdrant Cloud
**Chosen**: Qdrant Cloud (free tier)

**Rationale**:
- 1GB free storage
- Easy Python SDK
- Good performance for semantic search
- No credit card required

**Alternatives Considered**:
- Pinecone: More complex setup
- Weaviate: Heavier infrastructure
- ChromaDB: Less production-ready

### Authentication: JWT with Better-Auth compatibility
**Chosen**: Custom JWT implementation compatible with Better-Auth

**Rationale**:
- Stateless authentication
- Easy frontend integration
- Can migrate to Better-Auth later
- Simple implementation for hackathon

## Consequences

### Positive
- Fast development with FastAPI
- Cost-effective AI with GPT-4o-mini
- Free hosting possible with Qdrant Cloud
- Clean separation of concerns

### Negative
- In-memory user store needs database migration
- GPT-4o-mini may have occasional quality issues
- Qdrant free tier has storage limits

### Risks
- OpenAI API rate limits during demo
- Qdrant Cloud availability

## Implementation Notes
- Use environment variables for all secrets
- Implement retry logic for API calls
- Add request logging for debugging

