import unittest
from output_manager import OutputManager
import io
import sys


class TestOutputManager(unittest.TestCase):

    def setUp(self):
        self.outputs = OutputManager()

    def test_list(self):
        tag_list = self.outputs.list()

        # Assert tag list length
        self.assertTrue(len(tag_list) > 0)
        for tag in tag_list:
            print(tag)

    def test_stdout_dump(self):
        # TODO: Redirect stdout
        self.outputs.dump('stdout', "Hi!")
