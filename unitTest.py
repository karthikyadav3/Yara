import unittest
from argparse import Namespace
from report import *


class AppTest(unittest.TestCase):
    def test_github_connection(self):
        token = 'XYZ' # wrong token
        self.assertEqual(github_connection(token), False)

    def test_validate_arguments(self):
        args_parser = argparse.ArgumentParser()
        self.assertEqual(validate_arguments(args_parser), (False, Namespace(organization=None, token=None)))