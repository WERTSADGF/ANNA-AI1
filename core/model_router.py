from chat.providers import ChatModelProvider, MockModelProvider
from config.chat_settings import ChatSettings, load_chat_settings


class ModelRouter:
    """
    Provider-independent model selection foundation.

    Provider selection can come from explicit caller input or
    from ChatSettings when no provider is supplied.
    """

    def __init__(self, settings: ChatSettings | None = None):
        self.settings = settings or load_chat_settings()

        self._providers: dict[str, ChatModelProvider] = {
            "mock": MockModelProvider(),
        }

    def get_chat_provider(
        self,
        provider_name: str | None = None,
    ) -> ChatModelProvider:

        selected_provider = provider_name or self.settings.provider

        provider = self._providers.get(selected_provider)

        if provider is None:
            raise ValueError(
                f"Unsupported chat provider: {selected_provider}"
            )

        return provider
