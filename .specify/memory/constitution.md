# Physical AI & Humanoid Robotics Textbook Constitution

## Project Overview

This constitution governs the development of an AI-native technical textbook on Physical AI and Humanoid Robotics, built using Docusaurus with an integrated RAG chatbot, authentication, personalization, and translation features.

**Project Name**: Physical AI Textbook
**Target Audience**: Developers learning robotics, ROS 2, simulation, and VLA models
**Hackathon Goal**: Score 300/300 points by implementing all required and bonus features

---

## Core Principles

### I. Specification-First Development (NON-NEGOTIABLE)
Every feature, chapter, and component MUST be specified before implementation:
- All work starts with a specification document in `specs/`
- No code is written until spec is approved and tasks are defined
- ADRs document all significant architectural decisions
- PHRs capture prompt patterns that work for content generation

### II. Educational Excellence
Content quality is paramount:
- Every chapter must be beginner-friendly yet technically accurate
- Include hands-on code examples with comments
- Provide 3+ practice exercises per chapter
- Use the P+Q+P pattern (Persona + Questions + Principles) for personalization
- Content must be verifiable against official documentation

### III. Modular Architecture
The system is composed of independent, testable modules:
- **Frontend**: Docusaurus static site with custom React components
- **Backend**: FastAPI with OpenAI Agents SDK for RAG
- **Database**: Neon Postgres for user data, Qdrant for vector embeddings
- **Auth**: Better-Auth for signup/signin with user profiling
- Each module has its own specification and can be developed/tested independently

### IV. Accessibility & Internationalization
The textbook must be accessible to diverse learners:
- Mobile-first responsive design
- Support for Urdu translation (RTL layout considerations)
- Content personalization based on user skill level (Beginner/Intermediate/Advanced)
- Clear visual hierarchy and readable typography

### V. AI-Assisted Development
Leverage AI intelligently:
- Use structured prompts (documented in PHRs) for content generation
- Create reusable Skills and Subagents for repetitive tasks
- Never use AI output without human review
- All AI-generated content must be verified for accuracy

### VI. Test-Driven Quality
Quality is enforced through testing:
- Unit tests for all backend endpoints
- Integration tests for auth flows and RAG functionality
- E2E tests for critical user journeys
- Content accuracy verified against official sources (ROS 2 docs, NVIDIA Isaac docs)

---

## Technology Stack Decisions

### Frontend
- **Framework**: Docusaurus 3.x with TypeScript
- **UI Components**: Custom React components for ChatWidget, PersonalizeButton, TranslateButton
- **Styling**: Docusaurus theme + custom CSS modules
- **Hosting**: GitHub Pages

### Backend
- **Framework**: FastAPI with Python 3.11+
- **AI/RAG**: OpenAI Agents SDK with GPT-4
- **Vector DB**: Qdrant Cloud (free tier)
- **Database**: Neon Serverless Postgres (free tier)
- **Hosting**: Railway or Render (free tier)

### Authentication
- **Library**: Better-Auth
- **User Data**: Background questions for personalization (experience level, hardware access, learning goals)

---

## Content Structure

### Module 1: ROS 2 - The Robotic Nervous System
- Introduction to ROS 2 concepts
- Nodes, Topics, Services, Actions
- URDF and robot modeling
- Hands-on: First publisher/subscriber

### Module 2: Gazebo & Unity - The Digital Twin
- Physics simulation fundamentals
- Sensor simulation (cameras, LiDAR, IMU)
- Integration with ROS 2
- Hands-on: Simulate a robot in Gazebo

### Module 3: NVIDIA Isaac - The AI-Robot Brain
- Isaac Sim overview
- Isaac ROS integration
- VSLAM and Nav2
- Hands-on: AI perception pipeline

### Module 4: VLA Models - Vision-Language-Action
- Multimodal AI for robotics
- OpenAI Whisper for voice commands
- LLMs for robot reasoning
- Hands-on: Build a voice-controlled robot

---

## Quality Gates

### Before Merge
- [ ] Specification exists and is approved
- [ ] All acceptance criteria are met
- [ ] Tests pass (unit, integration where applicable)
- [ ] PHR created for significant prompts
- [ ] ADR created for architectural decisions
- [ ] Code reviewed for security and best practices

### Content Quality
- [ ] Technical accuracy verified
- [ ] Code examples tested and working
- [ ] Exercises have solutions
- [ ] Personalization variants created (3 levels)
- [ ] Urdu translation reviewed for technical terms

---

## Governance

1. This constitution supersedes all other development practices
2. Amendments require documentation in an ADR with rationale
3. All features must align with the hackathon scoring criteria
4. Complexity must be justified by user value

**Version**: 1.0.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
