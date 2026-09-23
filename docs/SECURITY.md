# ANNA AI Security Foundation

## Security Flow

MODEL
-> PLAN
-> POLICY
-> PERMISSION
-> TOOL
-> EXECUTION
-> VERIFICATION

## Current Security Components

- PermissionManager
- ToolAllowlist
- DirectoryAllowlist
- AuditLogger
- Existing policy engine

## Current Tool Policy

Only the read_only tool is enabled.

Terminal execution is NOT enabled.

PC control is NOT enabled.

Agent mode is NOT enabled.

Destructive automation is NOT enabled.

## Permission Levels

0 = Read-only

1 = Low-risk

2 = Important change, requires confirmation

3 = High-impact, requires explicit confirmation

## Security Principle

The AI model is not the final authority for high-impact actions.

Permissions must be enforced outside the model's reasoning.
