"""
Main Testing File Loan Handler
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

from src.loan_handler import handler

os.environ['REQUIRED_PARAMS'] = contents['provider']['environment']['REQUIRED_PARAMS']
os.environ['HOST'] = contents['provider']['environment']['HOST']
os.environ['USERNAME'] = contents['provider']['environment']['USERNAME']
os.environ['PASSWORD'] = contents['provider']['environment']['PASSWORD']
os.environ['DB'] = contents['provider']['environment']['DB']


class TestLoanHandler(unittest.TestCase):
    """
    Primary class for the test suite.
    Args:
        unittest ([unittest.TesCase]): [built-in unittest class]
    """

    def setUp(self):
        self.event = {'total_loan-amount': 1200, 'borrower': "Ron",
                      'loan_id': 111}

    def test_handler(self):
        """
        Testing the response from the collector method.
        The response should be a long dict. It should contain essential details
        (e.g., bathrooms and bathrooms).
        """

        handler(self.event, context=None)


if __name__ == '__main__':
    unittest.main()
