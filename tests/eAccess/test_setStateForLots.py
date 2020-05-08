import json
from datetime import datetime

import pytest
import requests
from pytest_testrail.plugin import pytestrail

from resources.domain.lot import schema_lot
from resources.domain.tender import schema_tender


@pytestrail.case("C17128")
def test_setStateForLots_lot_state_is_not_different_from_the_current(host, port, prepared_cpid,
                                                                     prepare_data, prepared_token_entity,
                                                                     payload_setStateForLots,
                                                                     prepared_owner, response,
                                                                     execute_insert_into_access_tender,
                                                                     execute_select_access_tenders_by_cpid,
                                                                     clear_access_tender_by_cpid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lot = {
        "id": data['tender']['lots'][0]['id'],
        "status": data['tender']['lots'][0]['status'],
        "statusDetails": data['tender']['lots'][0]['statusDetails']
    }

    payload = payload_setStateForLots(lot)

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success

    record = execute_select_access_tenders_by_cpid(
        cp_id=cpid
    ).one()

    json_data = json.loads(record.json_data)

    assert json_data['tender']['lots'][0]['id'] == data['tender']['lots'][0]['id']
    assert json_data['tender']['lots'][0]['status'] == data['tender']['lots'][0]['status']
    assert json_data['tender']['lots'][0]['statusDetails'] == data['tender']['lots'][0]['statusDetails']


@pytest.mark.parametrize("record_status, set_status",
                         [
                             pytest.param("active", "cancelled",
                                          marks=pytestrail.case('C17131'),
                                          id=" status as cancelled"),

                             pytest.param("cancelled", "active",
                                          marks=pytestrail.case('C17132'),
                                          id=" status as active"),

                             pytest.param("active", "complete",
                                          marks=pytestrail.case('C17133'),
                                          id=" status as complete"),
                         ])
def test_setStateForLots_set_the_status(host, port, record_status, set_status,
                                        prepared_cpid, response,
                                        prepared_token_entity, prepared_owner,
                                        prepare_data, payload_setStateForLots,
                                        execute_insert_into_access_tender,
                                        clear_access_tender_by_cpid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    data['tender']['lots'][0]['status'] = record_status
    lot_id = data['tender']['lots'][0]['id']
    status_details = data['tender']['lots'][0]['statusDetails']
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    lot = {
        "id": lot_id,
        "status": set_status,
        "statusDetails": status_details
    }
    payload = payload_setStateForLots(lot)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = payload['params']['lots']

    assert actualresult == response.success


@pytestrail.case('C17134')
@pytest.mark.parametrize('statusDetails', ["empty"])
def test_setStateForLots_set_statusDetails_as_empty(host, port, statusDetails,
                                                    prepared_cpid,
                                                    response, prepared_token_entity,
                                                    prepared_owner, prepare_data,
                                                    payload_setStateForLots,
                                                    execute_insert_into_access_tender,
                                                    execute_select_access_tenders_by_cpid,
                                                    clear_access_tender_by_cpid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    lot_id = data['tender']['lots'][0]['id']
    status = data['tender']['lots'][0]['status']
    data['tender']['lots'][0]['statusDetails'] = "awarded"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lot = {
        "id": lot_id,
        "status": status,
        "statusDetails": statusDetails
    }

    payload = payload_setStateForLots(lot)

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [lot]

    assert actualresult == response.success

    record = execute_select_access_tenders_by_cpid(
        cp_id=cpid
    ).one()

    json_data = json.loads(record.json_data)

    assert json_data['tender']['lots'][0]['status'] == status
    assert json_data['tender']['lots'][0]['statusDetails'] == statusDetails


@pytestrail.case('C17135')
def test_setStateForLots_return_state_for_lots(host, port, prepared_cpid,
                                               execute_insert_into_access_tender,
                                               response, prepared_token_entity,
                                               prepared_owner, prepare_data,
                                               payload_setStateForLots,
                                               prepared_entity_id,
                                               clear_access_tender_by_cpid,
                                               execute_select_access_tenders_by_cpid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    data['tender']['lots'] = prepare_data(schema=schema_lot, quantity=2)

    lot_1 = data['tender']['lots'][0]
    lot_1['id'] = str(prepared_entity_id())
    lot_1['status'] = "cancelled"
    lot_1['statusDetails'] = "awarded"

    lot_2 = data['tender']['lots'][1]
    lot_2['id'] = str(prepared_entity_id())
    lot_2['status'] = "active"
    lot_2['statusDetails'] = "awarded"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lots = [
        {
            "id": lot_1['id'],
            "status": "active",
            "statusDetails": "empty"
        },
        {
            "id": lot_2['id'],
            "status": "cancelled",
            "statusDetails": "empty"
        }
    ]

    payload = payload_setStateForLots(
        *lots
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = payload['params']['lots']

    assert actualresult == response.success

    record = execute_select_access_tenders_by_cpid(
        cp_id=cpid
    ).one()

    json_data = json.loads(record.json_data)

    assert json_data['tender']['lots'][0]['status'] == "active"
    assert json_data['tender']['lots'][1]['status'] == "cancelled"
    assert json_data['tender']['lots'][0]['statusDetails'] == "empty"
    assert json_data['tender']['lots'][1]['statusDetails'] == "empty"


@pytestrail.case("C17140")
def test_setStateForLots_tender_not_found_by_cpid(host, port,
                                                  prepared_cpid, payload_setStateForLots, response,
                                                  prepare_data, prepared_ev_ocid, prepared_entity_id):
    lot = {
        "id": str(prepared_entity_id()),
        "status": "active",
        "statusDetails": "empty"
    }

    payload = payload_setStateForLots(
        lot
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR-10.1.7.1/3",
        "description": f"Lots '[{lot['id']}]' do not found."
    }]

    assert actualresult == response.error


@pytestrail.case('C17141')
@pytest.mark.parametrize("lot_id", ["", "4to-to"])
def test_setStateForLots_use_invalid_value_in_lots_array_for_id(host, port, response, prepare_data,
                                                                payload_setStateForLots,
                                                                lot_id):
    lot = {
        "id": lot_id,
        "status": "active",
        "statusDetails": "empty"
    }

    payload = payload_setStateForLots(
        lot
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-4/3",
        "description": "Data format mismatch."
                       " Expected data format: 'uuid',"
                       f" actual value: '{lot_id}'.",
        "details": [{"name": "Lot.id"}]
    }]

    assert actualresult == response.error


@pytestrail.case('C17142')
@pytest.mark.parametrize("status", ["", "4to-to"])
def test_setStateForLots_use_invalid_value_in_lots_array_for_status(host, port, response, prepare_data,
                                                                    payload_setStateForLots, prepared_entity_id,
                                                                    status):
    lot = {
        "id": str(prepared_entity_id()),
        "status": status,
        "statusDetails": "empty"
    }

    payload = payload_setStateForLots(
        lot
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-3/3",
        "description": "Attribute value mismatch with one of enum expected values. "
                       "Expected values: 'active, cancelled, complete'"
                       f" actual value: '{status}'.",
        "details": [{"name": "Lot.status"}]
    }]

    assert actualresult == response.error


@pytestrail.case('C17143')
@pytest.mark.parametrize("status_details", ["", "4to-to"])
def test_setStateForLots_use_invalid_value_in_lots_array_for_status_details(host, port, response, prepare_data,
                                                                            payload_setStateForLots, prepared_entity_id,
                                                                            status_details):
    lot = {
        "id": str(prepared_entity_id()),
        "status": "active",
        "statusDetails": status_details
    }

    payload = payload_setStateForLots(
        lot
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-3/3",
        "description": f"Attribute value mismatch with one of enum expected values."
                       f" Expected values: 'empty', actual value: '{status_details}'.",
        "details": [{"name": "Lot.statusDetails"}]
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C17146'),
                                          id="without cpid"),

                             pytest.param("ocid",
                                          marks=pytestrail.case('C17147'),
                                          id=" without ocid"),

                             pytest.param("lots",
                                          marks=pytestrail.case('C17153'),
                                          id=" without lots array"),

                         ])
