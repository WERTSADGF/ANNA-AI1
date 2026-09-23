from chat.providers import ChatModelProvider, MockModelProvider


class ModelRouter:
    """
    Provider-independent model selection foundation.

    Only the deterministic mock provider is enabled at this stage.
    """

    def __init__(self):
        self._providers: dict[str, ChatModelProvider] = {
            "mock": MockModelProvider(),
        }

    def get_chat_provider(self, provider_name: str) -> ChatModelProvider:

        provider = self._providers.get(provider_name)

        if provider is None:
            raise ValueError(
                f"Unsupported chat provider: {provider_name}"
            )

        return provider
