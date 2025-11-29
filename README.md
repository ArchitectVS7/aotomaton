# Thursian Development Orchestrator

**Status**: MVP Complete ✅
**Version**: 0.1.0
**Type**: LangGraph-based workflow orchestrator with human-in-the-loop

---

## Overview

Thursian is a development workflow orchestrator that coordinates tasks through a deterministic state machine. The MVP uses **human agents** reading markdown guidelines, with a clear migration path to **AI-powered agents**.

**Key Features**:
- ✅ LangGraph state machine for deterministic workflows
- ✅ File-based protocol (.thursian/) for task communication
- ✅ Structured JSON decision logging for all agent assignments
- ✅ Git commits after each workflow phase for full traceability
- ✅ Human-in-the-loop with polling for completion
- ✅ Extension guide for migrating to AI agents

---

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create First Task

```bash
# Add task to queue
echo "Write a Python function to calculate factorial" > .thursian/task_queue.txt
```

### 3. Run Orchestrator

```bash
python -m orchestrator.main
```

### 4. Complete Tasks

**When orchestrator creates a task:**

1. **Read task file**: `.thursian/tasks/task_YYYYMMDD_HHMMSS.md`
2. **Follow agent guidelines**: `docs/agents/CODING_AGENT.md`
3. **Create output file**: `.thursian/output/task_YYYYMMDD_HHMMSS_output.md`
4. **Mark complete**: Include "**Status: COMPLETE**" in output

**When orchestrator requests validation:**

1. **Read validation task**: `.thursian/tasks/task_YYYYMMDD_HHMMSS_validation.md`
2. **Review primary output**: `.thursian/output/task_YYYYMMDD_HHMMSS_output.md`
3. **Follow validator guidelines**: `docs/agents/REVIEW_AGENT.md`
4. **Create validation file**: `.thursian/output/task_YYYYMMDD_HHMMSS_validation.md`
5. **Mark status**: Either "**Status: APPROVED**" or "**Status: NEEDS_REVISION**"

---

## Workflow Phases

```
IDLE
  ↓
TASK_SELECTION → Read from task queue
  ↓
ASSIGNMENT → Assign coding agent + review agent
  ↓
EXECUTION → Create task file, wait for human completion
  ↓ (polls every 5 seconds)
VALIDATION → Create validation task, wait for human review
  ↓ (polls every 5 seconds)
COMPLETED → Finalize workflow
```

**Loop-back patterns**:
- Execution loops until output file marked COMPLETE
- Validation loops until validation file created
- If validation says NEEDS_REVISION, returns to execution

---

## Project Structure

```
automaton/
├── .thursian/                  # File-based protocol directory
│   ├── tasks/                  # Task definitions from orchestrator
│   ├── output/                 # Completed work from agents
│   ├── decisions/              # JSON decision logs
│   ├── status.json             # Current workflow status
│   └── task_queue.txt          # Simple task backlog (FIFO)
├── orchestrator/               # Python orchestrator implementation
│   ├── state.py                # State definitions + phase enum
│   ├── helpers.py              # State transition helpers
│   ├── nodes.py                # 5 workflow nodes
│   ├── routing.py              # Conditional routing functions
│   ├── graph.py                # LangGraph graph construction
│   ├── git_manager.py          # Git commit automation
│   └── main.py                 # CLI entry point
├── docs/
│   ├── agents/
│   │   ├── CODING_AGENT.md     # Human agent guideline
│   │   └── REVIEW_AGENT.md     # Validator guideline
│   ├── orchestrator/
│   │   └── EXTENDING_TO_AI.md  # AI migration guide (4-8 hours)
│   └── patterns/
│       └── langgraph-patterns.md  # Implementation patterns
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Decision Logging

All agent assignments and tool usage are logged as structured JSON:

```json
{
  "task_id": "task_20250129_143022",
  "timestamp": "2025-01-29T14:30:22.123456",
  "phase": "execution",
  "agent_assigned": "coding_agent",
  "doc_reference": "docs/agents/CODING_AGENT.md",
  "tool_used": "file_creation",
  "reasoning": "Task requires code implementation",
  "outcome": "Task file created at .thursian/tasks/task_20250129_143022.md"
}
```

**Location**: `.thursian/decisions/`

---

## Git Traceability

After each phase transition, orchestrator creates a git commit:

```bash
git log --oneline

