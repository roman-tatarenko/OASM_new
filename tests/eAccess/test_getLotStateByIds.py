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
                                                            data_tender, prepared_cpid,
                                                            prepared_token_entity, prepared_owner,
                                                            payload_getLotStateByIds,
                                                            execute_insert_into_access_tender,
                                                            response, prepared_entity_id,
                                                            clear_access_tender_by_cpid):
    lot_id = str(prepared_entity_id())
    data = data_tender
    data['tender']['lots'][0]['id'] = lot_id
    data['tender']['lots'][0]['status'] = status
    data['tender']['lots'][0]['statusDetails'] = statusDetails
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_getLotStateByIds(lot_id)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": lot_id,
            "status": f"{status}",
            "statusDetails": f"{statusDetails}"
        }
    ]

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param('cpid', marks=pytestrail.case('C8369')),
                             pytest.param('ocid', marks=pytestrail.case('C8370')),
                             pytest.param('lotIds', marks=pytestrail.case('C8353'))
                         ])
def test_getLotStateByIds_request_does_not_contain_param_in_params(port, host, param, response,
                                                                   payload_getLotStateByIds):
    payload = payload_getLotStateByIds()
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
                                          marks=pytestrail.case('C8464'), id="cpid as empty string"),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8463'), id="ocid as empty string"),
                             pytest.param("lotIds", [""], "DR-4/3",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8465'), id="lotIds as array with empty string"),
                             pytest.param("lotIds", [], "DR-10/3",
                                          "Array is empty.",
                                          marks=pytestrail.case('C12522'), id="lotIds as empty array"),
                             pytest.param("lotIds", "", "RQ-02/3",
                                          "Can not parse 'params'.",
                                          marks=pytestrail.case('C8368'), id="lotIds as empty string"),
                             pytest.param("ocid", "ocds-t1s2t3-MD-1585832251336", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'ocds-t1s2t3-MD-1585832251336'.",
                                          marks=pytestrail.case('C8371'), id="inccorect ocid")

                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(host, port, param, value, code,
                                                                        response, description,
                                                                        payload_getLotStateByIds):
    payload = payload_getLotStateByIds()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]

    if param == "lotIds" and value == "":
        response.error['result'] = [
            {
                "code": code,
                "description": description

            }
        ]

    assert actualresult == response.error


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
                                                                                            data_two_lots_and_items,
                                                                                            response, data_tender,
                                                                                            payload_getLotStateByIds,
                                                                                            execute_insert_into_access_tender):
    lot_id_1, lot_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data_tender['tender'].update(data_two_lots_and_items)
    data = data_tender
    data['tender']['lots'][0]['id'] = lot_id_1
    data['tender']['lots'][0]['status'] = state_1['status']
    data['tender']['lots'][0]['statusDetails'] = state_1['statusDetails']
    data['tender']['lots'][1]['id'] = lot_id_2
    data['tender']['lots'][1]['status'] = state_2['status']
    data['tender']['lots'][1]['statusDetails'] = state_2['statusDetails']
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_getLotStateByIds(lot_id_1, lot_id_2)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": lot_id_1,
            "status": state_1['status'],
            "statusDetails": state_1['statusDetails']
        },
        {
            "id": lot_id_2,
            "status": state_2['status'],
            "statusDetails": state_2['statusDetails']
        }
    ]

    assert actualresult == response.success


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
                                                                                                       response,
                                                                                                       data_tender,
                                                                                                       payload_getLotStateByIds,
                                                                                                       execute_insert_into_access_tender):
    lot_id_1, lot_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data = data_tender
    data['tender']['lots'][0]['id'] = lot_id_1
    data['tender']['lots'][0]['status'] = state['status']
    data['tender']['lots'][0]['statusDetails'] = state['statusDetails']
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_getLotStateByIds(lot_id_1, lot_id_2)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.1.3.2/3",
            "description": f"Lots '[{lot_id_2}]' do not found."
        }
    ]

    assert actualresult == response.error


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
        response,
        payload_getLotStateByIds,
        data_tender, data_two_lots_and_items,
        execute_insert_into_access_tender):
    lot_id_1, lot_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data_tender['tender'].update(data_two_lots_and_items)
    data = data_tender
    data['tender']['lots'][0]['id'] = lot_id_1
    data['tender']['lots'][0]['status'] = state_1['status']
    data['tender']['lots'][0]['statusDetails'] = state_1['statusDetails']
    data['tender']['lots'][1]['id'] = lot_id_2
    data['tender']['lots'][1]['status'] = state_2['status']
    data['tender']['lots'][1]['statusDetails'] = state_2['statusDetails']
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_getLotStateByIds(lot_id_1)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": lot_id_1,
            "status": state_1['status'],
            "statusDetails": state_1['statusDetails']
        }
    ]

    assert actualresult == response.success
