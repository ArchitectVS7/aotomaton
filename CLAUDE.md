# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Automaton** is a documentation and architectural planning repository for the Thursian development orchestrator system. This repository contains design documents, integration assessments, agent configuration guides, and LangGraph workflow patterns.

**Key Purpose**: Design and document AI-powered workflow orchestration systems that coordinate multiple AI agents using LangGraph state machines, file-based protocols, and human-in-the-loop gates.

## Repository Structure

```
automaton/
├── docs/
│   ├── agents/              # AI agent configuration guides
│   ├── integration/         # Integration assessments and bridge plans
│   ├── patterns/            # LangGraph workflow patterns
│   └── references/          # Implementation plans and examples
```

## Core Concepts

### 1. AI Agent Configuration Framework

The "Human Factor" framework (defined in `docs/agents/AGENT_CONFIGURATION_GUIDE.md`) establishes how to design human-like AI agents with:

- **8 Human Factors**: Communication Style, Best Time to Engage, Strengths, Growth Areas, Quirks, Collaboration Preference, Feedback Style, Bias
- **Intentional Limitations**: Every agent has predictable weaknesses and biases
- **Complementary Teams**: Agents with opposing biases create healthy tension
- **Real Archetypes**: Based on Myers-Briggs, workplace stereotypes, literary characters

**Key Principle**: Perfect agents are not trustworthy - realistic agents with predictable strengths and limitations build trust.

### 2. LangGraph Workflow Patterns

Proven patterns from Focus-Pocus implementation (documented in `docs/patterns/langgraph-patterns.md`):

**State Management**:
- Use `Annotated[List[T], operator.add]` for accumulating data (logs, errors, phase history)
- Use plain `List[T]` for replacement data
- Define phase enums for type safety
- Helper functions for consistent state transitions

**Node Implementation**:
- All nodes are async-compatible
- Return dictionaries (LangGraph auto-merges)
- Try/except with error accumulation (don't throw exceptions)
- Explicit phase transitions in return statements

**Human-in-the-Loop Gates**:
- Three-state flag system: `waiting_for_human`, `current_gate`, `gate_data`
- Turbo mode bypass option
- Selective gate enablement
- Loop-back routing pattern for waiting states

**LLM Model Selection**:
- Haiku for parsing, classification, intermediate processing
- Sonnet for final reports, complex reasoning, critical decisions
- Temperature tuning (0.8 for diversity in persona generation)

### 3. Integration Architecture

The bridge architecture strategy (documented in `docs/integration/`) balances:

- **Standalone deployment**: Ship Focus-Pocus as standalone SaaS
- **Future integration**: Preserve path to extract as workflow in Thursian-Lite platform
- **Bridge components**: 10-hour investment preserves integration path without scope creep

**Bridge Components**:
1. Workflow Manifest (workflow contract)
2. Lineage Tracking (TraceGraph compatibility)
3. Role Constraints (agent boundaries)
4. LLM Router (cost + quality optimization)
5. Retry Logic (production reliability)
6. Documentation (knowledge preservation)

### 4. File Protocol (.thursian/)

Communication pattern for LangGraph orchestrator:
```
.thursian/
├── tasks/           # Input task definitions
├── output/          # Completed work
├── approvals/       # Review artifacts
├── status.txt       # Current workflow status
└── current_task.txt # Active task ID
```

Workflow cycle:
1. LangGraph writes task → `.thursian/tasks/{id}.md`
2. Notification system alerts agent
3. Agent reads full context from file
4. Work completed → `.thursian/output/{id}_output.md`
5. LangGraph detects completion → advances workflow

## Development Guidelines

### Documentation Style

When creating or modifying documentation:

1. **Use vivid, specific examples** rather than generic descriptions
2. **Include anti-patterns** (❌ Bad / ✅ Good comparisons)
3. **Provide implementation code samples** when documenting patterns
4. **Create decision frameworks** with clear criteria
5. **Document "why" not just "what"** - explain the reasoning behind patterns

### Agent Configuration

When defining new AI agents:

1. **Start with role**, build personality around it
2. **Make limitations intentional** - every strength has a shadow side
3. **Use real human archetypes** (mentor, librarian, coach, perfectionist)
4. **Create complementary teams** - different biases, balanced weaknesses
5. **Test configuration** - Can you predict how the agent will respond?

### LangGraph Workflows

When designing or modifying workflows:

1. **Define clear phase enums** upfront
2. **Create helper functions** for state transitions
3. **Use conditional routing** for state-dependent paths
4. **Implement error accumulation** instead of throwing exceptions
5. **Add human-in-the-loop gates** at decision points
6. **Log key operations** for debugging

## Key Documentation Files

### Agent Configuration
- `docs/agents/AGENT_CONFIGURATION_GUIDE.md` - Complete framework for designing AI agents
- `docs/agents/AGENT_TEMPLATE.md` - Template for creating new agent profiles

### Integration Strategy
- `docs/integration/Focus-Pocus-Thursian-Alpha-Integration.md` - Bridge architecture assessment
- `docs/integration/10-HOUR-BRIDGE-PLAN-ALIGNMENT.md` - Work breakdown verification

### Implementation Patterns
- `docs/patterns/langgraph-patterns.md` - Production-proven LangGraph patterns from Focus-Pocus
- `docs/references/ORG-004-Implementation-Plan.md` - Orchestrator implementation plan

### Workflow Examples
- `docs/references/N8N Orchestrator Example 1.md` - N8N integration patterns
- `docs/references/N8N Orchestrator Example 2.md` - Additional N8N examples
- `docs/references/Programming Workflow Example.md` - Programming workflow patterns

## Architecture Principles

### 1. Deterministic State Machines
Use LangGraph StateGraph for all workflow orchestration - avoid dynamic routing that makes workflows unpredictable.

### 2. File-Based Context
Rich context in files (markdown task definitions) separates data transport from notification, enabling full autonomy while preserving context.

### 3. Intentional Bias
Agents with explicit biases create healthy tension and force critical thinking - don't create "perfect" agents.

### 4. Evolutionary Architecture
Bridge components preserve future integration paths without committing to platform complexity upfront.

### 5. Production Hardening
LLM Router + Retry Logic + Error Accumulation patterns ensure reliability in production.

## Notes for Claude Code

- This is a **documentation repository** with no executable code (Python, TypeScript, etc.)
- Focus on **markdown documentation quality** when making changes
- Preserve the **vivid, specific writing style** with examples and anti-patterns
- When asked about implementation, reference the patterns documented here
- Integration assessments use **decision frameworks** - preserve the structure when updating
- Agent configurations follow the **Human Factor framework** - maintain consistency
