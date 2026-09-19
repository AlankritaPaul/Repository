"""Unit tests for chatbot internal structures and client configuration."""
import unittest
from unittest.mock import patch
import os
import sys

# Add directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestChatbotLogic(unittest.TestCase):

    def test_free_ai_mode_when_no_key(self):
        """Verify get_client_and_config falls back to free AI mode when no key is set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            import chatbot
            client, model, display = chatbot.get_client_and_config()
            self.assertEqual(model, "openai")
            self.assertIn("Free AI Cloud", display)

    def test_official_openai_mode_when_key_provided(self):
        """Verify get_client_and_config configures official OpenAI client when real key is set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test12345678"}):
            import chatbot
            client, model, display = chatbot.get_client_and_config()
            self.assertEqual(model, "gpt-4o-mini")
            self.assertIn("OpenAI (gpt-4o-mini)", display)


if __name__ == "__main__":
    unittest.main()
