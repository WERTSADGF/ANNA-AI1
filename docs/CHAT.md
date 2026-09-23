# ANNA AI Chat Foundation

## Purpose

This layer establishes the basic provider-independent conversation foundation.

## Current Flow

USER TEXT
-> CHAT SERVICE
-> MODEL ROUTER
-> CHAT MODEL PROVIDER
-> CHAT RESPONSE

## Current Provider

Only a deterministic `mock` provider exists at this stage.

The mock provider is used for testing architecture and must not be treated as a real AI model.

## Provider Independence

The application communicates through the `ChatModelProvider` interface.

A real AI provider can later be added without rewriting the chat service.

## Current Scope

Implemented:

- Chat message model
- Chat request model
- Chat response model
- Chat service
- Provider abstraction
- Model router
- Deterministic test provider
- Chat configuration
- Automated tests

Not implemented yet:

- Real external model provider
- Memory
- Companion personality
- Voice
- Web research
- File retrieval
- Tutor engine
- PC control
- Agent mode
