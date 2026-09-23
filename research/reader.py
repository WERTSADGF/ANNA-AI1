from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class SourceContent:
    url: str
    content: str
    retrieved_at: str
    success: bool
    error: str = ""


class SourceReader:

    def read(self, url: str) -> SourceContent:

        request = Request(
            url,
            headers={
                "User-Agent": "ANNA-AI-Research/1.0"
            },
        )

        try:
            with urlopen(
                request,
                timeout=15,
            ) as response:

                raw = response.read()

                content_type = (
                    response.headers.get(
                        "Content-Type",
                        "",
                    ).lower()
                )

                charset = "utf-8"

                if "charset=" in content_type:
                    charset = content_type.split(
                        "charset=",
                        1,
                    )[1].split(
                        ";",
                        1,
                    )[0].strip()

                text = raw.decode(
                    charset,
                    errors="replace",
                )

                return SourceContent(
                    url=url,
                    content=text,
                    retrieved_at=datetime.now(
                        timezone.utc
                    ).isoformat(),
                    success=True,
                )

        except Exception as exc:
            return SourceContent(
                url=url,
                content="",
                retrieved_at=datetime.now(
                    timezone.utc
                ).isoformat(),
                success=False,
                error=str(exc),
            )
