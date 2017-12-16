import unittest
from gisrep.outputs.output_manager import Output, OutputManager


# Variable to validate output handled values
validate = {}


class TestOutputManager(unittest.TestCase):

    def setUp(self):
        # Create the output manager
        self.outputs = OutputManager()
        # Clear the state variables
        validate = {}

    def test_list(self):
        tag_list = self.outputs.list()

        # Assert tag list length
        self.assertTrue(len(tag_list) > 0)
        self.assertIn('stdout', tag_list)
        self.assertIn('file', tag_list)
        self.assertIn('clipboard', tag_list)

    def test_std_dump(self):
        report_string = "Hi!"

        # Pass the 'report' to the test output
        output = self.outputs.get_output(['test_std'])
        output.publish(report_string)

        # Assert that the report was handled
        self.assertEqual(TestStdOutput.validate['report'], report_string)
        self.assertNotIn('args', TestStdOutput.validate)

    def test_args_dump(self):
        report_string = "Yo!"
        output_args = ['second_arg']

        combined_args = ['test_args']
        combined_args.extend(output_args)
        # Pass the 'report' to the test output
        output = self.outputs.get_output(combined_args)
        output.publish(report_string)

        # Assert that the report was handled
        self.assertEqual(TestArgsOutput.validate['report'], report_string)
        self.assertEqual(TestArgsOutput.validate['args'].arg_a, output_args[0])

class TestStdOutput(Output):
    tag = "test_std"
    description = "Saves the report to a variable"
    validate = {}

    def dump(self, report, args=None):
        # Store the report
        self.validate['report'] = report

class TestArgsOutput(Output):
    tag = "test_args"
    description = "Saves the report to a variable, requires argument"
    validate = {}

    def configure_parser(self, parser):
        parser.add_argument(
            'arg_a',
            help="A fake argument for the output")
        return parser

    def dump(self, report, args=None):
        # Store the report
        self.validate['report'] = report
        self.validate['args'] = args
