---
type: implement
mode: backend
---

# Fix: Personalization Data Flow & Logic

## Context
The "Better-Auth" bonus feature requires personalizing content based on the user's background (Experience Level, Programming Languages, etc.). Testing revealed that while the data was collected during signup, it was not being correctly passed to the RAG service for answer generation.

## Issues Identified
1.  **Frontend**: `ChatWidget` was hardcoded to `user_level='intermediate'` and ignored other background fields.
2.  **Frontend**: `ContentActions` was reading from a non-existent `userBackground` localStorage key instead of the main `user` object.
3.  **Backend**: `auth.py` was not returning the full user profile (languages, goals) in the Login/Signup response.
4.  **Backend**: `rag_service.py`'s `explain_text` method did not accept or use the detailed profile fields.

## Requirements
1.  **Update Auth API**: Ensure `/api/auth/login` and `/api/auth/signup` return the full user object.
2.  **Update Frontend State**: Modify `AuthModal`, `ChatWidget`, and `ContentActions` to store and retrieve the full user profile from `localStorage`.
3.  **Update RAG Service**:
    *   Expand `answer_question` and `explain_text` signatures to accept `programming_languages`, `robotics_experience`, etc.
    *   Pass this context to the `RoboticsExplainerSkill` to generate truly personalized responses (e.g., using Python analogies for Python users).

## Goal
Ensure the Personalization feature is fully functional and compliant with the Hackathon's "Better-Auth" bonus requirements.
