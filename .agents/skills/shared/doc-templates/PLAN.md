# Plan template

`plan.yaml` in the feature folder. Written by `planner`, executed and kept current by `architect`.

```yaml
plan_id: string                        # the feature slug
objective: string
spec: string                           # path to spec.md, or null for a simple plan
created_at: string                     # ISO 8601
status: pending_approval | approved | in_progress | completed | failed
complexity: simple | medium | complex

tasks:
  - id: string                         # task_001, task_002, ...
    title: string                      # deliverable-focused, not code-focused
    slice: string                      # the vertical slice this task belongs to
    description: |                     # rich context for the assigned agent
    wave: number                       # 1 runs first, 2 waits for 1, and so on
    agent: string                      # a specialist from the architect's roster
    tier: fast | standard | deep       # model tier, see the delegation skill
    status: pending | in_progress | completed | failed | needs_revision
    dependencies:
      - string                         # task ids this waits for
    context_files:
      - string                         # pointers: spec sections, research, code
    acceptance_criteria:
      - string                         # how to verify completion
    verification:
      - string                         # commands or checks to run
    estimated_effort: small | medium | large

contracts:                             # interfaces between tasks in different waves
  - from_task: string
    to_task: string
    interface: string                  # what the producer provides
    format: string                     # data format or schema

pre_mortem:                            # complex plans only
  overall_risk_level: low | medium | high
  critical_failure_modes:
    - scenario: string
      likelihood: low | medium | high
      impact: low | medium | high
      mitigation: string
  assumptions:
    - string                           # what would invalidate the plan
```

## Task lifecycle

```
pending → in_progress → completed
                      → needs_revision → in_progress
                      → failed (after 3 retries, then escalate to the user)
```

## Slices and tasks

A **slice** is the unit of demo: a narrow path through every layer (schema, API, UI, tests) that works on its own. A **task** is the unit of delegation: one specialist, at most 3 files or about 500 lines. A slice that spans specialists becomes several tasks with the same `slice` value, joined by contracts.
