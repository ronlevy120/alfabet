"""
Create DB record module of the "Database Package".
"""

from datetime import date
from .setup import setup_connection


def create_db_record(table_name: str,
                     table_fields: list,
                     input_dict: dict) -> int:
    """
    Helper method used to insert the record to SQL table.

    Args:
        table_name   (str):  [Table Name to be inserted to]
        table_fields (list): [Table fields to be updated]
        input_dict   (dict): [Dictionary of the corresponding field-values]

    Returns:
        int: [The id of the record created]
    """

    conn = setup_connection()

    # Collect the values to the list:
    values = []
    for field in table_fields:
        value = input_dict.get(field)

        if value is None:
            values.append('NULL')
        elif isinstance(value, str):
            values.append(f'"{value}"')
        elif isinstance(value, date):
            values.append(f'"{str(value)}"')
        else:
            values.append(str(value))

    # Create the keys from the table fields:
    keys = ', '.join(table_fields)
    print(f"keys: {keys}")
    print(f"values: {values}")
    # Execute the SQL insert query:
    try:
        cursor = conn.cursor()
        query = f'''INSERT INTO {table_name} ({keys}) VALUES ({', '.join(values)})'''
        cursor.execute(query)
        print(f"Executing query: {query}")
        conn.commit()
        last_row_id = cursor.lastrowid
        cursor.close()
        conn.close()
    except Exception as exception:
        print("THIS IS THE EXCEPTION")
        print(exception)
        message = f'MYSQL {table_name} table insertion has failed'
        print(message)
        last_row_id = None

    return last_row_id
