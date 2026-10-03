import unittest

from config.chat_settings import ChatSettings
from core.model_router import ModelRouter


class TestChatRoutingConfiguration(unittest.TestCase):

    def test_router_uses_configured_provider(self):
        settings = ChatSettings(
            provider="mock",
            model="configured-test-model",
        )

        router = ModelRouter(settings=settings)

        provider = router.get_chat_provider()

        self.assertEqual(provider.provider_name, "mock")

    def test_router_can_still_select_provider_explicitly(self):
        settings = ChatSettings(
            provider="mock",
            model="configured-test-model",
        )

        router = ModelRouter(settings=settings)

        provider = router.get_chat_provider("mock")

        self.assertEqual(provider.provider_name, "mock")

    def test_unsupported_configured_provider_is_rejected(self):
        settings = ChatSettings(
            provider="unsupported-provider",
            model="configured-test-model",
        )

        router = ModelRouter(settings=settings)

        with self.assertRaises(ValueError):
            router.get_chat_provider()


if __name__ == "__main__":
    unittest.main()
