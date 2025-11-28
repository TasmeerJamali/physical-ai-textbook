# 🤖 Physical AI & Humanoid Robotics Textbook

An **AI-Native Textbook** for learning Physical AI and Humanoid Robotics, built for the Panaversity Hackathon.

## 🎯 Features

### Core Features (100 pts)
- ✅ **Docusaurus Textbook** - 4 comprehensive modules
- ✅ **RAG Chatbot** - Ask questions, get contextual answers
- ✅ **OpenAI Agents SDK** - Powered by GPT-4o-mini
- ✅ **Qdrant Vector DB** - Semantic search over content

### Bonus Features (+200 pts)
- ✅ **Better-Auth** (+50) - Signup/signin with background questions
- ✅ **Personalization** (+50) - Adapt content to your level
- ✅ **Urdu Translation** (+50) - اردو میں ترجمہ
- ✅ **Reusable Intelligence** (+50) - Skills & Subagents

## 📚 Modules

| Module | Topic | Technologies |
|--------|-------|--------------|
| 1 | ROS 2 - The Robotic Nervous System | Nodes, Topics, Services |
| 2 | Gazebo & Unity - Digital Twins | Physics Simulation |
| 3 | NVIDIA Isaac - AI-Robot Brain | Isaac Sim, cuVSLAM |
| 4 | VLA Models - Vision-Language-Action | Multimodal AI |

## 🛠️ Tech Stack

- **Frontend**: Docusaurus 3.x, React, TypeScript
- **Backend**: FastAPI, Python 3.11
- **Database**: Neon Serverless Postgres
- **Vector DB**: Qdrant Cloud
- **AI**: OpenAI GPT-4o-mini
- **Auth**: Better-Auth compatible JWT

## 🚀 Quick Start

### Frontend
```bash
npm install
npm start
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
physical-ai-textbook/
├── docs/                    # Textbook content
├── src/                     # React components
├── backend/                 # FastAPI backend
├── .specify/                # Spec-Kit Plus artifacts
│   ├── memory/             # Constitution
│   ├── skills/             # Reusable AI skills
│   └── subagents/          # AI subagents
├── specs/                   # Feature specifications
└── history/                 # ADRs and PHRs
    ├── adr/                # Architectural decisions
    └── prompts/            # Prompt history records
```

## 📋 Spec-Kit Plus Compliance

This project follows **SDD-RI** (Specification-Driven Development with Reusable Intelligence):

- ✅ Constitution defined before coding
- ✅ Specifications with user stories
- ✅ ADRs for all major decisions
- ✅ PHRs documenting prompt evolution
- ✅ Skills following P+Q+P pattern
- ✅ Subagents with handoff conditions

## 🏆 Hackathon Scoring

| Category | Points | Status |
|----------|--------|--------|
| Base (Textbook + Chatbot) | 100 | ✅ |
| Better-Auth | +50 | ✅ |
| Personalization | +50 | ✅ |
| Urdu Translation | +50 | ✅ |
| Reusable Intelligence | +50 | ✅ |
| **Total** | **300** | 🏆 |

## 👤 Author

**Tasmeer Jamali**
- GitHub: [@tasmeerjamali](https://github.com/tasmeerjamali)

---
*Built with ❤️ for the Panaversity Hackathon*
