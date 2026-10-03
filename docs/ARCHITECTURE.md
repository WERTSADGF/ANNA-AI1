# ANNA AI Architecture

## Core Direction

ANNA AI is a:

- Personal AI Companion
- Personal AI Assistant
- Personal AI Tutor / Teaching Friend

ANNA is always an AI.

## Current Foundation

- Configuration
- Structured logging
- Security policy foundation
- Permission levels
- Database abstraction
- Application entry point
- Foundation tests
- Core Chat
- Chat session state
- Companion behavior foundation
- Provider abstraction
- Model routing

## Current Chat Flow

USER TEXT
-> CHAT SESSION
-> COMPANION CONTEXT
-> MODEL ROUTER
-> CHAT MODEL PROVIDER
-> CHAT RESPONSE
-> CHAT SESSION UPDATE

## Security Flow

MODEL
-> PLAN
-> POLICY
-> PERMISSION
-> TOOL
-> EXECUTION
-> VERIFICATION

## Current Limitations

- Only the deterministic mock chat provider is connected.
- Persistent memory is not yet integrated into Core Chat.
- Full language preference/context integration is not yet connected to Core Chat.
- No unrestricted operating-system control exists.
- No autonomous agent mode exists.
- No destructive automation exists.
- No real voice provider is connected.

## Next Architecture Layers

- Memory integration
- Language integration
- Files and knowledge
- Research
- Voice
- Tutor integration
- Assistant tools
- Coding
- Safe PC control
- Agent mode
- Optimization and hardening
