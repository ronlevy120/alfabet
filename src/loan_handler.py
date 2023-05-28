"""
Loan Handler module
"""

from src.database import create_db_record
from datetime import datetime
from datetime import timedelta


class Loan:
    """
    Class to populate Loan table.
    """

    def __init__(self, total_loan_amount, borrower, loan_id):
        self.total_loan_amount = total_loan_amount
        self.borrower = borrower
        self.loan_id = loan_id

    def create_loan(self):
        create_db_record(table_name='loans',
                         table_fields=['total_loan_amount', 'borrower', 'loan_id'],
                         input_dict={'total_loan_amount': self.total_loan_amount, 'borrower': self.borrower,
                                     'loan_id': self.loan_id})

    def create_payment_plan(self):
        weekly_amount = self.total_loan_amount / 12
        input_dict = {'expected_amount': weekly_amount,
                      'loan_id': self.loan_id}
        table_fields = ['expected_amount', 'loan_id', 'payment_scheduled_to']
        for i in range(0, 12):
            new_payment_date = (datetime.today().date() + timedelta(weeks=i)).strftime('%Y-%V')
            input_dict['payment_scheduled_to'] = new_payment_date

            create_db_record(table_name='payments_plan',
                             table_fields=table_fields,
                             input_dict=input_dict)


def handler(event, context=None):
    loan = Loan(total_loan_amount=event.get('total_loan-amount'), borrower=event.get('borrower'),
                loan_id=event.get('loan_id'))
    loan.create_loan()
    loan.create_payment_plan()
