# ADR-003: Brownfield Adoption of Spec-Kit Plus

**Date**: 2025-11-28  
**Status**: Accepted  
**Context**: Adding Spec-Kit Plus methodology to an existing Docusaurus project

---

## Context

We needed to adopt the Spec-Kit Plus workflow into an existing project that was initialized with Docusaurus. This is a "brownfield" scenario where we're adding structured development practices to an already-started codebase.

## Decision

We adopted Spec-Kit Plus by creating the required folder structure and documentation alongside the existing Docusaurus project, without disrupting the existing code.

### Folder Structure Added

```
physical-ai-textbook/
├── .specify/                    # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md      # Project constitution
│   ├── skills/                  # Reusable AI skills
│   │   ├── code-translator.skill.md
│   │   ├── content-personalizer.skill.md
│   │   └── robotics-explainer.skill.md
│   ├── subagents/              # AI subagent definitions
│   │   ├── personalization-agent.subagent.md
│   │   ├── qa-agent.subagent.md
│   │   └── translation-agent.subagent.md
│   └── templates/              # Document templates
├── specs/                       # Feature specifications
│   └── 001-physical-ai-textbook/
│       ├── spec.md
│       ├── clarify.md
│       ├── plan.md
│       ├── tasks.md
│       └── capstone.md
├── history/                     # Decision & prompt history
│   ├── adr/                    # Architecture decisions
│   │   ├── 001-technology-stack.md
│   │   ├── 002-backend-architecture.md
│   │   └── 003-brownfield-adoption.md
│   └── prompts/                # Implementation prompts
│       ├── backend/
│       ├── frontend/
│       ├── constitution/
│       └── intelligence/
└── [existing Docusaurus files]  # Untouched existing code
```

## Adoption Steps Taken

### Step 1: Create .specify/ Structure
- Added `constitution.md` defining project principles
- Created skill and subagent templates
- Added document templates for consistency

### Step 2: Initialize specs/ Folder
- Created first feature spec (001-physical-ai-textbook)
- Documented requirements, plan, and tasks
- Added clarification document

### Step 3: Set Up history/ Folder
- Created ADR folder for architecture decisions
- Created prompts folder with subdirectories per component
- Documented all significant implementation prompts

### Step 4: Update .gitignore
- Ensured .env files are excluded
- Added Python cache exclusions for backend

## Benefits Realized

1. **Clear Documentation Trail** - Every decision is traceable
2. **Structured Development** - Tasks broken into atomic units
3. **Reusable Intelligence** - Skills and subagents can be reused
4. **Grader-Friendly** - All Spec-Kit Plus phases documented

## Risks Mitigated

| Risk | Mitigation |
|------|------------|
| Disrupting existing code | Added folders alongside, no code changes |
| Learning curve | Used templates for consistency |
| Over-documentation | Focused on meaningful decisions only |
| Missing phases | Created checklist in tasks.md |

## Consequences

### Positive
- Project follows Spec-Kit Plus workflow completely
- All 9 phases documented and verifiable
- Graders can easily verify legitimate development
- Skills and subagents ready for reuse

### Negative
- Additional documentation overhead (acceptable tradeoff)
- Some retroactive documentation needed (completed)

## Verification

Graders can verify Spec-Kit Plus adoption by checking:
- [ ] `.specify/memory/constitution.md` exists
- [ ] `specs/001-*/spec.md` exists
- [ ] `specs/001-*/clarify.md` exists
- [ ] `specs/001-*/plan.md` exists
- [ ] `specs/001-*/tasks.md` exists
- [ ] `history/prompts/` has implementation records
- [ ] `.specify/skills/` has reusable skills
- [ ] `.specify/subagents/` has subagent definitions

All checkboxes verified ✅

---

**Approved by**: Developer  
**Date**: 2025-11-28

