from files.authorization import FileAuthorizer
from files.chunker import TextChunker
from files.extractor import TextExtractor
from files.index import LocalTextIndex
from files.inspector import FileInspector
from files.models import FileSearchResult


class FileService:

    def __init__(
        self,
        authorizer: FileAuthorizer,
        index: LocalTextIndex | None = None,
    ):
        self.authorizer = authorizer
        self.inspector = FileInspector()
        self.extractor = TextExtractor()
        self.chunker = TextChunker()
        self.index = index or LocalTextIndex()

    def inspect(self, path: str):
        authorized = self.authorizer.require_authorized(path)

        return self.inspector.inspect(
            str(authorized)
        )

    def ingest(self, path: str):
        metadata = self.inspect(path)

        content = self.extractor.extract(
            metadata
        )

        chunks = self.chunker.chunk(
            file_path=metadata.path,
            content=content,
        )

        self.index.add(chunks)

        return metadata, chunks

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[FileSearchResult]:

        return self.index.search(
            query=query,
            limit=limit,
        )
