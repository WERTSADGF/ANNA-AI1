import re
from html import unescape


class SourceTextExtractor:

    def extract(self, content: str) -> str:

        if not content:
            return ""

        text = re.sub(
            r"(?is)<script.*?>.*?</script>",
            " ",
            content,
        )

        text = re.sub(
            r"(?is)<style.*?>.*?</style>",
            " ",
            text,
        )

        text = re.sub(
            r"(?s)<[^>]+>",
            " ",
            text,
        )

        text = unescape(text)

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()
