# Thursian Development Orchestrator Implementation Plan

**ORG-004: LangGraph + GitHub + N8N Integration Design**

**Status**: ✅ APPROVED - Ready for Implementation
**Version**: 1.0
**Target**: Weekend Prototype (2-4 hours)
**Repository**: `thursian-dev-orchestrator` (separate from Focus-Pocus)
**Tech Stack**: Docker + N8N + LangGraph + File Protocol + AutoHotKey (Windows 10)

---

## Quick Start

**Full plan available at**: `C:\Users\J\.claude\plans\noble-herding-tiger.md`

**Next step**: Create new repository at `C:\dev\GIT\thursian-dev-orchestrator`

---

## Executive Summary

Hybrid orchestration system combining:
- **LangGraph**: Deterministic state machine (proven patterns from Focus-Pocus)
- **File Protocol** (`.thursian/`): Rich context communication
- **AutoHotKey**: Automated notifications to Claude Code
- **N8N**: Event triggers and system integration
- **PostgreSQL**: Workflow state persistence

**Key Innovation**: Separates data transport (files) from notification (AutoHotKey) to achieve full autonomy while preserving context.

---

## Repository Structure

```
thursian-dev-orchestrator/
├── orchestrator/              # LangGraph + FastAPI
├── claude-bridge/             # AutoHotKey scripts
├── n8n-workflows/             # N8N workflow exports
├── .thursian-template/        # File protocol template
└── docs/                      # Architecture docs
```

---

## Implementation Phases (2-4 hours)

1. **Repository Setup** (30 min) - Directory structure, Python venv
2. **Docker Setup** (20 min) - N8N + PostgreSQL via docker-compose
3. **LangGraph Workflow** (60 min) - State machine implementation
4. **AutoHotKey Bridge** (15 min) - Windows notification system
5. **N8N Integration** (30 min) - Webhooks and triggers
6. **Test Project** (15 min) - End-to-end validation

---

## Workflow Phases

```
IDLE → Task Selection → Planning → Assignment → Execution
  → Self-Check → Validation → Approval Loop → Documentation → COMPLETED
```

**Human-in-the-Loop**: AutoHotKey alerts Claude Code when tasks are ready

---

## File Protocol (.thursian/)

Every project has:
```
.thursian/
├── tasks/           # Input task definitions
├── output/          # Completed work
├── approvals/       # Review artifacts
├── status.txt       # Current workflow status
└── current_task.txt # Active task ID
```

**Communication Flow**:
1. LangGraph writes task → `.thursian/tasks/{id}.md`
2. N8N triggers AutoHotKey alert
3. Claude Code reads full context from file
4. Work completed → `.thursian/output/{id}_output.md`
5. LangGraph detects completion → advances workflow

---

## Critical Success Criteria

✅ LangGraph workflow compiles and runs
✅ AutoHotKey successfully alerts Claude Code
✅ File protocol working (task files → output files)
✅ One complete end-to-end workflow cycle
✅ N8N webhook triggers AutoHotKey

---

**Full implementation details in master plan file**
**Ready to create repository and begin Phase 1**
