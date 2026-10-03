# ANNA AI Assistant Foundation

## Phase 9

The Assistant layer provides:

- Tasks
- Task status
- Reminders
- Projects
- Project/task relationships
- Persistent local state
- Permission-aware mutations
- Due-reminder queries

Task states:

TODO
IN PROGRESS
BLOCKED
DONE

## Architecture

CHAT SERVICE
->
ASSISTANT SERVICE
->
PERMISSION CHECK
->
LOCAL ASSISTANT STORE

Assistant state is stored locally in:

`data/assistant.json`

## Permission Boundary

Task, reminder, and project creation are low-risk operations.

Project deletion is an important change and requires explicit confirmation.

PC control, application launching, file modification, and agent execution are not part of this phase.

## Current Limitations

- No background notification scheduler yet.
- No natural-language task parser yet.
- No calendar integration yet.
- No application-launch tool yet.
- No PC-control execution yet.
- No agent mode yet.

These remain later phases.

## Verification

The Phase 9 tests verify task persistence, reminder due detection, project/task relationships, confirmation protection, and ChatService integration.
