import json
import time

import pytest
import requests
from pytest_testrail.plugin import pytestrail
from mimesis.random import random
from resources.domain.tender import schema_tender_GPA, schema_tender
from datetime import datetime


@pytestrail.case('C23436')
def test_findAuctions_check_eAccess_returns_result_with_tender_electronicAuctions(execute_insert_into_access_tender,
                                                                                  prepared_cpid, prepared_tp_ocid,
                                                                                  prepared_token_entity,
                                                                                  prepared_owner, prepare_data,
                                                                                  payload_findAuctions,
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
    payload = payload_findAuctions(
        cpid=cpid,
        ocid=prepared_tp_ocid,
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "tender": {
            "electronicAuctions": data['tender']['electronicAuctions']
        }
    }

    # print(json.dumps(data))
    # print(json.dumps(payload))
    print(json.dumps(actualresult))
    print(json.dumps(response.success))
    assert actualresult == response.success


@pytestrail.case('C23437')
def test_findAuctions_check_eAccess_success_without_result_in_response(execute_insert_into_access_tender,
                                                                       prepared_cpid, prepared_tp_ocid,
                                                                       prepared_token_entity,
                                                                       prepared_owner, prepare_data,
                                                                       payload_findAuctions,
                                                                       host, port, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender_GPA, quantity=1)
    del data['tender']['electronicAuctions']
    data['ocid'] = cpid
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="TP",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_findAuctions(
        cpid=cpid,
        ocid=prepared_tp_ocid,
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(actualresult))
    # print(json.dumps(response.success))
    assert actualresult == response.success


@pytestrail.case('C23438')
def test_findAuctions_service_can_not_find_tender_by_cpid_cpid_does_not_present_into_DB(
        execute_insert_into_access_tender,
        prepared_cpid, prepared_tp_ocid,
        prepared_token_entity,
        prepared_owner, prepare_data,
        payload_findAuctions,
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

    def prepared_cpid_for_payload():
        cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
        return cp_id

    cpid_for_payload = prepared_cpid_for_payload()
    payload = payload_findAuctions(
        cpid=cpid_for_payload,
        ocid=prepared_tp_ocid
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR.COM-1.19.1/3",
        "description": f"Tender not found by cpid='{cpid_for_payload}' and ocid='{prepared_tp_ocid}'."

    }]

    # print(json.dumps(data))
    # print(json.dumps(payload))
    # print(json.dumps(actualresult))
    # print(json.dumps(response.error))
    assert actualresult == response.error

@pytest.mark.xfail(reason="eAccess does not search by ocid")
@pytestrail.case('C23439')
def test_findAuctions_service_can_not_find_tender_by_ocid_does_not_present_into_DB(
        execute_insert_into_access_tender,
        prepared_cpid, prepared_tp_ocid,
        prepared_token_entity,
        prepared_owner, prepare_data,
        payload_findAuctions,
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

    payload = payload_findAuctions(
        cpid=cpid,
        ocid=prepared_tp_ocid
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR.COM-1.19.1/3",
        "description": f"Tender not found by cpid='{cpid}' and ocid='{prepared_tp_ocid}'."

    }]

    # print(json.dumps(data))
    # print(json.dumps(payload))
    print(json.dumps(actualresult))
    print(json.dumps(response.error))
    assert actualresult == response.error

@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C23440'),
                                          id="del cpid"),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C23441'),
                                          id="del ocid")

                         ])
def test_checTenderState_without_attribute_in_params_object(prepared_cpid, payload_findAuctions, host, port,
                                                            response,
                                                            prepared_tp_ocid, param):
    payload = payload_findAuctions(
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
                                          marks=pytestrail.case('C23442'),
                                          id="cpid ==False"),
                             pytest.param("ocid", False, "DR-5/3", "Data mismatch to pattern: "
                                                                   "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-"
                                                                   "(AC|EI|EV|FS|NP|PN|TP)-[0-9]{13}$'. "
                                                                   "Actual value: 'false'.",
                                          marks=pytestrail.case('C23443'),
                                          id="ocid == False")


                         ])
def test_checTenderState_use_invalid_value_in_prarams(prepared_cpid, payload_findAuctions, host, port,
                                                      response, value, code, description,
                                                      prepared_tp_ocid, param):
    payload = payload_findAuctions(
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