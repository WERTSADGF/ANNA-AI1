# ANNA AI — Agent Mode

## Status

Phase 11 foundation is implemented and verified as a bounded, foreground Agent Mode.

## Architecture

Agent flow:

USER GOAL -> DETERMINISTIC PLAN -> BOUNDED RUNNER -> ONE TOOL STEP -> TOOL RESULT -> VERIFICATION -> STOP/CONTINUE

The Agent layer contains:

- `agent/models.py` — run, step, plan, status, and stop-reason models.
- `agent/planner.py` — deterministic planning for the currently supported tool actions.
- `agent/executor.py` — executes exactly one planned tool step.
- `agent/runner.py` — advances a bounded plan and enforces stopping rules.
- `agent/service.py` — public Agent API.
- `ChatService.agent_plan()` and `ChatService.agent_run()` — runtime integration.

## Supported Actions

The current planner recognizes:

- System information
- Python source inspection
- Project test execution
- Authorized directory listing
- Authorized directory creation
- Allowlisted application launching

These actions are delegated to the existing Phase 10 `ToolService`.

## Safety Boundaries

The Agent does not bypass the existing permission system.

Application launching remains an IMPORTANT_CHANGE and requires explicit confirmation before real execution.

Dry-run results are not reported as executed or verified.

The Agent runner enforces a maximum step budget.

A run stops when:

- The goal is completed.
- The plan is exhausted.
- The step budget is exhausted.
- Permission/confirmation is required.
- Verification fails.
- A tool action fails.
- An unsupported action is requested.

## Current Limitations

This phase does not provide:

- Arbitrary shell execution.
- Unrestricted PC control.
- Background automation.
- Persistent autonomous operation.
- Dynamic unrestricted replanning.
- Model-generated autonomous tool selection.
- Agent operation outside the existing ToolService permissions and boundaries.

The current implementation is therefore a bounded Agent foundation, not unrestricted autonomy.