def test_setStateForLots_does_not_contains_param(host, port, response, payload_setStateForLots, param):
    payload = payload_setStateForLots()
    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-02/3",
        "description": "Can not parse 'params'."
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case('C17148'),
                                          id="without id"),

                             pytest.param("status",
                                          marks=pytestrail.case('C17149'),
                                          id=" without status"),

                             pytest.param("statusDetails",
                                          marks=pytestrail.case('C17150'),
                                          id=" without statusDetails"),

                         ])
def test_setStateForLots_without_attribute_in_lots_array(host, port, response, payload_setStateForLots, param,
                                                         prepare_data, prepared_entity_id):
    lot = {
        "id": str(prepared_entity_id()),
        "status": "active",
        "statusDetails": "empty"
    }

    payload = payload_setStateForLots(lot)
    del payload['params']['lots'][0][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-02/3",
        "description": "Can not parse 'params'."
    }]

    assert actualresult == response.error


@pytestrail.case("C17152")
def test_setStateForLots_lots_as_empty_array(host, port,
                                             payload_setStateForLots, response):
    payload = payload_setStateForLots()
    payload['params']['lots'] = []

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-10/3",
        "description": "Array is empty.",
        "details": [{"name": "lots"}]

    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, description",
                         [
                             pytest.param("cpid", "",
                                          "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: ''.",
                                          marks=pytestrail.case('C20915'),
                                          id="by cpid"),

                             pytest.param("ocid", "",
                                          "Data mismatch to pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: ''.",
                                          marks=pytestrail.case('C20916'),
                                          id=" by ocid")

                         ])
def test_setStateForLots_data_mismatch_to_the_pattern(host, port,
                                                      param, value, description,
                                                      prepare_data,
                                                      payload_setStateForLots,
                                                      prepared_entity_id,
                                                      response):
    lot = {
        "id": str(prepared_entity_id()),
        "status": "active",
        "statusDetails": "empty"
    }

    payload = payload_setStateForLots(lot)
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-5/3",
        "description": description,
        "details": [{
            "name": param
        }]
    }]

    assert actualresult == response.error
