# ANNA AI Chat

## Purpose

This layer provides the Core Chat + Companion runtime foundation.

## Current Flow

USER TEXT
-> CHAT SESSION
-> COMPANION CONTEXT
-> MODEL ROUTER
-> CHAT MODEL PROVIDER
-> CHAT RESPONSE
-> CHAT SESSION UPDATE

## Chat Session

The chat session stores short-lived conversation history for the current chat service instance.

Session state is intentionally separate from persistent ANNA memory.

The session supports:

- Add user and assistant messages
- Read conversation history
- Clear the current conversation

Persistent memory remains a later integration layer.

## Companion Integration

The chat service builds Companion context before sending a request to the model provider.

Current Companion guidance includes:

- ANNA identity as an AI
- Response language detected from current input
- Warm-natural tone
- Natural-conversational style
- AI identity transparency when relevant

The Companion profile remains provider-independent.

## Provider Independence

The application communicates through the `ChatModelProvider` interface.

`ModelRouter` selects the configured provider through `ChatSettings`.

The existing deterministic `mock` provider remains the default foundation provider.

A real AI provider can later be added without replacing the chat service architecture.

## Current Scope

Implemented:

- Chat message model
- Chat request model
- Chat response model
- Chat session
- Chat service
- Companion context integration
- Provider abstraction
- Model router
- Chat configuration
- Deterministic test provider
- Application chat entrypoint
- Automated Phase 2 integration tests

Not implemented yet:

- Real external AI provider
- Persistent memory integration
- Full language preference/context integration
- Voice
- Web research
- File retrieval
- Tutor engine integration
- Assistant tools
- PC control
- Agent mode
