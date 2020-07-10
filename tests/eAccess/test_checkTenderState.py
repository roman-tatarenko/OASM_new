import copy
import json
import random
import time
from datetime import datetime
from uuid import uuid4

import pytest
import requests
from mimesis.random import random
from pytest_testrail.plugin import pytestrail

from resources.domain.tender import schema_tender_GPA


@pytestrail.case('C23068')
def test_checkTenderState_check_on_service_return_success_in_response_without_result(execute_insert_into_access_tender,
                                                                                     prepared_cpid, prepared_tp_ocid,
                                                                                     prepared_token_entity,
                                                                                     prepared_owner, prepare_data,
                                                                                     payload_checkTenderState,
                                                                                     host, port, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_checkTenderState(
        cpid=cpid,
        ocid=prepared_tp_ocid,
        operationType="qualificationConsideration"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    print(json.dumps(data))
    print(json.dumps(payload))
    assert actualresult == response.success


@pytestrail.case('C23069')
def test_checkTenderState_service_can_not_find_tender_by_cpid(execute_insert_into_access_tender, prepared_cpid,
                                                              prepare_data, prepared_token_entity, prepared_owner,
                                                              payload_checkTenderState,
                                                              prepared_tp_ocid, host, port, response):
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    def prepared_cpid_for_payload():
        cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
        return cp_id

    cpid_for_payload = prepared_cpid_for_payload()
    payload = payload_checkTenderState(
        cpid=cpid_for_payload,
        ocid=ocid,
        operationType="qualificationConsideration"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.1/3",
        "description": f"Tender not found by cpid='{cpid_for_payload}' and "
                       f"ocid='{ocid}'."
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(actualresult))
    # print(json.dumps(response.error))
    assert actualresult == response.error


@pytest.mark.xfail(reason="eAccess does not search by ocid")
@pytestrail.case('C23070')
def test_checkTenderState_service_can_not_find_tender_by_ocid(execute_insert_into_access_tender, prepared_cpid,
                                                              prepare_data, prepared_token_entity, prepared_owner,
                                                              prepared_tp_ocid, response, host, port,
                                                              payload_checkTenderState):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_checkTenderState(
        cpid=cpid,
        ocid=prepared_tp_ocid,
        operationType="qualificationConsideration"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.1/3",
        "description": f"Tender not found by cpid='{cpid}' and "
                       f"ocid='{prepared_tp_ocid}'."
    }]
    print(json.dumps(data))
    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23075')
def test_checkTenderState_use_incorrect_status(execute_insert_into_access_tender, prepared_cpid,
                                               prepare_data, prepared_token_entity,
                                               prepared_owner,
                                               payload_checkTenderState, host, port, response,
                                               prepared_tp_ocid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid
    data['tender']['status'] = "planning"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_checkTenderState(
        cpid=cpid,
        ocid=prepared_tp_ocid,
        operationType="qualificationConsideration"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.2/3",
        "description": f"Tender with id='{data['tender']['id']}' has invalid states.",
        "details": [{
            "id": f"{data['tender']['id']}"
        }]
    }]
    print(json.dumps(data))
    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23076')
def test_checkTenderState_use_incorrect_statusDetails(execute_insert_into_access_tender, prepared_cpid,
                                                      prepare_data, prepared_token_entity,
                                                      prepared_owner,
                                                      payload_checkTenderState, host, port, response,
                                                      prepared_tp_ocid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid
    data['tender']['statusDetails'] = "empty"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_checkTenderState(
        cpid=cpid,
        ocid=prepared_tp_ocid,
        operationType="qualificationConsideration"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.2/3",
        "description": f"Tender with id='{data['tender']['id']}' has invalid states.",
        "details": [{
            "id": f"{data['tender']['id']}"
        }]
    }]
    print(json.dumps(data))
    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.parametrize("param, value, description",
                         [
                             pytest.param("country", "DE", f"Tender states not found by country='DE' "
                                                           f"and pmd='GPA' and "
                                                           f"operationType='qualificationConsideration'.",
                                          marks=pytestrail.case('C23071'),
                                          id="country does not present in DB"),

                             pytest.param("pmd", "OT", f"Tender states not found by country='MD' and "
                                                       f"pmd='OT' and operationType='qualificationConsideration'.",
                                          marks=pytestrail.case('C23072'),
                                          id="pmd does not present in DB"),

                             pytest.param("operationType", "qualification", f"Tender states not found by country='MD' "
                                                                            f"and pmd='GPA' and"
                                                                            f" operationType='qualification'.",
                                          marks=pytestrail.case('C23073'),
                                          id="operationType does not present in DB")

                         ])
def test_checkTenderState_check_on_service_return_error_in_response(execute_insert_into_access_tender, prepared_cpid,
                                                                    prepare_data, prepared_token_entity, prepared_owner,
                                                                    prepared_tp_ocid, response, host, port,
                                                                    payload_checkTenderState, param, value,
                                                                    description):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_checkTenderState(
        cpid=cpid,
        ocid=prepared_tp_ocid,
        operationType="qualificationConsideration"
    )
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR-17/3",
        "description": description
    }]
    print(json.dumps(data))
    print(json.dumps(actualresult))
    assert actualresult == response.error

# @pytestrail.case('C23074')
# def test_checkTenderState_check_on_service_return error in response if use invalid operationType(execute_insert_into_access_tender, prepared_cpid,
#                                                       prepare_data, prepared_token_entity,
#                                                       prepared_owner,
#                                                       payload_checkTenderState, host, port, response,
#                                                       prepared_tp_ocid):
#     cpid = prepared_cpid
#     data = prepare_data(schema=schema_tender_GPA, quantity=1)
#     data['ocid'] = cpid
#     data['tender']['statusDetails'] = "empty"
#
#     execute_insert_into_access_tender(
#         cp_id=cpid,
#         stage="TP",
#         token_entity=prepared_token_entity,
#         created_date=datetime.now(),
#         json_data=data,
#         owner=prepared_owner
#     )
#
#     payload = payload_checkTenderState(
#         cpid=cpid,
#         ocid=prepared_tp_ocid,
#         operationType="qualificationConsideration"
#     )
#     actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
#
#     response.error['result'] = [{
#         "code": "VR.COM-1.17.2/3",
#         "description": f"Tender with id='{data['tender']['id']}' has invalid states.",
#         "details": [{
#             "id": f"{data['tender']['id']}"
#         }]
#     }]
#     print(json.dumps(data))
#     print(json.dumps(actualresult))
#     assert actualresult == response.error