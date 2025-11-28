# ADR-001: Technology Stack for Physical AI Textbook

> **Scope**: Complete technology stack for the AI-native textbook including frontend, backend, database, and AI components.

- **Status:** Accepted
- **Date:** 2025-11-28
- **Feature:** Core Infrastructure
- **Context:** Building an AI-native textbook for Physical AI & Humanoid Robotics that requires a static site generator, RAG chatbot, authentication, and personalization features. Must use free-tier services and score 300/300 in hackathon.

## Decision

### Frontend Stack
- **Framework**: Docusaurus 3.x with TypeScript
- **UI Components**: Custom React components (ChatWidget, PersonalizeButton, TranslateButton)
- **Styling**: Docusaurus theme + CSS modules
- **Deployment**: GitHub Pages (free)

### Backend Stack
- **Framework**: FastAPI (Python 3.11+)
- **AI/RAG**: OpenAI Agents SDK with GPT-4
- **Vector Database**: Qdrant Cloud (free tier - 1GB storage)
- **Relational Database**: Neon Serverless Postgres (free tier - 0.5GB)
- **Deployment**: Railway or Render (free tier)

### Authentication
- **Library**: Better-Auth
- **Features**: Email/password signup, user profiling questions

### Development Tools
- **Methodology**: Spec-Kit Plus (SDD-RI)
- **AI Assistant**: Claude Code / Augment Agent
- **Version Control**: Git with GitHub

## Consequences

### Positive
- Docusaurus is purpose-built for documentation/textbooks with excellent MDX support
- FastAPI provides async performance and automatic OpenAPI docs
- Qdrant offers excellent vector search with generous free tier
- Neon provides serverless Postgres with auto-scaling
- All services have free tiers meeting hackathon budget constraints
- OpenAI Agents SDK provides structured agent development
- Better-Auth is lightweight and easy to integrate

### Negative
- Docusaurus has limited dynamic content capabilities (mitigated by React components)
- Free tiers have usage limits (acceptable for hackathon demo)
- Multiple services increase deployment complexity
- OpenAI API costs for production use (acceptable for demo)

## Alternatives Considered

### Alternative Stack A: Next.js + Supabase
- **Pros**: Full-stack framework, integrated auth and database
- **Cons**: Overkill for documentation site, more complex setup
- **Why rejected**: Docusaurus is better suited for textbook format

### Alternative Stack B: VitePress + Firebase
- **Pros**: Fast, simple, Google ecosystem
- **Cons**: Less React flexibility, Firebase pricing unpredictable
- **Why rejected**: Docusaurus has better plugin ecosystem for our needs

### Alternative Stack C: GitBook + Custom Backend
- **Pros**: Beautiful out-of-box, no frontend work
- **Cons**: Limited customization, paid features needed
- **Why rejected**: Cannot add custom React components for chatbot

### Vector DB Alternatives
- **Pinecone**: More popular but free tier is limited
- **Weaviate**: Good but more complex setup
- **ChromaDB**: Local only, not suitable for deployed app
- **Why Qdrant**: Best free tier (1GB), simple API, cloud-hosted

## References

- Feature Spec: `specs/001-physical-ai-textbook/spec.md`
- Implementation Plan: `specs/001-physical-ai-textbook/plan.md`
- Related ADRs: None (first ADR)
- Constitution: `.specify/memory/constitution.md`

