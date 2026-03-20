# AI Toolbox

A portable library of reusable AI agents and skills. This repo contains no application code — it exists solely to store agent definitions and skill modules that can be copied into any project.

## How to Use

Copy the `.agents/agents/` and `.agents/skills/` directories (or individual files) into your target project. Agents read the **target project's** `AGENTS.md` for workspace conventions, not this repo's.

## Available Agents

| Agent | Role | Tools | Invocation |
|-------|------|-------|------------|
| `architect` | Orchestrator — delegates all work, never implements directly | Read-only + agent delegation | User-invocable, primary entry point |
| `planner` | Context enricher — asks questions, creates plan.yaml with DAG of tasks | Read-only | Subagent of architect |
| `fe-engineer` | Frontend implementation — React 19, TS, Tailwind v4, Next.js/Vite | Full edit | Subagent |
| `ui-engineer` | Web quality — accessibility (WCAG 2.1 AA), SEO, Core Web Vitals | Full edit | Subagent |
| `be-js-engineer` | Backend JS — TypeScript + Bun.js APIs | Full edit | Subagent |
| `be-rust-engineer` | Backend Rust — Axum/Actix APIs and scripts | Full edit | Subagent |
| `quality-engineer` | Testing — Vitest unit tests, Playwright e2e | Full edit | Subagent |
| `security-engineer` | Security audit — OWASP Top 10, secrets, vulnerabilities | Read-only (never modifies code) | Subagent |

## Delegation Protocol

The `architect` orchestrates all work through a formal delegation protocol. Every task flows through a plan.

### Plan Location

```
docs/plan/{plan_id}/plan.yaml
```

### Plan Schema

```yaml
plan_id: string
objective: string
created_at: string                     # ISO 8601
status: pending_approval | approved | in_progress | completed | failed
complexity: simple | medium | complex

tasks:
  - id: string                         # e.g., "task_001"
    title: string                      # Deliverable-focused, not code-focused
    description: |                     # Rich context for the assigned agent
    wave: number                       # Execution wave: 1 runs first, 2 waits for 1, etc.
    agent: string                      # One of the available agents
    status: pending | in_progress | completed | failed | needs_revision
    dependencies:
      - string                         # Task IDs this depends on
    context_files:
      - string                         # Relevant files for the agent
    acceptance_criteria:
      - string                         # How to verify completion
    verification:
      - string                         # Commands or checks to run
    estimated_effort: small | medium | large

contracts:                             # Inter-task interfaces
  - from_task: string                  # Producer task ID
    to_task: string                    # Consumer task ID
    interface: string                  # What producer provides
    format: string                     # Data format or schema

pre_mortem:                            # Risk analysis (complex tasks only)
  overall_risk_level: low | medium | high
  critical_failure_modes:
    - scenario: string
      likelihood: low | medium | high
      impact: low | medium | high
      mitigation: string
```

### Task Status Lifecycle

```
pending → in_progress → completed
                      → needs_revision → in_progress
                      → failed (after 3 retries)
```

### Delegation Message Format

When architect delegates to a subagent via `runSubagent`, it passes:

```json
{
  "task_id": "string",
  "plan_id": "string",
  "plan_path": "docs/plan/{plan_id}/plan.yaml",
  "task_definition": {
    "title": "string",
    "description": "string",
    "context_files": ["string"],
    "acceptance_criteria": ["string"],
    "verification": ["string"],
    "contracts": []
  }
}
```

### Agent Response Format

Every subagent returns:

```json
{
  "status": "completed | failed | needs_revision",
  "task_id": "string",
  "plan_id": "string",
  "summary": "Brief summary, max 3 sentences",
  "failure_type": "transient | fixable | needs_replan | escalate",
  "extra": {}
}
```

### Execution Rules

1. **Wave ordering**: Wave 1 tasks execute first (up to 4 concurrent). Wave 2 waits for Wave 1, etc.
2. **Retry policy**: Failed tasks retry up to 3 times. After max retries, escalate to user.
3. **Contracts**: For wave > 1, include contracts from dependencies in the task_definition.
4. **Failure handling**:
   - `transient` → retry same task
   - `fixable` → re-delegate with error logs injected
   - `needs_replan` → delegate to planner for replanning
   - `escalate` → mark blocked, ask user
5. **Read-only agents** (planner, security-engineer) must never modify source code.
6. **Plan approval**: Complex plans require user approval before execution.
