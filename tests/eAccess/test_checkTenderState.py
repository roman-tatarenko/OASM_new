import json
import random
import time
from datetime import datetime
from resources.domain._ import _
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
    )
    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    print(json.dumps(data))
    print(json.dumps(payload))
    print(cpid)
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
    )

    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)

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
    )
    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.1/3",
        "description": f"Tender not found by cpid='{cpid}' and "
                       f"ocid='{prepared_tp_ocid}'."
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
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
    )
    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.2/3",
        "description": f"Tender with id='{data['tender']['id']}' has invalid states.",
        "details": [{
            "id": f"{data['tender']['id']}"
        }]
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
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
        ocid=prepared_tp_ocid
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR.COM-1.17.2/3",
        "description": f"Tender with id='{data['tender']['id']}' has invalid states.",
        "details": [{
            "id": f"{data['tender']['id']}"
        }]
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23071')
def test_checkTenderState_check_on_service_return_error_in_response_country_not_found(execute_insert_into_access_tender,
                                                                                      prepared_cpid,
                                                                                      prepare_data,
                                                                                      prepared_token_entity,
                                                                                      prepared_owner,
                                                                                      payload_checkTenderState, host,
                                                                                      port, response,
                                                                                      prepared_tp_ocid):
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
        ocid=prepared_tp_ocid
    )
    payload['params']['country'] = "DEDE"
    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR-17/3",
        "description": f"Tender states not found by country='{payload['params']['country']}' "
                       f"and pmd='{payload['params']['pmd']}' and "
                       f"operationType='{payload['params']['operationType']}'."
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23072')
def test_checkTenderState_check_on_service_return_error_in_response_pmd_not_found(execute_insert_into_access_tender,
                                                                                  prepared_cpid,
                                                                                  prepare_data,
                                                                                  prepared_token_entity,
                                                                                  prepared_owner,
                                                                                  payload_checkTenderState, host,
                                                                                  port, response,
                                                                                  prepared_tp_ocid):
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
        ocid=prepared_tp_ocid
    )
    payload['params']['pmd'] = "OT"
    if data['tender']['statusDetails'] == "qualification":
        payload['params']['operationType'] = _("random.schoice", seq=["qualification", "qualificationConsideration",
                                                                      "qualificationProtocol", ], end=1)
    elif data['tender']['statusDetails'] == "qualificationStandstill":
        payload['params']['operationType'] = _("random.schoice",
                                               seq=["applyQualificationProtocol", "withdrawQualificationProtocol",
                                                    "startSecondStage", ], end=1)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR-17/3",
        "description": f"Tender states not found by country='{payload['params']['country']}' "
                       f"and pmd='{payload['params']['pmd']}' and "
                       f"operationType='{payload['params']['operationType']}'."
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.xfail(reason=f"table settings (ocds.access_rules)  do not allow this test ")
@pytestrail.case('C23073')
def test_checkTenderState_check_on_service_return_error_in_response_operationType_not_found(
        execute_insert_into_access_tender,
        prepared_cpid,
        prepare_data,
        prepared_token_entity,
        prepared_owner,
        payload_checkTenderState, host,
        port, response,
        prepared_tp_ocid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    data['ocid'] = cpid
    data['tender']['statusDetails'] = "qualification"

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
        ocid=prepared_tp_ocid
    )
    payload['params']['operationType'] = "startSecondStage"

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "VR-17/3",
        "description": f"Tender states not found by country='{payload['params']['country']}' "
                       f"and pmd='{payload['params']['pmd']}' and "
                       f"operationType='{payload['params']['operationType']}'."
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23074')
def test_checkTenderState_error_in_response_if_use_invalid_operationType(execute_insert_into_access_tender,
                                                                         prepared_cpid,
                                                                         prepare_data, prepared_token_entity,
                                                                         prepared_owner,
                                                                         payload_checkTenderState, host, port, response,
                                                                         prepared_tp_ocid):
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
    )
    payload['params']['operationType'] = "quali"
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "DR-3/3",
        "description": f"Attribute value mismatch with one of enum expected values. "
                       f"Expected values: 'applyQualificationProtocol, qualification, qualificationConsideration, "
                       f"qualificationProtocol, startSecondStage, withdrawQualificationProtocol', actual value: 'quali'.",
        "details": [{
            "name": "operationType"
        }]
    }]
    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C23090'),
                                          id="del cpid"),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C23091'),
                                          id="del ocid"),
                             pytest.param("pmd",
                                          marks=pytestrail.case('C23092'),
                                          id="del pmd"),
                             pytest.param("country",
                                          marks=pytestrail.case('C23093'),
                                          id="del country"),
                             pytest.param("operationType",
                                          marks=pytestrail.case('C23094'),
                                          id="del operationId")
                         ])
def test_checTenderState_without_attribute_in_params_object(prepared_cpid, payload_checkTenderState, host, port,
                                                            response,
                                                            prepared_tp_ocid, param):
    payload = payload_checkTenderState(
        cpid=prepared_cpid,
        ocid=prepared_tp_ocid
    )

    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": "RQ-02/3",
        "description": "Can not parse 'params'."
    }]

    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(response.error))
    # print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.parametrize("param, value,code, description",
                         [
                             pytest.param("cpid", False, "DR-5/3", "Data mismatch to pattern: "
                                                                   "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                                                   "Actual value: 'false'.",
                                          marks=pytestrail.case('C23095'),
                                          id="cpid ==False"),
                             pytest.param("ocid", False, "DR-5/3", "Data mismatch to pattern: "
                                                                   "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-"
                                                                   "(AC|EI|EV|FS|NP|PN|TP)-[0-9]{13}$'. "
                                                                   "Actual value: 'false'.",
                                          marks=pytestrail.case('C23096'),
                                          id="ocid == False"),
                             pytest.param("pmd", 123, "DR-3/3", "Attribute value mismatch with one of enum expected "
                                                                "values. Expected values: 'MV, OT, RT, SV, DA, NP, FA, "
                                                                "OP, GPA, TEST_OT, TEST_SV, TEST_RT, TEST_MV, TEST_DA, "
                                                                "TEST_NP, TEST_FA, TEST_OP, TEST_GPA', "
                                                                "actual value: '123'.",
                                          marks=pytestrail.case('C23097'),
                                          id="del pmd == 123")

                         ])
def test_checTenderState_use_invalid_value_in_prarams(prepared_cpid, payload_checkTenderState, host, port,
                                                      response, value, code, description,
                                                      prepared_tp_ocid, param):
    payload = payload_checkTenderState(
        cpid=prepared_cpid,
        ocid=prepared_tp_ocid,
    )

    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [{
        "code": code,
        "description": description,
        "details": [{
            "name": param
        }]

    }]
    print(prepared_cpid)
    print(json.dumps(actualresult))
    assert actualresult == response.error
