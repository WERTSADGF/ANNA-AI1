# ANNA AI

ANNA AI is a personal AI system built around three core roles:

1. Personal AI Companion
2. Personal AI Assistant
3. Personal AI Tutor / Teaching Friend

## Current Phase

Foundation

## Build Principles

- Build incrementally.
- Inspect existing project state before changes.
- Preserve working components.
- Use PowerShell for implementation.
- Keep providers replaceable.
- Keep permissions separate from model reasoning.
- Test meaningful modules.
- Verify actions before reporting success.
- Do not silently drift from the ANNA AI Master Plan.

## Current Known Component

- data_preprocessing.py

## Current Known Issue

No known import-time failure remains in data_preprocessing.py.

The legacy preprocessing component is now import-safe and exposes
an explicit preprocess_data() function for caller-supplied datasets.

## Important

This README describes the current project state only.
