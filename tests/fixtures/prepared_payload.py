import json

import pytest


@pytest.fixture(scope='session')
def payload_registered_document():
    def _payload_registered_document(file_name, hash, weight):
        return {
            "fileName": file_name,
            "hash": f"{hash}",
            "weight": weight
        }

    return _payload_registered_document


@pytest.fixture(scope='function')
def payload_check_registration(prepared_request_id):
    def _payload_check_registration(ids):
        return {
            "version": "2.0.0",
            "id": f"{prepared_request_id}",
            "action": "checkRegistration",
            "params": {
                "documentIds": ids
            }
        }

    return _payload_check_registration


@pytest.fixture(scope='function')
def payload_notice_compiled_release(request_template, data_for_test_notice_compiled_release):
    payload = request_template(action='updateRecord')

    def _payload_notice_compiled_release(data=data_for_test_notice_compiled_release, startDate="2020-04-02T09:14:25Z"):
        payload['params'] = {
            "date": startDate,
            "data": json.dumps(data)
        }

        return payload

    return _payload_notice_compiled_release


@pytest.fixture(scope='function')
def payload_openAccess(request_template):
    payload = request_template(action='openAccess')

    def _payload_openAccess(ids, datePublished):
        payload['params'] = {
            "documentIds": ids,
            "datePublished": datePublished
        }
        return payload

    return _payload_openAccess
