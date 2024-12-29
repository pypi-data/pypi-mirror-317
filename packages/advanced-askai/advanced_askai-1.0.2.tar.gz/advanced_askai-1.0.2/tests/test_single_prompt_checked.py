"""
Unit test file.
"""

import subprocess
import unittest

from advanced_askai.util import authenticaion_valid

IS_AUTHENTICATED = authenticaion_valid()


class SingleCheckedPromptTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_cli(self) -> None:
        command = 'askai "Respond with HELLO" --check'
        output = subprocess.check_output(command, shell=True, text=True)
        self.assertIn("HELLO", output)

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_cli_advanced(self) -> None:
        command = 'askai "Respond with HELLO" --advanced --check'
        output = subprocess.check_output(command, shell=True, text=True)
        self.assertIn("HELLO", output)


if __name__ == "__main__":
    unittest.main()
