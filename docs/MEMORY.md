# ANNA AI Memory Foundation

## Memory Classes

- Working
- Personal
- Project
- Learning
- Knowledge
- Episodic
- Sensitive
- Uncertain

## Persistent Memory Metadata

Each persistent memory contains:

- ID
- Type
- Content
- Source
- Created date
- Updated date
- Confidence
- Importance
- Privacy level
- Project association
- Optional expiration
- Status
- Confirmation state

## Memory Operations

- Store
- Retrieve
- Update
- Merge foundation reserved for later
- Archive
- Delete
- Forget
- Confirm

## Storage Policy

ANNA does not automatically store everything.

The current foundation requires:

- Non-empty content
- Minimum confidence
- Minimum importance
- Correct privacy classification for sensitive memory

## Retrieval Policy

The foundation does not load all memory automatically.

The retrieval layer supports:

- Query relevance
- Memory type filtering
- Confidence filtering
- Privacy filtering
- Sensitive-memory permission
- Result limits

## Current Retrieval

The current implementation uses a simple deterministic keyword relevance mechanism.
Expired memories are excluded from retrieval.

Semantic/vector retrieval is not implemented yet.

## Privacy

Sensitive memory is hidden unless sensitive retrieval is explicitly allowed.

## Current Scope

Implemented:

- Memory models
- Memory storage
- Memory policy
- Memory retrieval
- Memory manager
- Memory JSON storage
- Memory tests

Not implemented yet:

- Embeddings
- Vector database
- Automatic memory extraction
- Automatic memory consolidation
- Full intent-driven retrieval
- Memory merge intelligence
- Expiration worker
- UI memory controls
