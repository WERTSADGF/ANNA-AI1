# ANNA AI Research Foundation

## Research Workflow

USER QUESTION
-> OBJECTIVE
-> SEARCH PLAN
-> SOURCE COLLECTION
-> SOURCE READING
-> INFORMATION EXTRACTION
-> CROSS-CHECK
-> UNCERTAINTY CHECK
-> SYNTHESIS
-> SOURCES
-> ANSWER

## Research Modes

### Normal Research

For ordinary questions.

### Deep Research

For questions requiring multiple relevant sources and conflict/uncertainty analysis.

## Claim Types

Every recorded finding can be classified as:

- Fact
- Inference
- Opinion
- Uncertain

The system does not treat those categories as interchangeable.

## Source Provenance

Sources preserve:

- URL
- Title
- Retrieval time
- Publisher
- Source type
- Accessed state

## Honesty Rule

The research layer must never claim:

- A source was accessed when it was not.
- Information was verified when it was not.
- A source supports a claim when the source was not actually inspected.

## Current Provider

Only a deterministic mock provider is used for testing.

A real search/source provider can later be added behind the same interface.

## Current Source Reader

The foundation contains a standard-library HTTP reader.

Network access is not assumed to have succeeded.

Every access returns explicit success/failure information.

## Current HTML Extraction

Basic HTML/script/style stripping is included.

It is intentionally simple and replaceable.

## Current Limitations

Not implemented yet:

- Search engine integration
- Search provider adapters
- Citation ranking
- Domain authority ranking
- Automatic claim extraction
- Automatic contradiction detection
- Source-quality scoring
- Deep research orchestration
- Browser rendering
- JavaScript-heavy page extraction
- PDF research ingestion
- YouTube research
- Persistent research knowledge storage

The next research iterations should add these incrementally.
