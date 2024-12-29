"""
Unit test file.
"""

import unittest

from advanced_askai.cli import cli
from advanced_askai.util import authenticaion_valid, get_authentication

IS_AUTHENTICATED = authenticaion_valid()


class InteractiveSessionTester(unittest.TestCase):
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
        cli()


if __name__ == "__main__":
    unittest.main()
