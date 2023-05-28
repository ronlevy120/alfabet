"""
Helpers module
"""

from datetime import datetime
import json


def create_api_response(report=None, error_message=None, success=True):
    """
    Create API response to the client.

    Args:
        report: [dict]
        error_message: [str] The receive error (if any)
        success:       [bool] Success API response or failure

    Returns:
            [dict] Response to client.

    """

    response = {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True, 'Content-Type': 'application/json'},
        'statusCode': 200 if success else error_message.get('status_code', 500)
    }

    metadata = {"timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}

    if success:
        response['body'] = json.dumps(
            {'report': report, 'metadata': metadata})

    else:

        response['body'] = json.dumps(
            {'error': error_message, 'metadata': metadata})

    return response
