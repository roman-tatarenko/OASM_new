# : status complete, status details empty
import json
from datetime import datetime

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("status,statusDetails",
                         [
                             pytest.param("complete", "empty",
                                          marks=pytestrail.case('C8345')),
                             pytest.param("active", "empty",
                                          marks=pytestrail.case('C8346')),
                             pytest.param("unsuccessful", "empty",
                                          marks=pytestrail.case('C8347')),
                             pytest.param("cancelled", "empty",
                                          marks=pytestrail.case('C8348')),
                             pytest.param("planning", "empty",
                                          marks=pytestrail.case('C8349')),
                             pytest.param("active", "awarded",
                                          marks=pytestrail.case('C8350')),

                         ])
def test_eAccess_returns_successful_response_with_lot_state(host, port, status, statusDetails,
                                                            prepared_data_access_tender, prepared_cpid,
                                                            prepared_token_entity, prepared_owner,
                                                            prepared_payload_getLotStateByIds,
                                                            execute_insert_into_access_tender,
                                                            response_success, prepared_entity_id,
                                                            clear_access_tender_by_cpid):
    lot_id = prepared_entity_id()
    data = prepared_data_access_tender
    data['tender']['lots'][0]['id'] = f"{lot_id}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_getLotStateByIds(lot_id=lot_id)

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success
    expectedresult['result'] = [
        {
            "id": f"{lot_id}",
            "status": f"{status}",
            "statusDetails": f"{statusDetails}"
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(payload))


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("id", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8354')),
                             pytest.param("id", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8355')),
                             pytest.param("id", "", "DR-4/3",
                                          "Data format mismatch."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8356')),
                             pytest.param("action", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8359')),
                             pytest.param("action", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8360')),
                             pytest.param("action", "", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'getLotIds, checkAccessToTender, getLotStateByIds,"
                                          " responderProcessing, checkPersonesStructure, setStateForLots,"
                                          " setStateForTender', actual value: ''.",
                                          marks=pytestrail.case('C8358')),
                             pytest.param("action", "checkItems", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'getLotIds, checkAccessToTender, getLotStateByIds,"
                                          " responderProcessing, checkPersonesStructure, setStateForLots,"
                                          " setStateForTender', actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8357')),
                             pytest.param("version", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8364')),
                             pytest.param("version", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8363')),
                             pytest.param("version", "", "DR-4/3",
                                          "Data format mismatch."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8365'))
                         ])
def test_on_there_is_response_with_status_error_if_request_contains(port, host, param, value, code, description,
                                                                    response_error,
                                                                    prepared_payload_getLotStateByIds):
    payload = prepared_payload_getLotStateByIds()
    payload[param] = value

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

    if param == "id":
        expectedresult['id'] = "00000000-0000-0000-0000-000000000000"
    if param in {'action', "id"}:
        expectedresult['version'] = '2.0.0'

        assert actualresult == expectedresult, print(actualresult)


@pytest.mark.parametrize("param",
                         [
                             pytest.param("version", marks=pytestrail.case('C8361')),
                             pytest.param("params", marks=pytestrail.case('C8366'))

                         ])
def test_on_there_is_response_with_status_error_if_request_does_not_contain(port, host, param,
                                                                            prepared_payload_getLotStateByIds,
                                                                            response_error
                                                                            ):
    payload = prepared_payload_getLotStateByIds()
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


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8369')),
                             pytest.param("ocid", marks=pytestrail.case('C8370')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_param_in_params(port, host, param,
                                                                                                prepared_request_id,
                                                                                                response_error,
                                                                                                prepared_payload_getLotStateByIds):
    payload = prepared_payload_getLotStateByIds()
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
                             pytest.param("cpid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8464'), id="empty string as cpid"),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8463'), id="empty string as ocid"),
                             pytest.param("lotIds", [""], "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8465'), id="[""] as lotIds"),
                             pytest.param("lotIds", [], "DR-10/3",
                                          "Array is empty.",
                                          marks=pytestrail.case('C12522'), id="[] as lotIds"),
                             pytest.param("lotIds", "", "DR-10/3",
                                          "Can not parse 'params'.",
                                          marks=pytestrail.case('C8368'), id="[] as lotIds"),
                             pytest.param("ocid", "ocds-t1s2t3-MD-1585832251336", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'ocds-t1s2t3-MD-1585832251336'.",
                                          marks=pytestrail.case('C8371'), id="inccorect ocid")

                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(host, port, param, value, code,
                                                                        response_error, description,
                                                                        prepared_payload_getLotStateByIds):
    payload = prepared_payload_getLotStateByIds()
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

    if param == "lotIds" and value == "":
        expectedresult['result'] = [
            {
                "code": code,
                "description": description

            }
        ]

    assert actualresult == expectedresult, print(f"ex = {json.dumps(payload)}, ar = {json.dumps(actualresult)}")


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("params", [{}], marks=pytestrail.case('C8367'))
                         ])
def test_on_eAccess_with_inccorect_params_in_payload(host, port, param, value, response_error,
                                                     prepared_payload_getLotStateByIds):
    payload = prepared_payload_getLotStateByIds()
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


@pytest.mark.parametrize("state_1,state_2",
                         [
                             pytest.param({"status": "complete", "statusDetails": "empty"},
                                          {"status": "active", "statusDetails": "awarded"},
                                          marks=pytestrail.case('C8351'))
                         ])
def test_eAccess_returns_successful_response_with_lots_states_if_here_are_more_then_one_lot(port, host, state_1,
                                                                                            state_2,
                                                                                            prepared_entity_id,
                                                                                            prepared_token_entity,
                                                                                            prepared_owner,
                                                                                            prepared_cpid,
                                                                                            response_success,
                                                                                            prepared_payload_getLotStateByIds,
                                                                                            prepared_data_access_tender_2_lots,
                                                                                            execute_insert_into_access_tender):
    lot_id_1 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()

    data = prepared_data_access_tender_2_lots

    data['tender']['lots'][0]['id'] = f"{lot_id_1}"
    data['tender']['lots'][0]['status'] = state_1['status']
    data['tender']['lots'][0]['statusDetails'] = state_1['statusDetails']

    data['tender']['lots'][1]['id'] = f"{lot_id_2}"
    data['tender']['lots'][1]['status'] = state_2['status']
    data['tender']['lots'][1]['statusDetails'] = state_2['statusDetails']

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_getLotStateByIds()
    payload['params']["lotIds"] = [f"{lot_id_1}", f"{lot_id_2}"]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success
    expectedresult['result'] = [
        {
            "id": f"{lot_id_1}",
            "status": state_1['status'],
            "statusDetails": state_1['statusDetails']
        },
        {
            "id": f"{lot_id_2}",
            "status": state_2['status'],
            "statusDetails": state_2['statusDetails']
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(payload))


@pytest.mark.parametrize("state",
                         [
                             pytest.param({"status": "complete", "statusDetails": "empty"},
                                          marks=pytestrail.case('C8352'))
                         ])
def test_eAccess_returns_unsuccessful_response_if_at_least_one_lot_from_request_is_not_presented_in_DB(port, host,
                                                                                                       state,
                                                                                                       prepared_entity_id,
                                                                                                       prepared_token_entity,
                                                                                                       prepared_owner,
                                                                                                       prepared_cpid,
                                                                                                       response_error,
                                                                                                       prepared_payload_getLotStateByIds,
                                                                                                       prepared_data_access_tender,
                                                                                                       execute_insert_into_access_tender):
    lot_id_1 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()

    data = prepared_data_access_tender

    data['tender']['lots'][0]['id'] = f"{lot_id_1}"
    data['tender']['lots'][0]['status'] = state['status']
    data['tender']['lots'][0]['statusDetails'] = state['statusDetails']

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_getLotStateByIds()
    payload['params']["lotIds"] = [f"{lot_id_1}", f"{lot_id_2}"]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "VR-10.1.3.2/3",
            "description": f"Lots '[{lot_id_2}]' do not found."
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(actualresult))


@pytest.mark.parametrize("state_1,state_2",
                         [
                             pytest.param({"status": "complete", "statusDetails": "empty"},
                                          {"status": "active", "statusDetails": "awarded"},
                                          marks=pytestrail.case('C8372'))
                         ])
def test_eAccess_returns_successful_response_with_lots_states_if_there_are_more_then_one_lot_in_DB_and_one_lot_in_request(
        port, host, state_1,
        state_2,
        prepared_entity_id,
        prepared_token_entity,
        prepared_owner,
        prepared_cpid,
        response_success,
        prepared_payload_getLotStateByIds,
        prepared_data_access_tender_2_lots,
        execute_insert_into_access_tender):
    lot_id_1 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()

    data = prepared_data_access_tender_2_lots

    data['tender']['lots'][0]['id'] = f"{lot_id_1}"
    data['tender']['lots'][0]['status'] = state_1['status']
    data['tender']['lots'][0]['statusDetails'] = state_1['statusDetails']

    data['tender']['lots'][1]['id'] = f"{lot_id_2}"
    data['tender']['lots'][1]['status'] = state_2['status']
    data['tender']['lots'][1]['statusDetails'] = state_2['statusDetails']

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_getLotStateByIds()
    payload['params']["lotIds"] = [f"{lot_id_1}"]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success
    expectedresult['result'] = [
        {
            "id": f"{lot_id_1}",
            "status": state_1['status'],
            "statusDetails": state_1['statusDetails']
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(payload))


@pytest.mark.parametrize("state_1,state_2",
                         [
                             pytest.param({"status": "complete", "statusDetails": "empty"},
                                          {"status": "active", "statusDetails": "awarded"},
                                          marks=pytestrail.case('C8353'))
                         ])
def test_eAccess_returns_successful_response_with_states_of_all_lots_from_DB_if_request_does_not_contain_lotIds_array(
        port, host, state_1,
        state_2,
        prepared_entity_id,
        prepared_token_entity,
        prepared_owner,
        prepared_cpid,
        response_success,
        prepared_payload_getLotStateByIds,
        prepared_data_access_tender_2_lots,
        execute_insert_into_access_tender):
    lot_id_1 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()

    data = prepared_data_access_tender_2_lots

    data['tender']['lots'][0]['id'] = f"{lot_id_1}"
    data['tender']['lots'][0]['status'] = state_1['status']
    data['tender']['lots'][0]['statusDetails'] = state_1['statusDetails']

    data['tender']['lots'][1]['id'] = f"{lot_id_2}"
    data['tender']['lots'][1]['status'] = state_2['status']
    data['tender']['lots'][1]['statusDetails'] = state_2['statusDetails']

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner=prepared_owner)

    payload = prepared_payload_getLotStateByIds()
    del payload['params']["lotIds"]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success
    expectedresult['result'] = [
        {
            "id": f"{lot_id_1}",
            "status": state_1['status'],
            "statusDetails": state_1['statusDetails']
        },
        {
            "id": f"{lot_id_2}",
            "status": state_2['status'],
            "statusDetails": state_2['statusDetails']
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(payload))
