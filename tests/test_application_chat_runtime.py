import unittest

import app
from chat.service import ChatService


class TestApplicationChatRuntime(unittest.TestCase):

    def test_create_chat_service_uses_configured_router(self):
        service = app.create_chat_service()

        self.assertIsInstance(service, ChatService)
        self.assertEqual(service.provider.provider_name, "mock")
        self.assertEqual(service.provider.model_name, "mock-foundation-v1")

    def test_main_can_process_chat_input(self):
        response = app.main("Hello Anna.")

        self.assertIsNotNone(response)
        self.assertEqual(response.provider, "mock")
        self.assertEqual(response.model, "mock-foundation-v1")
        self.assertIn("Hello Anna.", response.message.content)


if __name__ == "__main__":
    unittest.main()
