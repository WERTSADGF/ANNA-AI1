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

data_preprocessing.py references a placeholder dataset path:

path_to_your_dataset.csv

It has passed Python syntax compilation but currently fails during import because the referenced dataset file does not exist.

## Important

This README describes the current project state only.
