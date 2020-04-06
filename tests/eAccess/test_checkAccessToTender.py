import json
from datetime import datetime
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8404')
def test_eAccess_returns_successful_response_when_token_and_owner_are_present_in_the_DB(port, host, prepared_cpid,
                                                                                        prepared_token_entity,
                                                                                        prepared_owner,
                                                                                        response_success,
                                                                                        prepared_data_access_tender,
                                                                                        prepared_payload_checkAccessToTender,
                                                                                        execute_insert_into_access_tender,
                                                                                        clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    data['ocid'] = prepared_cpid

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_checkAccessToTender

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = response_success

    assert actual_result == expected_result


@pytest.mark.parametrize("param,value,code",
                         [
                             pytest.param("owner", f"{uuid4()}", "VR-10.1.1.2/3", marks=pytestrail.case('C8405'),
                                          id="request contains token which is not present in the DB"),
                             pytest.param("token", f"{uuid4()}", "VR-10.1.1.1/3", marks=pytestrail.case('C8406'),
                                          id="request contains owner which is not present in the DB"),
                             pytest.param("owner", "", "DR-4/3", marks=pytestrail.case('C8430'))

                         ])
def test_eAccess_returns_response_with_status_error(port, host, param, value, prepared_cpid, code,
                                                    prepared_token_entity,
                                                    prepared_owner,
                                                    response_error,
                                                    prepared_data_access_tender,
                                                    prepared_payload_checkAccessToTender,
                                                    execute_insert_into_access_tender,
                                                    clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    data['ocid'] = prepared_cpid

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_checkAccessToTender
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": code,
            "description": f"Invalid {param} '{value}' by cpid '{prepared_cpid}'."
        }
    ]

    if param == "owner" and value == "":
        expectedresult['result'] = [
            {
                "code": "DR-4/3",
                "description": "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                "details": [
                    {
                        "name": "owner"
                    }
                ]
            }
        ]

    assert actualresult == expectedresult, print(json.dumps(actualresult))


@pytest.mark.parametrize("param",
                         [
                             pytest.param("owner", marks=pytestrail.case('C8407')),
                             pytest.param("token", marks=pytestrail.case('C8409'))

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_attribute(port, host, param,
                                                                                          prepared_cpid,
                                                                                          prepared_token_entity,
                                                                                          prepared_owner,
                                                                                          response_error,
                                                                                          prepared_data_access_tender,
                                                                                          prepared_payload_checkAccessToTender,
                                                                                          execute_insert_into_access_tender,
                                                                                          clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    data['ocid'] = prepared_cpid

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_checkAccessToTender
    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8418')),
                             pytest.param("version", 3.14, "DR-2/3",
                                          "Data type mismatch. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8411')),
                             pytest.param("version", True, "DR-2/3",
                                          "Data type mismatch. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8412')),
                             pytest.param("id", 3.14, "DR-2/3",
                                          "Data type mismatch. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8419')),
                             pytest.param("id", True, "DR-2/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: 'true'.",
                                          marks=pytestrail.case('C8420')),
                             pytest.param("id", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8421')),
                             pytest.param("action", 3.14, "DR-2/3",
                                          "Data type mismatch. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8416')),
                             pytest.param("action", "", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'getLotIds, checkAccessToTender, getLotStateByIds,"
                                          " responderProcessing, checkPersonsStructure', actual value: ''.",
                                          marks=pytestrail.case('C8417')),
                             pytest.param("action", "checkItems", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values. "
                                          "Expected values: 'getLotIds, checkAccessToTender,"
                                          " getLotStateByIds, responderProcessing, checkPersonsStructure',"
                                          " actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8414')),
                             pytest.param("action", True, "DR-2/3",
                                          "Data type mismatch. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8415')),

                         ])
def test_on_there_is_response_with_status_error_if_request_contains_number_as_version(port, host, param, value, code,
                                                                                      description, prepared_request_id,
                                                                                      prepared_payload_checkAccessToTender
                                                                                      ):
    payload = prepared_payload_checkAccessToTender
    payload[param] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description,
                "details": [
                    {
                        "name": param
                    }
                ]
            }
        ]
    }

    if param == "id":
        expectedresult['id'] = "00000000-0000-0000-0000-000000000000"

    if param in {'action', "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8423')),
                             pytest.param("ocid", marks=pytestrail.case('C8424')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_param_in_params(port, host, param,
                                                                                                prepared_request_id,
                                                                                                response_error,
                                                                                                prepared_payload_checkAccessToTender):
    payload = prepared_payload_checkAccessToTender
    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == expectedresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("version", marks=pytestrail.case('C8410')),
                             pytest.param("params", marks=pytestrail.case('C8422'))

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_param(port, host, param,
                                                                                      prepared_payload_checkAccessToTender,
                                                                                      response_error
                                                                                      ):
    payload = prepared_payload_checkAccessToTender
    del payload[param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "DR-1/3",
            "description": "Missing required attribute.",
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]
    if param in {"version"}:
        expectedresult['version'] = '1.0.0'

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("params", [{}], marks=pytestrail.case('C8425'))
                         ])
def test_on_dataValidation_with_inccorect_params_in_payload(host, port, param, value, response_error,
                                                            prepared_payload_checkAccessToTender):
    payload = prepared_payload_checkAccessToTender
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == expectedresult, payload

    pytest.param("ocid", "", "DR-5/3", marks=pytestrail.case('C8428'))


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("cpid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8427'), id="empty string as cpid"),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8428'), id="empty string as ocid"),
                             pytest.param("token", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8429'), id="empty string as token"),
                             pytest.param("ocid", "ocds-t1s2t3-MD-1585832251336", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'ocds-t1s2t3-MD-1585832251336'.",
                                          marks=pytestrail.case('C8426'), id="inccorect ocid")

                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(host, port, param, value, code,
                                                                        response_error, description,
                                                                        prepared_payload_checkAccessToTender):
    payload = prepared_payload_checkAccessToTender
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(actualresult))
