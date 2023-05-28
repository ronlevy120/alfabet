"""
Setup module of the "Database Package".
"""

import os
import sys

sys.path.append(f"{os.environ['MNT_DIR']}")

import pymysql


def setup_connection():
    """
    Helper function used to setup a connection to the relevant DB.
    """

    try:
        conn = pymysql.connect(host=os.environ['HOST'],
                               user=os.environ['USERNAME'],
                               passwd=os.environ['PASSWORD'],
                               database=os.environ['DB'])

        return conn

    except Exception as exception:
        print(exception)
        message = 'Pymysql connection has failed'
        print(message)
        return None