b5687d1 Workflow: execution (task: task_20250129_143022)
f6d54d8 Workflow: assignment (task: task_20250129_143022)
de063aa Workflow: task_selection (task: task_20250129_143022)
```

**Purpose**: Full audit trail of workflow execution for debugging and analysis.

---

## Extending to AI Agents

See **`docs/orchestrator/EXTENDING_TO_AI.md`** for complete migration guide.

**Summary**:
1. Install `langchain-anthropic` (2 hours)
2. Convert guidelines to system prompts (1 hour)
3. Implement AI-powered nodes (3 hours)
4. Add toggle mode (1 hour)

**Total**: 4-8 hours to full AI autonomy

**Toggle**:
```bash
USE_AI_AGENTS=true python -m orchestrator.main
```

---

## Architecture

This implementation follows proven patterns from `docs/patterns/langgraph-patterns.md`:

**Key Patterns**:
- `Annotated[List[T], operator.add]` for accumulating state (logs, errors, phase history)
- Error accumulation (not throwing exceptions)
- Loop-back routing for polling/waiting states
- Decision logging at every node
- Git commits for traceability

**State Machine**: Deterministic LangGraph StateGraph with conditional edges

---

## Examples

### Example 1: Simple Task

**Task**: "Write a Python function to calculate factorial"

**Process**:
1. Add to queue: `echo "Write a Python function..." > .thursian/task_queue.txt`
2. Run: `python -m orchestrator.main`
3. Complete execution (human implements factorial)
4. Complete validation (human reviews and approves)
5. Workflow completes

**Result**: Decision logs, git commits, complete audit trail

### Example 2: Revision Required

**Task**: "Implement user authentication"

**Process**:
1. Execution phase: Human implements auth
2. Validation phase: Reviewer finds security issue, marks NEEDS_REVISION
3. Workflow returns to execution
4. Human fixes issue, marks COMPLETE
5. Validation phase: Reviewer approves
6. Workflow completes

**Result**: Multiple execution iterations logged in decision logs

---

## Troubleshooting

### Workflow stuck in polling loop

**Symptom**: "Waiting for human to complete execution..."

**Solution**:
- Check if output file exists: `.thursian/output/task_YYYYMMDD_HHMMSS_output.md`
- Verify file contains: "**Status: COMPLETE**"

### Git commit failed

**Symptom**: "Git commit failed" in logs

**Solution**:
- Ensure git is initialized: `git status`
- Check if `.thursian/` directory has changes

### No tasks in queue

**Symptom**: "Task queue is empty"

**Solution**:
- Add tasks to: `.thursian/task_queue.txt` (one per line)

---

## Development Guidelines

### Adding New Agent Roles

1. Add to `AgentRole` enum in `orchestrator/state.py`
2. Create agent guidelines in `docs/agents/{AGENT_NAME}.md`
3. Update `assignment_node` logic in `orchestrator/nodes.py`

### Adding New Workflow Phases

1. Add to `WorkflowPhase` enum in `orchestrator/state.py`
2. Create node function in `orchestrator/nodes.py`
3. Add routing logic in `orchestrator/routing.py`
4. Update graph in `orchestrator/graph.py`

---

## Testing

Run end-to-end test:

```bash
# 1. Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Create test task
echo "Write a function to reverse a string" > .thursian/task_queue.txt

# 3. Run orchestrator
python -m orchestrator.main

# 4. Complete manually
# (follow on-screen instructions)

# 5. Verify
ls .thursian/decisions/     # Check decision logs
git log --oneline           # Check commits
cat .thursian/status.json   # Check final status
```

---

## Documentation

- **Agent Configuration**: `docs/agents/AGENT_CONFIGURATION_GUIDE.md`
- **LangGraph Patterns**: `docs/patterns/langgraph-patterns.md`
- **AI Extension Guide**: `docs/orchestrator/EXTENDING_TO_AI.md`
- **Integration Strategy**: `docs/integration/Focus-Pocus-Thursian-Alpha-Integration.md`

---

## License

Proprietary - Thursian Development Orchestrator

---

## Version History

- **v0.1.0** (2025-01-29): MVP release with human agents, file protocol, decision logging
- **v0.2.0** (planned): AI agent support with toggle mode
- **v0.3.0** (planned): Multi-task parallel execution
