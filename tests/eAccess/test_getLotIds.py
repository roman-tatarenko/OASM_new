import json
import random
from datetime import datetime
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{"status": "complete"}], "complete",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8020')),
                             pytest.param([{"status": "active"}], "active",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8025')),
                             pytest.param([{"status": "unsuccessful"}], "unsuccessful",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8026')),
                             pytest.param([{"status": "cancelled"}], "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8027')),
                             pytest.param([{"status": "planning"}], "planning",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8028')),
                             pytest.param([{"statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8029')),
                             pytest.param([{"statusDetails": "awarded"}], "active", "awarded",
                                          marks=pytestrail.case('C8030')),
                             pytest.param([{"status": "complete", "statusDetails": "empty"}], "complete", "empty",
                                          marks=pytestrail.case('C8031')),
                             pytest.param([{"status": "active", "statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8032')),
                             pytest.param([{"status": "active", "statusDetails": "awarded"}], "active", "awarded",
                                          marks=pytestrail.case('C8033')),
                             pytest.param([{"status": "unsuccessful", "statusDetails": "empty"}], "unsuccessful",
                                          "empty",
                                          marks=pytestrail.case('C8034')),
                             pytest.param([{"status": "cancelled", "statusDetails": "empty"}], "cancelled",
                                          "empty",
                                          marks=pytestrail.case('C8035')),
                             pytest.param([{"status": "planning", "statusDetails": "empty"}], "planning",
                                          "empty",
                                          marks=pytestrail.case('C8036')),
                         ])
def test_eAccess_returns_lots_in_states(host, states, port, status, statusDetails, execute_insert_into_access_tender,
                                        prepared_cpid,
                                        prepared_entity_id, prepared_token_entity, prepared_request_id,
                                        prepared_payload_getLotIds, prepared_data_access_tender,
                                        clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    lot_id = prepared_entity_id()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{lot_id}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "result": [
            f"{lot_id}"
        ],
        "status": "success"
    }

    assert actual_result == expected_result


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{"status": "complete"}], "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8048')),
                             pytest.param([{"status": "active"}], "complete",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8049')),
                             pytest.param([{"status": "unsuccessful"}], "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8050')),
                             pytest.param([{"status": "cancelled"}], "active",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8051')),
                             pytest.param([{"status": "planning"}], "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8052')),
                             pytest.param([{"statusDetails": "empty"}], "active", "awarded",
                                          marks=pytestrail.case('C8053')),
                             pytest.param([{"statusDetails": "awarded"}], "active", "empty",
                                          marks=pytestrail.case('C8054')),
                             pytest.param([{"status": "complete", "statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8055')),
                             pytest.param([{"status": "active", "statusDetails": "empty"}], "complete", "empty",
                                          marks=pytestrail.case('C8056')),
                             pytest.param([{"status": "active", "statusDetails": "awarded"}], "active", "empty",
                                          marks=pytestrail.case('C8057')),
                             pytest.param([{"status": "unsuccessful", "statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8058')),
                             pytest.param([{"status": "cancelled", "statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8059')),
                             pytest.param([{"status": "planning", "statusDetails": "empty"}], "active", "empty",
                                          marks=pytestrail.case('C8060')),
                         ])
def test_eAccess_without_result(host, states, port, status, statusDetails, execute_insert_into_access_tender,
                                prepared_cpid,
                                prepared_entity_id, prepared_token_entity, response_success,
                                prepared_payload_getLotIds, prepared_data_access_tender, clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    lotId = prepared_entity_id()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{lotId}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success

    assert actualresult == expectedresult


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{"status": "complete"}, {"status": "unsuccessful"}],
                                          ("complete", "active"), (
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty"))),
                                          marks=pytestrail.case('C8063'))
                         ])
def test_eAccess_returns_lots_in_if_there_two_states_objects(host, states, port, status, statusDetails,
                                                             execute_insert_into_access_tender,
                                                             prepared_cpid,
                                                             prepared_entity_id, prepared_token_entity,
                                                             prepared_request_id,
                                                             prepared_payload_getLotIds,
                                                             prepared_data_access_tender_2_lots,
                                                             clear_access_tender_by_cpid):
    data = prepared_data_access_tender_2_lots

    entity_id_1, entity_id_2 = uuid4(), uuid4()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{entity_id_1}"
    data['tender']['lots'][0]['status'] = status[0]
    data['tender']['lots'][0]['statusDetails'] = statusDetails[0]

    data['ocid'] = prepared_cpid
    data['tender']['lots'][1]['id'] = f"{entity_id_2}"
    data['tender']['lots'][1]['status'] = status[1]
    data['tender']['lots'][1]['statusDetails'] = statusDetails[1]

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "result": [
            f"{entity_id_1}"
        ],
        "status": "success"
    }

    assert actual_result == expected_result


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{"status": "unsuccessful"}, {"status": "cancelled"}],
                                          ("complete", "active"), (
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty"))),
                                          marks=pytestrail.case('C8064'))
                         ])
def test_eAccess_returns_successful_response_without_result_array(host, states, port, status, statusDetails,
                                                                  execute_insert_into_access_tender,
                                                                  prepared_cpid,
                                                                  prepared_entity_id, prepared_token_entity,
                                                                  response_success,
                                                                  prepared_payload_getLotIds,
                                                                  prepared_data_access_tender_2_lots,
                                                                  clear_access_tender_by_cpid):
    data = prepared_data_access_tender_2_lots

    entity_id_1, entity_id_2 = uuid4(), uuid4()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{entity_id_1}"
    data['tender']['lots'][0]['status'] = status[0]
    data['tender']['lots'][0]['statusDetails'] = statusDetails[0]

    data['ocid'] = prepared_cpid
    data['tender']['lots'][1]['id'] = f"{entity_id_2}"
    data['tender']['lots'][1]['status'] = status[1]
    data['tender']['lots'][1]['statusDetails'] = statusDetails[1]

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_success

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,states,status,statusDetails,description",
                         [
                             pytest.param("status", [{"status": "withdrawn"}], "canceled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, unsuccessful, complete',"
                                          " actual value: 'withdrawn'.",
                                          marks=pytestrail.case('C8071'))
                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains_an_invalid_enum_value_for_(host, param, states,
                                                                                                   port, status,
                                                                                                   statusDetails,
                                                                                                   description,
                                                                                                   execute_insert_into_access_tender,
                                                                                                   prepared_cpid,
                                                                                                   prepared_entity_id,
                                                                                                   prepared_token_entity,
                                                                                                   prepared_request_id,
                                                                                                   prepared_payload_getLotIds,
                                                                                                   prepared_data_access_tender,
                                                                                                   clear_access_tender_by_cpid):
    data = prepared_data_access_tender
    lot_id = prepared_entity_id()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{lot_id}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-3/3",
                "description": description,
                "details": [
                    {
                        "name": param
                    }
                ]
            }
        ]
    }

    assert actual_result == expected_result, print(actual_result)


@pytest.mark.parametrize("param",
                         [
                             pytest.param("params", marks=pytestrail.case('C8087'))

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_(port, host, param,
                                                                                 prepared_request_id,
                                                                                 prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
    del payload[param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": 'DR-1/3',
                "description": "Missing required attribute.",
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

    if param in {"action", "params", "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8089')),
                             pytest.param("ocid", marks=pytestrail.case('C8090')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_does_not_contain_param_in_params(port, host, param,
                                                                                                prepared_request_id,
                                                                                                prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-02/3",
                "description": "Can not parse 'params'."
            }
        ]
    }

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8466')),
                             pytest.param("id", "", "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8467')),
                             pytest.param("action", "", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'getLotIds, checkAccessToTender, getLotStateByIds,"
                                          " responderProcessing, checkPersonesStructure', actual value: ''.",
                                          marks=pytestrail.case('C8468')),
                             pytest.param("version", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8642')),
                             pytest.param("id", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8643')),
                             pytest.param("action", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8644')),
                             pytest.param("version", True, "DR-2/3", "Data type mismatch."
                                                                     " Expected data type: 'STRING',"
                                                                     " actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8645')),
                             pytest.param("id", True, "DR-2/3", "Data type mismatch."
                                                                " Expected data type: 'STRING',"
                                                                " actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8646')),
                             pytest.param("action", True, "DR-2/3", "Data type mismatch."
                                                                    " Expected data type: 'STRING',"
                                                                    " actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8647')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(port, host, param,
                                                                        value, code,
                                                                        description,
                                                                        prepared_request_id,
                                                                        prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
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

    if param in {"action", "params", "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult, print(actualresult)


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("status", [{"status": "", "statusDetails": "empty"}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values. "
                                          "Expected values: 'planning, active, cancelled, unsuccessful,"
                                          " complete', actual value: ''.",
                                          marks=pytestrail.case('C8470')),
                             pytest.param("statusDetails", [{"status": "active", "statusDetails": ""}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: ''.",
                                          marks=pytestrail.case('C8471')),
                             pytest.param("status", [{"status": ""}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, unsuccessful,"
                                          " complete', actual value: ''.",
                                          marks=pytestrail.case('C8472')),
                             pytest.param("statusDetails", [{"statusDetails": ""}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: ''.",
                                          marks=pytestrail.case('C8473')),
                             pytest.param("statusDetails", [{"statusDetails": "withdrawn"}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: 'withdrawn'.",
                                          marks=pytestrail.case('C8072')),
                             pytest.param("status", [{"status": "disqualified", "statusDetails": "empty"}], "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, "
                                          "unsuccessful, complete', actual value: 'disqualified'.",
                                          marks=pytestrail.case('C8073')),
                             pytest.param("statusDetails", [{"status": "active", "statusDetails": "disqualified"}],
                                          "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: 'disqualified'.",
                                          marks=pytestrail.case('C8074'))
                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains_status(port, host, param,
                                                                               value, code,
                                                                               description,
                                                                               prepared_request_id,
                                                                               prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
    payload['params']['states'] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
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

    assert actualresult == expectedresult, print(actualresult)


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('cpid', "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: ''.",
                                          marks=pytestrail.case('C8474')),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8475')),

                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains_param(port, host, param,
                                                                              value, code,
                                                                              description,
                                                                              prepared_request_id,
                                                                              prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
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

    if param in {"action", "params", "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult, print(payload)


@pytest.mark.parametrize("status,statusDetails",
                         [
                             pytest.param("cancelled", "empty", marks=pytestrail.case('C8088'))
                         ])
def test_eAccess_returns_successful_response_with_lots_ids_if_request_does_not_contain_states_array(host, port, status,
                                                                                                    statusDetails,
                                                                                                    execute_insert_into_access_tender,
                                                                                                    prepared_cpid,
                                                                                                    prepared_entity_id,
                                                                                                    prepared_token_entity,
                                                                                                    prepared_request_id,
                                                                                                    prepared_payload_getLotIds,
                                                                                                    prepared_data_access_tender,
                                                                                                    clear_access_tender_by_cpid):
    lot_id = prepared_entity_id()
    data = prepared_data_access_tender

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{lot_id}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    del payload['params']['states']

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "result": [
            f"{lot_id}"
        ],
        "status": "success"
    }

    assert actual_result == expected_result


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{"status": "complete"}, {"status": "active"}],
                                          ("complete", "active"), (
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                                  random.choice(("unsuccessful", "awarded", "cancelled", "empty"))),
                                          marks=pytestrail.case('C8062'))
                         ])
def test_eAccess_returns_successful_response_with_lots_ids_if_there_two_states_objects_in_request(host, states, port,
                                                                                                  status, statusDetails,
                                                                                                  execute_insert_into_access_tender,
                                                                                                  prepared_cpid,
                                                                                                  prepared_entity_id,
                                                                                                  prepared_token_entity,
                                                                                                  prepared_request_id,
                                                                                                  prepared_payload_getLotIds,
                                                                                                  prepared_data_access_tender_2_lots,
                                                                                                  clear_access_tender_by_cpid):
    data = prepared_data_access_tender_2_lots

    entity_id_1, entity_id_2 = uuid4(), uuid4()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{entity_id_1}"
    data['tender']['lots'][0]['status'] = status[0]
    data['tender']['lots'][0]['statusDetails'] = statusDetails[0]

    data['ocid'] = prepared_cpid
    data['tender']['lots'][1]['id'] = f"{entity_id_2}"
    data['tender']['lots'][1]['status'] = status[1]
    data['tender']['lots'][1]['statusDetails'] = statusDetails[1]

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actual_result = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expected_result = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": [
            f"{entity_id_1}",
            f"{entity_id_2}"
        ]
    }

    assert actual_result == expected_result


@pytest.mark.parametrize("value",
                         [
                             pytest.param({}, marks=pytestrail.case('C8648'))
                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains_status_object_instead_of_array_of_objects(port,
                                                                                                                  host,
                                                                                                                  value,
                                                                                                                  prepared_request_id,
                                                                                                                  prepared_payload_getLotIds):
    payload = prepared_payload_getLotIds
    payload['params']['states'] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-02/3",
                "description": "Can not parse 'params'."
            }
        ]
    }

    assert actualresult == expectedresult, print(actualresult)


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param([{}], "cancelled", "empty", marks=pytestrail.case('C8964'))
                         ])
def test_eAccess_returns_successful_response_without_result_if_request_contain_empty_states_array_of_objects(host, port,
                                                                                                             states,
                                                                                                             status,
                                                                                                             statusDetails,
                                                                                                             execute_insert_into_access_tender,
                                                                                                             prepared_cpid,
                                                                                                             prepared_entity_id,
                                                                                                             prepared_token_entity,
                                                                                                             response_error,
                                                                                                             prepared_payload_getLotIds,
                                                                                                             prepared_data_access_tender
                                                                                                             ):
    data = prepared_data_access_tender
    lot_id = prepared_entity_id()

    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = f"{lot_id}"
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails

    execute_insert_into_access_tender(cp_id=prepared_cpid, stage='EV', token_entity=prepared_token_entity,
                                      created_date=datetime.now(), json_data=data,
                                      owner='3fa85f64-5717-4562-b3fc-2c963f66afa6')

    payload = prepared_payload_getLotIds
    payload['params']['states'] = states

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    expectedresult = response_error
    expectedresult['result'] = [
        {
            "code": "DR-9/3",
            "description": "Object is empty.",
            "details": [
                {
                    "name": "states"
                }
            ]
        }
    ]

    assert actualresult == expectedresult, print(json.dumps(actualresult))
