
---

# 📘 **Thursian Autonomous Development Workflow (v1.0)**

*A deterministic, STOP-gated, multi-agent orchestration pipeline for autonomous code execution.*

---

# 🔁 **High-Level Loop**

The system continuously performs:

```
Idle → Select Task → Multi-Agent Execution → Documentation → Next Task
```

Every task is processed under governance, STOP-gates, and agentic cross-verification.

---

# 🧩 **Workflow Stages**

Below is the full workflow with strong wording, precise definitions, and zero ambiguity.

---

## **1. Task Selection Stage**

**Trigger:** System becomes idle (no active task).
**Behavior:**

1. Query the **task list** or **Kanban board**.
2. Identify the **first unblocked “TODO” item**.
3. Mark it as **“In Progress”**.
4. Begin the orchestration loop.

**Purpose:** Ensure deterministic FIFO processing, prevent starvation, and avoid working on blocked items.

---

## **2. Planning Stage**

**Goal:** Understand the task with full context before assigning agents.

**Behavior:**

* Load and analyze relevant **project documentation** (PRD, ARN, AFS, architecture notes).
* Identify upstream, downstream, and cross-system dependencies.
* Clarify acceptance criteria and any required STOP gates.

**Outcome:** A precise mental model of what needs to be built.

---

## **3. Assignment Stage**

**Goal:** Select the correct **Primary Agent** + **Validator Agent**.

**Inputs:**

* Task description
* Project context
* Domain of work (language/framework/toolchain)
* Difficulty level

**Behavior:**

1. Select an appropriate **Agent Protocol** (stored as `.md` playbooks).
2. Select a **Validator Agent** (QA, reviewer, specialist, PM, etc).

   > You have over 100 agents — system picks based on domain.
3. Record assignments in the orchestration log.

**Outcome:** Two agents are now committed:

* **Primary Executor**
* **Independent Verifier**

---

## **4. Training & Research Stage**

**Purpose:** Prime the agent pair with correct knowledge.

**Behavior:**

* Load the selected agent protocol (*.md file*).
* Pull in any project-specific docs or prior artifacts.
* Perform a proportional web search for:

  * Source documentation
  * Library references
  * Patterns and prior examples
  * Similar code solutions

**Note:**
Not every task needs deep research. The system scales effort based on:

* Complexity
* Safety impact
* Dependency chain width
* Novelty of domain

**Outcome:** Agents enter execution fully informed.

---

## **5. Execution Phase (Primary Agent)**

**Goal:** Produce the solution.

**Behavior:**

* Implement the required code or artifact.
* Follow the selected agent framework strictly.
* Write code in small deterministic units.
* Perform internal reasoning and incremental planning.

**Deliverables:**

* Working code or artifact
* Structured commit message or patch block
* Notes on decisions or tradeoffs (if any)

---

## **6. Self-Check Phase (Primary Agent)**

**Goal:** Validate correctness before external review.

**Behavior:**

* Compare output against the Atomic Feature Spec.
* Perform local testing:

  * Unit tests
  * Static analysis
  * Style/linting
  * Basic integration tests
* Ensure code meets all acceptance criteria.

**Outcome:**
Primary Agent produces a **self-verified artifact**.

---

## **7. Second-Check Phase (Validator Agent)**

**Goal:** Independent review and verification.

**Behavior:**

* Load the produced artifact AND the AFS.
* Validate:

  * Atomic requirements
  * Upstream/downstream integration
  * Constraints
  * Safety rules
  * Project architecture
* Run a broader test suite (integration + edge cases).
* If changes are necessary:

  * Validator updates the artifact
  * Changes are logged in the **Run ChangeLog**

**Deliverables:**

* Agreement OR
* Revised artifact + change notes

---

## **8. Approval Loop (STOP-Gate)**

**Goal:** Ensure both agents reach agreement on the final artifact.

**Rules:**

* Max **3 approval cycles** to prevent infinite loops.
* Each iteration:

  * Primary reviews validator changes
  * Primary accepts or disputes
  * Validator re-checks

**Logging:**
All loop iterations go into:

🗂 **approval-loop.log**
(*Your dedicated file for loop history, reasons, and outcomes*)

**If agreement after ≤ 3 loops:** proceed.
**If no agreement after 3 loops:** escalate to supervisory agent.

---

## **9. Escalation Stage (Project Manager Agent)**

**Goal:** Resolve disagreements with higher authority.

**Behavior:**

* Supervisory PM loads full context:

  * Task details
  * Both agent protocols
  * approval-loop.log
  * ChangeLog
  * Project documentation
* Computes **confidence score** (> 90% required).
* Determines outcome:

### Possible Outcomes:

1. **Approved** → Continue workflow
2. **Send back for rework** → Restart at Execution
3. **Mark task “On Hold”** → Requires human intervention
4. **Reassign to different domain agents**

**Logging:**
All escalation events go into:

🗂 **escalation-actions.log**

**Parallelism Rule:**
Work continues on other tasks; only this task is paused.

---

## **10. Documentation Stage**

**Goal:** Ensure system traceability & reproducibility.

**Behavior:**

* Update:

  * Work list
  * Kanban board
  * Task status
  * Assignee history
  * Running ChangeLog (*not verbose; succinct description*)
* Mark task as **Complete**.

**Outcome:**
Stable artifact with complete lineage.

---

## **11. Next-Task Stage**

Loop back to **Stage 1** and pick the next available task.

---

# 🧩 This workflow forms your full Thursian Autodev Loop

## **State Machine View**

```
Idle
  ↓
Task Selection
  ↓
Planning
  ↓
Assignment
  ↓
Training
  ↓
Execution
  ↓
Self-Check
  ↓
Second-Check
  ↓
Approval Loop (≤3x)
  ↘             ↙
    Escalation (Optional)
       ↓
Documentation
  ↓
Next Task
  ↓
Idle
```
