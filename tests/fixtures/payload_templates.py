from collections import namedtuple

import pytest


@pytest.fixture(scope='function')
def request_template(prepared_request_id):
    def _with_value(action: str = None, params={}):
        return {
            "id": f"{prepared_request_id}",
            "version": "2.0.0",
            "action": action,
            "params": params
        }

    return _with_value


@pytest.fixture(scope='session')
def response_template():
    return {
        "version": "2.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "str"
    }


@pytest.fixture(scope='function')
def response(response_template, prepared_request_id):
    response_template['id'] = f"{prepared_request_id}"
    response_success = response_template.copy()
    response_success['status'] = "success"
    response_error = response_template.copy()
    response_error['status'] = "error"
    return namedtuple('response', ['success', 'error'], defaults=[response_success, response_error])()
