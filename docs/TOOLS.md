# ANNA AI Coding + Safe PC Control

## Phase 10 Scope

Phase 10 introduces a controlled local tool layer.

Current capabilities:

- Local system information
- Python source inspection
- Project test execution
- Authorized project-directory listing
- Safe project-directory creation
- Allowlisted application launch proposals
- Permission-aware execution
- Dry-run action proposals
- Execution verification

## Architecture

CHAT SERVICE
->
TOOL SERVICE
->
PERMISSION CHECK
->
CONTROLLED LOCAL EXECUTION
->
VERIFICATION

## Coding Support

Coding support currently focuses on deterministic project operations:

- Inspect Python syntax
- Inspect imports and line counts
- Run the existing test suite
- Report verified success/failure

The model remains responsible for reasoning and code-generation through the normal chat provider.

## PC Safety

The tool layer does not accept arbitrary shell commands.

Application launching uses a fixed allowlist.

Project file paths must remain inside the ANNA project directory.

Important application-launch actions require explicit confirmation.

## Dry Run

Actions that can change the local environment can be proposed without executing them.

A dry-run result is not reported as executed or verified.

## Current Limitations

- No arbitrary terminal command execution.
- No recursive destructive file deletion.
- No registry modification.
- No unrestricted application launching.
- No autonomous action loops.
- No agent mode.
- No background automation.

These remain subject to later phases and hardening.
