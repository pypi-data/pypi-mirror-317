"""
Unit test file.
"""

import io
import sys
import unittest
from unittest.mock import patch

from advanced_askai.cli import cli
from advanced_askai.util import authenticaion_valid

IS_AUTHENTICATED = authenticaion_valid()


class SinglePromptTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_single_shot(self) -> None:
        """Test command line interface (CLI)."""
        sys.argv.append("Respond with HELLO")
        try:
            rtn = cli()
        finally:
            sys.argv.pop()
        self.assertEqual(0, rtn)

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    @patch("sys.stdin", io.StringIO("exit\n"))
    def test_interactive(self) -> None:
        """Test command line interface (CLI)."""
        rtn = cli()
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
