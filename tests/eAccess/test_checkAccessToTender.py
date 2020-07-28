from datetime import datetime
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8404')
def test_eAccess_returns_successful_response_when_token_and_owner_are_present_in_the_DB(port, host, prepared_cpid,
                                                                                        prepared_token_entity,
                                                                                        prepared_owner, response,
                                                                                        data_tender,
                                                                                        payload_checkAccessToTender,
                                                                                        execute_insert_into_access_tender
                                                                                        ):
    data = data_tender
    data['ocid'] = prepared_cpid
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_checkAccessToTender()
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value,code",
                         [
                             pytest.param("owner", f"{uuid4()}", "VR-10.1.1.2/3", marks=pytestrail.case('C8405'),
                                          id="request contains token which is not present in the DB"),
                             pytest.param("token", f"{uuid4()}", "VR-10.1.1.1/3", marks=pytestrail.case('C8406'),
                                          id="request contains owner which is not present in the DB")
                         ])
def test_checkAccessToTender_does_not_access_to_tender(port, host, param, value, prepared_cpid, code,
                                                       prepared_token_entity,
                                                       prepared_owner,
                                                       response,
                                                       data_tender,
                                                       payload_checkAccessToTender,
                                                       execute_insert_into_access_tender,
                                                       clear_access_tender_by_cpid):
    data = data_tender
    data['ocid'] = prepared_cpid
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_checkAccessToTender()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": f"Invalid {param} '{value}' by cpid '{prepared_cpid}'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("owner", marks=pytestrail.case('C8407')),
                             pytest.param("token", marks=pytestrail.case('C8409'))

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_attribute(port, host, param, response,
                                                                                          payload_checkAccessToTender):
    payload = payload_checkAccessToTender()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8423')),
                             pytest.param("ocid", marks=pytestrail.case('C8424')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_param_in_params(port, host, param,
                                                                                                response,
                                                                                                payload_checkAccessToTender):
    payload = payload_checkAccessToTender()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("cpid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8427'), id="empty string as cpid"),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN|TP)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8428'), id="empty string as ocid"),
                             pytest.param("ocid", "ocds-t1s2t3-MD-1585832251336", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN|TP)-[0-9]{13}$'."
                                          " Actual value: 'ocds-t1s2t3-MD-1585832251336'.",
                                          marks=pytestrail.case('C8426'), id="inccorect ocid"),
                             pytest.param("token", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8429'), id="empty string as token"),
                             pytest.param("owner", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8430'))
                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(host, port, param, value, code,
                                                                        response_error, description, response,
                                                                        payload_checkAccessToTender):
    payload = payload_checkAccessToTender()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]

    assert actualresult == response.error
