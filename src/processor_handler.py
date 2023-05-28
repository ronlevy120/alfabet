"""
Processor Handler module
"""

from src.database import create_db_record, get_status_table_data
import pandas as pd


class Processor:
    """
    Class to process transactions and download report on recent activity.
    """

    def __init__(self):
        pass

    def perform_transaction(self, src_bank_account, dst_bank_account, amount, direction):
        table_fields = ['src', 'dst', 'amount', 'direction']
        transactions_id = create_db_record(table_name='transactions',
                                           table_fields=table_fields,
                                           input_dict={'src': src_bank_account, 'dst': dst_bank_account,
                                                       'amount': amount,
                                                       'direction': direction})
        return transactions_id

    def download_report(self):
        report_raw = get_status_table_data(window=5)
        report = pd.DataFrame(report_raw).to_string(index=False)
        return report
