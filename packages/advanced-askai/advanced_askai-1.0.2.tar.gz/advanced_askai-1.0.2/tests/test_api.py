"""
Unit test file.
"""

import unittest

from advanced_askai.api import Chat, ChatBotConfig
from advanced_askai.constants import FAST_MODEL
from advanced_askai.util import authenticaion_valid, get_authentication

IS_AUTHENTICATED = authenticaion_valid()


class ApiTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_api(self) -> None:
        """Test command line interface (CLI)."""
        # rtn = os.system(COMMAND)
        # self.assertEqual(0, rtn)
        openai_key = get_authentication()
        assert openai_key is not None
        config = ChatBotConfig(
            model=FAST_MODEL,
            api_key=openai_key,
            ai_assistant_prompt="You are a helpful assistant that always returns 'EXPECTED-MESSAGE', and nothing else",
        )
        chat = Chat(config)
        response = chat.query("test-input")
        assert response == "EXPECTED-MESSAGE"


if __name__ == "__main__":
    unittest.main()
