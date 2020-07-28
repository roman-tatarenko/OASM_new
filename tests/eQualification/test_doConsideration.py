import json
import time
from random import random
from uuid import uuid4

import pytest
import requests

from pytest_testrail.plugin import pytestrail


@pytestrail.case('C23058')
def test_doConsideration_do_qualification_consideration(execute_insert_into_qualifications, prepared_cpid,
                                                        prepared_tp_ocid, data_qualification, payload_doConsideration,
                                                        response, host, port):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_doConsideration(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id
    )
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    print(json.dumps(data))
    print(json.dumps(payload))
    response.success['result'] = {
        "qualifications": [{
            "id": qualification_id,
            "statusDetails": "consideration"
        }]
    }
    assert actualresult == response.success


@pytestrail.case('C23059')
def test_doConsideration_check_data_has_changed_in_the_DB(execute_insert_into_qualifications, prepared_cpid,
                                                          prepared_tp_ocid, data_qualification, payload_doConsideration,
                                                          response, host, port, execute_select_qualifications_by_cpid):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    data['statusDetails'] = "awaiting"
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_doConsideration(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id
    )
    response.success['result'] = {
        "qualifications": [{
            "id": qualification_id,
            "statusDetails": "consideration"
        }]
    }
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    assert actualresult == response.success
    record = execute_select_qualifications_by_cpid(
        cpid=cpid
    ).one()
    json_data = json.loads(record.json_data)
    print(cpid)
    assert json_data['statusDetails'] == "consideration"


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-1599999999999",
                                          marks=pytestrail.case('C23077'),
                                          id="cpid does not exist in the DB"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-1599999999999-TP-1599999999999",
                                          marks=pytestrail.case('C23078'),
                                          id="ocid does not exist in the DB")

                         ])
def test_doConsideration_cpid_ocid_does_not_exist_in_the_DB(execute_insert_into_qualifications, prepared_cpid,
                                                            prepared_tp_ocid, data_qualification,
                                                            payload_doConsideration,
                                                            response, host, port, execute_select_qualifications_by_cpid,
                                                            param, value):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    data['statusDetails'] = "awaiting"
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )

    payload = payload_doConsideration(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id
    )
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['cpid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.21.1/22",
            "description": f"Qualification not found by cpid='{value}' and "
                           f"ocid='{ocid}' and "
                           f"id='{qualification_id}'."

        }]
    elif payload['params']['ocid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.21.1/22",
            "description": f"Qualification not found by cpid='{cpid}' and "
                           f"ocid='{value}' and "
                           f"id='{qualification_id}'."

        }]
    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23079')
def test_doConsideration_qualifications_id_does_not_exist_in_the_DB(execute_insert_into_qualifications, prepared_cpid,
                                                                    prepared_tp_ocid, data_qualification,
                                                                    payload_doConsideration,
                                                                    response, host, port,
                                                                    execute_select_qualifications_by_cpid,
                                                                    ):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    data['statusDetails'] = "awaiting"
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_doConsideration(
        cpid=cpid,
        ocid=ocid,
        id=str(uuid4())
    )
    actualresul = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR.COM-7.21.1/22",
        "description": f"Qualification not found by cpid='{cpid}' and "
                       f"ocid='{ocid}' and "
                       f"id='{uuid4()}'."

    }]
    print(uuid4())
    assert actualresul == response.error

# @pytestrail.case('C23067')
# def test_doConsideration_empty_qualifications_array(payload_doConsideration):
#     payload = payload_doConsideration()
#     payload['params']['qualifications']=[]
#     response.error['']