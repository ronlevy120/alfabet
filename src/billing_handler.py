"""
Billing handler module
"""

import os

from src.processor_handler import Processor


class Billing:
    """
    Class to orchestrate transactions.
    """

    def __init__(self):
        self.src_bank_account = os.environ['SRC_BANK_ACCOUNT']
        self.direction = "credit"
        self.processor = Processor()

    def perform_advance(self, amount, dst_bank_account):
        transactions_id = self.processor.perform_transaction(src_bank_account=self.src_bank_account,
                                                             dst_bank_account=dst_bank_account,
                                                             amount=amount,
                                                             direction=self.direction)
        report = self.processor.download_report()
        advance_result = {'report': report, 'transactions_id': transactions_id}

        return advance_result
