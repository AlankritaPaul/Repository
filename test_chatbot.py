"""Unit tests for chatbot internal structures and command logic."""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestChatbotLogic(unittest.TestCase):

    def test_missing_api_key_exits(self):
        """Verify check_api_key exits when OPENAI_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock print and sys.exit
            with patch("sys.exit") as mock_exit, patch("builtins.print"):
                import chatbot
                chatbot.check_api_key()
                mock_exit.assert_called_with(1)

    def test_valid_api_key_returns(self):
        """Verify check_api_key returns key when set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test12345678"}):
            import chatbot
            key = chatbot.check_api_key()
            self.assertEqual(key, "sk-test12345678")


if __name__ == "__main__":
    unittest.main()
