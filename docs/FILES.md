# ANNA AI File Assistant Foundation

## Pipeline

FILE
-> AUTHORIZED PATH CHECK
-> METADATA
-> CONTENT EXTRACTION
-> CHUNKING
-> INDEXING
-> RETRIEVAL

## Security

Files must be inside explicitly authorized directories.

The file assistant does not provide unrestricted filesystem access.

This foundation does not modify user files during ingestion.

## Built-in Formats

Current dependency-free extraction supports common text/code formats:

- TXT
- MD
- PY
- JS
- TS
- JSX
- TSX
- HTML
- CSS
- JSON
- CSV
- YAML
- YML
- XML
- LOG
- SQL
- PS1
- BAT
- CMD

## Optional Formats

The architecture recognizes:

- PDF
- DOCX
- PPTX
- XLSX
- Images

These remain behind optional adapter boundaries and are not falsely marked as supported until the required parser capability is actually installed and verified.

## Indexing

The current index is a simple in-memory lexical index.

It is intentionally replaceable.

Future implementations may use:

- Persistent indexing
- Embeddings
- Vector/semantic retrieval
- Source-aware retrieval
- Page/section metadata
- Multimodal extraction

## Current Scope

Implemented:

- File authorization
- File type detection
- File metadata
- Text extraction
- Chunking
- Local lexical index
- Retrieval
- Optional adapter registry
- File service
- Tests

Not implemented yet:

- PDF parser
- DOCX parser
- PPTX parser
- XLSX parser
- Image understanding
- Persistent semantic index
- OCR
- Audio/video extraction
- File modification tools
