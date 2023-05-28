"""
Get DB record module of the "Database Package".
"""

import datetime
from typing import List

from .setup import setup_connection


def execute_query(cursor,
                  query: str) -> List:
    """
    Method used to execute query and retrieve results from SQL

    Args:
        cursor (SQL cursor): [SQL Connection cursor]
        query  (str): [description]

    Returns:
        [List]: [List of records from the executed SQL Query]
    """

    print(f"Executing query: {query}")
    cursor.execute(query)

    column_names = cursor.description
    rows = cursor.fetchall()

    result = []
    if len(rows) > 0:
        for row in rows:
            tmp = {}
            for (column_index, column_value) in enumerate(row):
                column_name = column_names[column_index][0]

                # Cast datetime to string so it can be easily serialized after:
                if isinstance(column_value, datetime.datetime):
                    column_value = str(column_value)

                tmp[column_name] = column_value
            result.append(tmp)

    return result


def get_record_by_loan_id_and_week(loan_id: int,
                                   week: str,
                                   table_name: str) -> List:
    """
    Method used to pull record from Alfabet DB, using the loan_id column and the week
    as the key for the query.

    Args:
        loan_id (int): [Identifier for the loan]
        week     (str): [Payment week]
        table_name  (str): [Table Name to be pulled from]

    Returns:
        [List]: [List of records, identified by ID]
    """

    conn = setup_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name} WHERE loan_id={loan_id} and payment_scheduled_to='{week}';"

    try:
        result = execute_query(cursor, query)
    except Exception as exception:
        print(exception)
        message = f'MYSQL {table_name} table selection has failed'
        print(message)
        result = []

    cursor.close()
    conn.close()
    return result


def get_last_payment_date(loan_id: int) -> List:
    """
    Method used to pull the latest payment_schedule_to from payments_pan table.

    Args:
        loan_id (int): [Identifier for the loan]

    Returns:
        [List]: [List of records, identified by ID]
    """

    conn = setup_connection()
    cursor = conn.cursor()

    query = f"SELECT payment_schedule_to FROM payments_plan WHERE loan_id={loan_id} order by payment_schedule_to DSC " \
            f"LIMIT 1;"

    try:
        result = execute_query(cursor, query)
    except Exception as exception:
        print(exception)
        message = f'MYSQL `payment_schedule_to` table selection has failed'
        print(message)
        result = []

    cursor.close()
    conn.close()
    return result


def get_status_table_data(window: int = 5) -> List:
    """
    Method used to pull data from the recent days in status table/

    Args:
        window (int): [Number pf days back to pull data from]

    Returns:
        [List]: [List of records, identified by ID]
    """

    conn = setup_connection()
    cursor = conn.cursor()

    query = f"SELECT transaction_id, transaction_status FROM" \
            f" status WHERE transaction_timestamp BETWEEN DATE_SUB(NOW(), INTERVAL {window} DAY) AND NOW();"

    try:
        result = execute_query(cursor, query)
    except Exception as exception:
        print(exception)
        message = f'MYSQL report selection has failed'
        print(message)
        result = []

    cursor.close()
    conn.close()
    return result
