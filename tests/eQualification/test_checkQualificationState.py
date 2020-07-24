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


@pytestrail.case('C23098')
def test_checkQualificationState_check_on_service_return_success_in_response(execute_insert_into_qualifications,
                                                                             prepared_cpid, prepared_tp_ocid,
                                                                             data_qualification,
                                                                             payload_checkQualificationState, host,
                                                                             port, response):
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

    payload = payload_checkQualificationState(
        cpid=cpid,
        ocid=ocid,
        operationType="qualificationConsideration",
        qualificationId=qualification_id

    )

    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("qualificationId", "99999a99-9999-99b9-b999-9a99b99e9a99",
                                          marks=pytestrail.case('C23099'),
                                          id="qualificationId does not present into DB"),

                             pytest.param("cpid", "ocds-t1s2t3-MD-1599999999999",
                                          marks=pytestrail.case('C23100'),
                                          id="cpid does not present into DB"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-1599999999999-TP-1599999999999",
                                          marks=pytestrail.case('C23101'),
                                          id="ocid does not present into DB")
                         ])
def test_checkQualificationState_check_on_service_return_error_in_response(execute_insert_into_qualifications,
                                                                           prepared_cpid, prepared_tp_ocid,
                                                                           prepared_owner, prepared_token_entity,
                                                                           data_qualification,
                                                                           payload_checkQualificationState, param,
                                                                           value, response, host, port):
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

    payload = payload_checkQualificationState(
        cpid=cpid,
        ocid=ocid,
        qualificationId=qualification_id,
        operationType="qualificationConsideration"
    )
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['cpid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.17.1/22",
            "description": f"Qualification not found by cpid='{value}' and ocid='{ocid}' and id='{qualification_id}'."
        }]
    elif payload['params']['ocid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.17.1/22",
            "description": f"Qualification not found by cpid='{cpid}' and ocid='{value}' and id='{qualification_id}'."
        }]
    elif payload['params']['qualificationId'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.17.1/22",
            "description": f"Qualification not found by cpid='{cpid}' and ocid='{ocid}' and id='{value}'."
        }]


    assert actualresult == response.error


@pytestrail.case('C23106')
def test_checkQualificationState_service_return_error_if_qualification_status_does_not_match_the_service_settings(
        execute_insert_into_qualifications,
        prepared_cpid, prepared_tp_ocid,
        prepared_owner, prepared_token_entity,
        data_qualification,
        payload_checkQualificationState,
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
    data['status'] = "unsuccessful"
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_checkQualificationState(
        cpid=cpid,
        ocid=ocid,
        qualificationId=qualification_id,
        operationType="qualificationConsideration"
    )

    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR.COM-7.17.2/22",
        "description": f"Qualification with id='{qualification_id}' has invalid states."
    }]

    assert actualresult == response.error


@pytestrail.case('C23107')
def test_checkQualificationState_service_return_error_if_qualification_statusDetails_does_not_match_the_service_settings(
        execute_insert_into_qualifications,
        prepared_cpid, prepared_tp_ocid,
        prepared_owner, prepared_token_entity,
        data_qualification,
        payload_checkQualificationState,
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
    data['statusDetails'] = "consideration"
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_checkQualificationState(
        cpid=cpid,
        ocid=ocid,
        qualificationId=qualification_id,
        operationType="qualificationConsideration"
    )

    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR.COM-7.17.2/22",
        "description": f"Qualification with id='{qualification_id}' has invalid states."
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("country", "USA",
                                          marks=pytestrail.case('C23102'),
                                          id="country does not present in DB"),

                             pytest.param("pmd", "OT",
                                          marks=pytestrail.case('C23103'),
                                          id="pmd does not present in DB"),

                             pytest.param("operationType", "quan",
                                          marks=pytestrail.case('C23105'),
                                          id="mismatch of 'operationType' with one of enum expected values")
                         ])
def test_checkQualificationState_check_on_service_return_error_in_response(execute_insert_into_qualifications,
                                                                           prepared_cpid, prepared_tp_ocid,
                                                                           prepared_owner, prepared_token_entity,
                                                                           data_qualification,
                                                                           payload_checkQualificationState,
                                                                           response, host, port, param, value):
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

    payload = payload_checkQualificationState(
        cpid=cpid,
        ocid=ocid,

        qualificationId=qualification_id,
        operationType="qualificationConsideration"
    )
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['country'] == value:
        response.error['result'] = [{
            "code": "VR.COM-17/22",
            "description": f"Qualification states not found by country='{value}' and pmd='{payload['params']['pmd']}' "
                           f"and operationType='qualificationConsideration'.",

        }]
    elif payload['params']['pmd'] == value:
        response.error['result'] = [{
            "code": "DR-3/22",
            "description": f"Attribute value mismatch of 'pmd' with one of enum expected values. "
                           f"Expected values: 'GPA, TEST_GPA', actual value: '{value}'.",
            "details": [{
                "name": param
            }]
        }]
    elif payload['params']['operationType'] == value:
        response.error['result'] = [{
            "code": "DR-3/22",
            "description": f"Attribute value mismatch of 'operationType' with one of enum expected values. "
                           f"Expected values: 'qualificationDeclareNonConflictOfInterest, qualification, "
                           f"qualificationConsideration', actual value: '{value}'.",
            "details": [{
                "name": param
            }]

        }]


    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C23108'),
                                          id="del cpid from payload"),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C23109'),
                                          id="del ocid from payload"),

                             pytest.param("country",
                                          marks=pytestrail.case('C23110'),
                                          id="del country from payload"),

                             pytest.param("pmd",
                                          marks=pytestrail.case('C23111'),
                                          id="del pmd from payload"),

                             pytest.param("operationType",
                                          marks=pytestrail.case('C23112'),
                                          id="del operationType from payload"),

                             pytest.param("qualificationId",
                                          marks=pytestrail.case('C23113'),
                                          id="del qualificationId from payload")
                         ])
def test_checkQualificationState_without_attribute_in_params_object(payload_checkQualificationState, prepared_cpid,
                                                                    prepared_tp_ocid, param, host, port, response):
    payload = payload_checkQualificationState(
        cpid=prepared_cpid,
        ocid=prepared_tp_ocid,
        qualificationId=str(uuid4()),
        operationType="qualificationConsideration"
    )
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-1/22",
        "description": "Error parsing 'params'"
    }]


    assert actualresult == response.error
