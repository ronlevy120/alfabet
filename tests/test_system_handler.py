"""
Main Testing File for System Handler
"""
import os
import unittest

import yaml

os.environ['MNT_DIR'] = ""
os.environ["STAGE"] = "local"

with open("serverless.yml", "r") as stream:
    try:
        contents = yaml.load(stream, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        print(exc)

from src.system_handler import caller

os.environ['REQUIRED_PARAMS'] = contents['provider']['environment']['REQUIRED_PARAMS']
os.environ['HOST'] = contents['provider']['environment']['HOST']
os.environ['USERNAME'] = contents['provider']['environment']['USERNAME']
os.environ['PASSWORD'] = contents['provider']['environment']['PASSWORD']
os.environ['DB'] = contents['provider']['environment']['DB']
os.environ['SRC_BANK_ACCOUNT'] = contents['provider']['environment']['SRC_BANK_ACCOUNT']


class TestSystemHandler(unittest.TestCase):
    """
    Primary class for the test suite.
    Args:
        unittest ([unittest.TesCase]): [built-in unittest class]
    """

    def setUp(self):
        self.event = {"loan_id": "111", "amount": 100, 'dst_bank_account': 'discount'}

    def test_caller(self):
        """
        Testing the response from the collector method.
        The response should be a long dict. It should contain essential details
        (e.g., bathrooms and bathrooms).
        """

        output = caller(self.event, _context=None)
        print(output)
        self.assertTrue(isinstance(output, dict))


if __name__ == '__main__':
    unittest.main()
