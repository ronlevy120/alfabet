"""
System Handler module
"""

import os
import json
from datetime import timedelta
from datetime import datetime
import pandas as pd

from src.billing_handler import Billing
from src.helpers import *
from src.database import get_record_by_loan_id_and_week, get_last_payment_date, create_db_record


def caller(event: dict, _context: None) -> dict:
    """
    Entry point and the handler of the Billing system.
    Args:
        event: [dict] event with data

        Example event:
        {"loan_id": "111", "amount": 100, 'dst_bank_account': 'discount'}

        _context: NOT USED.

    Returns: [dict] API output
    """
    event_body = json.loads(event['body']) if event.get('body') else event
    print(f'Request fields body is {event_body}')
    driver_result = driver(event_body=event_body)

    if driver_result.get('error'):
        return create_api_response(error_message=driver_result['error'],
                                   success=False)

    try:
        report = runner(event_body)
    except Exception as exception:
        print(exception)
        error_ie01 = {
            "code": "IE01",
            "status_code": 500,
            "category": "Internal Server Error",
            "description": f"An exception occurred when attempting"
                           f" to process your request: {str(exception)}",
        }

        return create_api_response(error_message=error_ie01,
                                   success=False)

    driver_out = create_api_response(report=report)

    print("Transactions report from the recent 5 days:")
    print(report)

    return driver_out


def driver(event_body: dict) -> dict:
    """
    Checking the validity of the input fields.

    Args:
        event_body: [dict] event with data

    Returns: [dict] dictionary with indication regarding the input validity
    """

    # Error RE01 check - all keys exists?
    event_body_params = set([f.strip() for f in event_body.keys()])
    required_params_types_list = [obj.split(",") for obj in
                                  [param_and_type for param_and_type in os.environ[
                                      'REQUIRED_PARAMS'].split("|")]]
    required_params_types = {obj[0].strip(): obj[1].strip() for obj in required_params_types_list}
    required_params = set(required_params_types.keys())

    missing_params = required_params - event_body_params
    if missing_params:
        error = {
            "code": "RE01",
            "status_code": 400,
            "category": "Request Error",
            "description": f"The given parameter(s) were not enough"
                           f" to fulfill the request: {' ,'.join(event_body_params)}."
                           f" missing: {' ,'.join(missing_params)}"
        }

        return {"status": "failed", "error": error}

    # Error RE02 check - correct type?
    error = {
        "code": "RE02",
        "status_code": 400,
        "category": "Request Error",
    }

    # Checking that all fields are strings before continuing

    types_dict = {"string": str, "integer": int, "float": float}

    for param, param_type in required_params_types.items():
        event_field = event_body[param]
        expected_type = types_dict[param_type]
        # noinspection PyTypeHints
        if not isinstance(event_field, expected_type): # Ignoring Pycharm inspection
            rule = f'Must be a {param_type}'
            error['description'] = f"The {param} parameter violates the rule: {rule}"
            return {"status": "failed", "error": error}

    # Strip parameters
    for field in event_body:
        if isinstance(event_body[field], str):
            event_body[field] = event_body[field].strip()

    error = {
        "code": "RE03",
        "status_code": 400,
        "category": "Request Error",
    }

    # Error RE03 check - correct length?
    for field in required_params:
        event_field = event_body[field]

        # try-and-except, in case field length is not defined
        try:
            field_length = int(os.environ[f'{field.upper()}_LENGTH'])
        except KeyError:
            continue

        if not len(event_field) >= field_length:
            rule = f'{field} Length must be greater than or equal to {field_length}'
            error['description'] = f"The {field} parameter violates the rule: {rule}"
            return {"status": "failed", "error": error}

    return {"status": "success", "error": None}


def runner(event_body: dict) -> str:
    """
    Running the functionality for the "System Handler".
    Args:
        event_body: [dict] event with data

    Returns: [str] output to the client

    """
    amount = event_body['amount']
    billing = Billing()
    advance_result = billing.perform_advance(
        amount=amount, dst_bank_account=event_body["dst_bank_account"])

    if not advance_result.get('transactions_id'):
        last_payment_record = get_last_payment_date(loan_id=event_body['loan_id'])
        last_payment_date = datetime.strptime(last_payment_record[0]['payment_schedule_to'],
                                              "%Y-%m")
        new_payment_to_append = last_payment_date + timedelta(weeks=1)

        payments_plan_table_fields = ['payment_schedule_to', 'amount', 'loan_id']
        create_db_record(table_name="payments_plan",
                         table_fields=payments_plan_table_fields,
                         input_dict={'payment_schedule_to': new_payment_to_append, 'amount': amount,
                                     'loan_id': event_body['loan_id']})

    week = datetime.today().date().strftime('%Y-%V')
    payments_plan_record = get_record_by_loan_id_and_week(loan_id=event_body['loan_id'],
                                                          week=week,
                                                          table_name='payments_plan')
    payment_id = payments_plan_record[0]['id']
    status_table_fields = ["transaction_id", "payment_id", "transaction_status"]
    status_input_dict = {"transaction_id": advance_result.get('transactions_id'),
                         "payment_id": payment_id,
                         "transaction_status": True if advance_result.get(
                             'transactions_id') else False}

    create_db_record(table_name="status",
                     table_fields=status_table_fields,
                     input_dict=status_input_dict)

    return advance_result.get(
        'report',
        pd.DataFrame(columns=['transaction_id', 'transaction_status']).to_string(index=False))
