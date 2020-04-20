import json
from dataclasses import dataclass

import pytest


@pytest.fixture(scope='function')
def responses(prepared_request_id):
    @dataclass()
    class Responses:
        version = '0.0.1'
        ok = {'id': f'{prepared_request_id}', 'data': {}, 'version': version}
        errors = {'id': f'{prepared_request_id}', 'errors': [], 'version': version}

    return Responses


@pytest.fixture(scope='function')
def prepared_payload(prepared_request_id, prepared_operation_id):
    def with_values(command, cpid=None, stage="EV", operationid=prepared_operation_id, id=None, token=None,
                    owner='445f6851-c908-407d-9b45-14b92f3e964b'):
        return {
            "id": f"{prepared_request_id}",
            "command": command,
            "context": {
                "operationId": f"{operationid}",
                "requestId": "7eb32550-2335-11ea-7a78-e9a0e1c3d51d",
                "cpid": cpid,
                "ocid": "ocds-t1s2t3-MD-1576850865434-EV-1576850873109",
                "stage": stage,
                "prevStage": "EV",
                "processType": "startConsiderByAward",
                "operationType": "doAwardConsideration",
                "phase": "awarding",
                "owner": f"{owner}",
                "country": "MD",
                "language": "ro",
                "pmd": "TEST_OT",
                "token": f'{token}',
                "startDate": "2019-12-20T14:32:05Z",
                "id": f"{id}",
                "timeStamp": 1576852325413,
                "isAuction": False
            },
            "data": {},
            "version": "0.0.1"
        }

    return with_values

@pytest.fixture(scope='function')
def prepared_payload_findLotIds(prepared_request_id, prepared_cpid, prepared_ev_ocid):
    return {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "findLotIds",
        "params": {
            "states": [
                {
                    "status": "active",
                    "statusDetails": "empty"
                }
            ],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }


@pytest.fixture(scope='function')
def prepared_payload_checkAccessToTender(prepared_request_id, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
                                         prepared_owner):
    return {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "checkAccessToTender",
        "params": {
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}",
            "token": f"{prepared_token_entity}",
            "owner": f"{prepared_owner}"
        }
    }


@pytest.fixture(scope='function')
def prepared_payload_getLotStateByIds(prepared_request_id, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
                                      prepared_owner):
    def _prepared_payload_getLotStateByIds(lot_id=prepared_token_entity):
        return {
            "version": "2.0.0",
            "id": f"{prepared_request_id}",
            "action": "getLotStateByIds",
            "params": {
                "lotIds": [
                    f"{lot_id}"
                ],
                "cpid": f"{prepared_cpid}",
                "ocid": f"{prepared_ev_ocid}"
            }
        }

    return _prepared_payload_getLotStateByIds


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
    payload = request_template(acton='updateRecord')

    def _payload_notice_compiled_release(data=data_for_test_notice_compiled_release, startDate="2020-04-02T09:14:25Z"):
        payload['params'] = {
            "date": startDate,
            "data": json.dumps(data)
        }

        return payload

    return _payload_notice_compiled_release


@pytest.fixture(scope='function')
def payload_openAccess(request_template):
    payload = request_template(acton='openAccess')

    def _payload_openAccess(ids, datePublished):
        payload['params'] = {
            "documentIds": ids,
            "datePublished": datePublished
        }
        return payload

    return _payload_openAccess


@pytest.fixture(scope='function')
def payload_checkRelatedTenderer(request_template):
    payload = request_template(acton='checkRelatedTenderer')

    def _payload_checkRelatedTenderer(cpid, ocid, awadId, requirmentId, relatedTendererId):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "awardId": awadId,
            "requirementId": requirmentId,
            "relatedTendererId": relatedTendererId
        }
        return payload

    return _payload_checkRelatedTenderer


@pytest.fixture(scope='function')
def payload_checkPersonesStructure(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(acton='checkPersonesStructure')

    def _payload_checkPersonesStructure(persones, cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                        locationOfPersones="award"):
        payload['params'] = {
            "persones": persones,
            "cpid": cpid,
            "ocid": ocid,
            "locationOfPersones": locationOfPersones
        }
        return payload

    return _payload_checkPersonesStructure



