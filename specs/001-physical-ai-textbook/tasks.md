# Tasks: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook  
**Created**: 2025-11-28  
**Plan Reference**: `specs/001-physical-ai-textbook/plan.md`

---

## Task Breakdown

### Epic 1: Frontend Foundation

#### Task 1.1: Initialize Docusaurus Project
- [ ] Run `npx create-docusaurus@latest . classic --typescript`
- [ ] Configure `docusaurus.config.ts` with project metadata
- [ ] Set up navigation for 4 modules
- [ ] Verify local dev server works

**Acceptance**: `npm start` shows homepage with navigation

#### Task 1.2: Create Module Structure
- [ ] Create `docs/module-1-ros2/` with intro.md
- [ ] Create `docs/module-2-gazebo/` with intro.md
- [ ] Create `docs/module-3-isaac/` with intro.md
- [ ] Create `docs/module-4-vla/` with intro.md
- [ ] Update sidebars.ts for all modules

**Acceptance**: All 4 modules visible in sidebar navigation

#### Task 1.3: Deploy to GitHub Pages
- [ ] Configure GitHub Actions workflow
- [ ] Set baseUrl for GitHub Pages
- [ ] Push to repository
- [ ] Verify deployment at `https://tasmeerjamali.github.io/physical-ai-textbook`

**Acceptance**: Site accessible via GitHub Pages URL

---

### Epic 2: Backend Foundation

#### Task 2.1: Initialize FastAPI Project
- [ ] Create `backend/` directory
- [ ] Set up virtual environment
- [ ] Install FastAPI, uvicorn, openai, qdrant-client, asyncpg
- [ ] Create `main.py` with health check endpoint
- [ ] Create `requirements.txt`

**Acceptance**: `uvicorn main:app` runs, `/health` returns 200

#### Task 2.2: Database Setup
- [ ] Create Neon Postgres database
- [ ] Create `models.py` with User, ChatSession schemas
- [ ] Create `database.py` with connection pool
- [ ] Run migrations to create tables

**Acceptance**: Can connect to Neon and query users table

#### Task 2.3: Qdrant Setup
- [ ] Create Qdrant Cloud cluster
- [ ] Create `qdrant_client.py` with connection
- [ ] Create collection for textbook embeddings
- [ ] Test vector insertion and search

**Acceptance**: Can insert and retrieve vectors from Qdrant

#### Task 2.4: Deploy Backend
- [ ] Create Railway/Render project
- [ ] Configure environment variables
- [ ] Deploy FastAPI app
- [ ] Verify health endpoint accessible

**Acceptance**: Backend API accessible at deployed URL

---

### Epic 3: RAG Chatbot (100 pts base)

#### Task 3.1: Content Embedding Pipeline
- [ ] Create script to read all markdown files
- [ ] Chunk content into ~500 token segments
- [ ] Generate embeddings using OpenAI
- [ ] Store embeddings in Qdrant with metadata

**Acceptance**: All chapter content embedded in Qdrant

#### Task 3.2: OpenAI Agents SDK Integration
- [ ] Install openai-agents-sdk
- [ ] Create RAG agent with retrieval tool
- [ ] Configure system prompt for textbook assistant
- [ ] Test agent responses

**Acceptance**: Agent answers questions using textbook context

#### Task 3.3: Chat API Endpoint
- [ ] Create `/api/chat` POST endpoint
- [ ] Accept message, context, chapter_id
- [ ] Retrieve relevant chunks from Qdrant
- [ ] Generate response with OpenAI agent
- [ ] Return response with sources

**Acceptance**: API returns contextual answers within 5 seconds

#### Task 3.4: ChatWidget Component
- [ ] Create `src/components/ChatWidget.tsx`
- [ ] Implement floating chat button
- [ ] Create chat interface with message history
- [ ] Connect to backend API
- [ ] Add text selection trigger

**Acceptance**: User can select text, click Ask AI, get response

---

### Epic 4: Authentication (+50 pts bonus)

#### Task 4.1: Better-Auth Integration
- [ ] Install better-auth package
- [ ] Configure auth providers (email/password)
- [ ] Create auth API routes
- [ ] Set up session management

**Acceptance**: Auth endpoints work for signup/signin

#### Task 4.2: User Profiling
- [ ] Create onboarding flow component
- [ ] Add 3 background questions
- [ ] Store responses in user profile
- [ ] Display profile in dashboard

**Acceptance**: New users answer questions, data saved

---

### Epic 5: Personalization (+50 pts bonus)

#### Task 5.1: PersonalizeButton Component
- [ ] Create `src/components/PersonalizeButton.tsx`
- [ ] Add button to chapter layout
- [ ] Call personalization API on click
- [ ] Replace content with personalized version

**Acceptance**: Button visible, content changes on click

#### Task 5.2: Personalization API
- [ ] Create `/api/personalize` endpoint
- [ ] Retrieve user profile
- [ ] Generate personalized content variant
- [ ] Cache result for performance

**Acceptance**: API returns content matching user level

---

### Epic 6: Urdu Translation (+50 pts bonus)

#### Task 6.1: TranslateButton Component
- [ ] Create `src/components/TranslateButton.tsx`
- [ ] Add button to chapter layout
- [ ] Call translation API on click
- [ ] Handle RTL layout switch

**Acceptance**: Button visible, content shows in Urdu

#### Task 6.2: Translation API
- [ ] Create `/api/translate` endpoint
- [ ] Use GPT-4 for translation
- [ ] Preserve code blocks in English
- [ ] Cache translations

**Acceptance**: API returns Urdu translation with code intact

---

### Epic 7: Reusable Intelligence (+50 pts bonus)

#### Task 7.1: Create Content Generation Skill
- [ ] Document P+Q+P pattern for chapter writing
- [ ] Create reusable prompt template
- [ ] Store in `history/prompts/skills/`

#### Task 7.2: Create Personalization Subagent
- [ ] Define persona for adaptive learning
- [ ] Create question set for level detection
- [ ] Document principles for content adaptation

**Acceptance**: Skills documented and reusable

---

## Progress Tracking

| Epic | Tasks | Completed | Status |
|------|-------|-----------|--------|
| 1. Frontend | 3 | 0 | Not Started |
| 2. Backend | 4 | 0 | Not Started |
| 3. RAG Chatbot | 4 | 0 | Not Started |
| 4. Authentication | 2 | 0 | Not Started |
| 5. Personalization | 2 | 0 | Not Started |
| 6. Translation | 2 | 0 | Not Started |
| 7. Intelligence | 2 | 0 | Not Started |

