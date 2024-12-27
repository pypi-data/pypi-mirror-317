import unittest
from unittest.mock import patch, MagicMock
import subprocess

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from PyDepManger import Manger

class TestManger(unittest.TestCase):
    @patch('subprocess.run')
    def test_blueprint(self, mock_subprocess_run):
        # Test for blueprint method with "java"
        Manger.java()
        mock_subprocess_run.assert_called_once_with(["./PyDepManger/bash/blueprint.sh", "java"])

        # Reset the mock for the next test
        mock_subprocess_run.reset_mock()

        # Test for blueprint method with "py"
        Manger.python()
        mock_subprocess_run.assert_called_once_with(["./PyDepManger/bash/blueprint.sh", "py"])

        # Reset the mock for the next test
        mock_subprocess_run.reset_mock()

        # Test for blueprint method with "data"
        try:
            Manger.data()
            mock_subprocess_run.assert_called_once_with(["./PyDepManger/bash/pacs.sh"])
        except AssertionError:
            raise AssertionError


if __name__ == '__main__':
    unittest.main()
