# Clarification Document: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook  
**Created**: 2025-11-28  
**Last Updated**: 2025-11-28  
**Spec Reference**: `specs/001-physical-ai-textbook/spec.md`

---

## Clarification Sessions

### Session 1: Initial Requirements Clarification

**Date**: 2025-11-28  
**Participants**: Developer, AI Assistant

#### Questions Asked & Answers Received

**Q1: What specific topics must be covered in the Physical AI textbook?**
> A: The textbook must cover 4 modules: (1) ROS 2 - The Robotic Nervous System, (2) Gazebo & Unity - The Digital Twin, (3) NVIDIA Isaac - The AI-Robot Brain, (4) VLA Models - Vision-Language-Action. Each module needs 3+ chapters with code examples.

**Q2: What are the exact scoring criteria for the hackathon?**
> A: Base score 100 points for RAG chatbot, +50 for Better-Auth, +50 for Personalization, +50 for Urdu Translation, +50 for Reusable Intelligence = 300 total.

**Q3: What technology constraints exist?**
> A: Must use OpenAI Agents SDK for RAG, Qdrant for vector storage, Neon Postgres for user data, Better-Auth for authentication. Frontend must be Docusaurus deployed to GitHub Pages.

**Q4: How will graders verify work is legitimate?**
> A: Graders check specs/, history/, and .specify/ folders. They verify Spec-Kit Plus workflow was followed, not "vibe coding". All prompts, decisions, and iterations must be documented.

---

### Session 2: Edge Cases & Constraints

**Date**: 2025-11-28

#### Identified Edge Cases

| Edge Case | Resolution |
|-----------|------------|
| User asks question outside textbook scope | AI responds: "I can only answer questions about Physical AI topics covered in this textbook" |
| OpenAI API rate limit exceeded | Implement exponential backoff, cache common responses |
| Qdrant unavailable | Fallback to keyword search in local content |
| Translation API fails | Show error toast, keep English content displayed |
| User has no internet during personalization | Cache last personalized version locally |
| Mobile user tries text selection | Provide alternative "Ask AI" button in mobile view |
| Urdu RTL breaks code blocks | Preserve LTR for code blocks only |

#### Clarified Constraints

1. **Free Tier Limits**: All cloud services (Qdrant, Neon, OpenAI) must work within free tier limits
2. **Response Time**: RAG chatbot must respond within 5 seconds
3. **Content Accuracy**: All technical content must be verified against official documentation
4. **Personalization Levels**: Exactly 3 levels - Beginner, Intermediate, Advanced
5. **Authentication**: Email/password only, no OAuth required for MVP

---

### Session 3: Technical Decisions Clarification

**Date**: 2025-11-28

#### Architecture Questions

**Q: Should the backend be deployed separately or as serverless functions?**
> A: Deploy as a single FastAPI service to Railway/Render. Serverless adds complexity without benefit for this use case.

**Q: How should content embeddings be structured?**
> A: Chunk content into ~500 token segments with metadata (chapter_id, section, module). Store in Qdrant with OpenAI embeddings.

**Q: What user profile data is collected?**
> A: Three questions during signup: (1) Experience level (beginner/intermediate/advanced), (2) Hardware access (Jetson/RTX GPU/None), (3) Learning goals (free text).

---

## Outstanding Questions

*None - all critical questions resolved*

---

## Clarification Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2025-11-28 | Initial clarification document | Project kickoff |
| 2025-11-28 | Added edge cases section | Identified during implementation planning |
| 2025-11-28 | Resolved all outstanding questions | Implementation complete |

---

## Sign-off

- [x] All critical questions answered
- [x] Edge cases documented
- [x] Constraints clearly defined
- [x] Ready for implementation

**Approved by**: Developer  
**Date**: 2025-11-28

