import json
from datetime import datetime
import pytest
import requests
from pytest_testrail.plugin import pytestrail
from resources.domain.lot import schema_lot, schema_lot_for_request
from resources.domain.tender import schema_tender


@pytestrail.case("C17128")
def test_setStateForLots_does_not_return_status_for_lots_and_statusDetails_for_lots(host, port, prepared_cpid,
                                                                                    prepare_data, prepared_ev_ocid,
                                                                                    prepared_token_entity,
                                                                                    execute_insert_into_access_tender,
                                                                                    payload_setStateForLots,
                                                                                    prepared_owner, response):
    cpid = prepared_cpid
    token = prepared_token_entity
    owner = prepared_owner
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=token,
        created_date=datetime.now(),
        json_data=data,
        owner=owner
    )

    lot = [prepare_data(schema=schema_lot_for_request)]
    lot[0]['id'] = data['tender']['lots'][0]['id']
    lot[0]['status'] = data['tender']['lots'][0]['status']
    lot[0]['statusDetails'] = data['tender']['lots'][0]['statusDetails']
    payload = payload_setStateForLots(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        lots=lot
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


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
def test_setStateForLots_set_the_status(host, port, execute_insert_into_access_tender, prepared_cpid, response,
                                        prepared_token_entity, prepared_owner, prepare_data, payload_setStateForLots,
                                        prepared_ev_ocid, record_status, set_status):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    data['tender']['lots'][0]['status'] = record_status
    record_lot_id = data['tender']['lots'][0]['id']
    record_status_detail = data['tender']['lots'][0]['statusDetails']
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lot = [prepare_data(schema=schema_lot_for_request)]
    lot[0]['id'] = record_lot_id
    lot[0]['status'] = set_status
    lot[0]['statusDetails'] = record_status_detail

    payload = payload_setStateForLots(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        lots=lot
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": record_lot_id,
            "status": set_status,
            "statusDetails": record_status_detail
        }

    ]

    assert actualresult == response.success


@pytestrail.case('C17134')
def test_setStateForLots_set_statusDetails_as_empty(host, port, execute_insert_into_access_tender, prepared_cpid,
                                                    response, prepared_token_entity, prepared_owner, prepare_data,
                                                    payload_setStateForLots, prepared_ev_ocid):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    record_lot_id = data['tender']['lots'][0]['id']
    record_lot_status = data['tender']['lots'][0]['status']
    data['tender']['lots'][0]['statusDetails'] = "awarded"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lot = [prepare_data(schema=schema_lot_for_request)]
    lot[0]['id'] = record_lot_id
    lot[0]['status'] = record_lot_status
    lot[0]['statusDetails'] = "empty"

    payload = payload_setStateForLots(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        lots=lot
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": record_lot_id,
            "status": record_lot_status,
            "statusDetails": "empty"
        }

    ]

    assert actualresult == response.success


@pytestrail.case('C17135')
def test_setStateForLots_return_status_for_lots_and_the_statusDetails_for_lots(host, port, prepared_cpid,
                                                                               execute_insert_into_access_tender,
                                                                               response, prepared_token_entity,
                                                                               prepared_owner, prepare_data,
                                                                               payload_setStateForLots,
                                                                               prepared_ev_ocid, prepared_entity_id):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    data['ocid'] = cpid
    data['tender']['lots'] = prepare_data(schema=schema_lot, quantity=2)
    data['tender']['lots'][1]['id'] = str(prepared_entity_id())

    lot_a = data['tender']['lots'][0]
    lot_b = data['tender']['lots'][1]
    lot_a['status'] = "cancelled"
    lot_a['statusDetails'] = "awarded"
    lot_b['status'] = "active"
    lot_b['statusDetails'] = "awarded"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    lot = prepare_data(schema=schema_lot_for_request, quantity=2)
    lot[0]['id'] = lot_a['id']
    lot[0]['status'] = "active"
    lot[0]['statusDetails'] = "empty"
    lot[1]['id'] = lot_b['id']
    lot[1]['status'] = "cancelled"
    lot[1]['statusDetails'] = "empty"

    payload = payload_setStateForLots(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        lots=lot
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": lot_a['id'],
            "status": "active",
            "statusDetails": "empty"
        },
        {
            "id": lot_b['id'],
            "status": "cancelled",
            "statusDetails": "empty"
        }
    ]

    assert actualresult == response.success


@pytestrail.case("C17140")
def test_setStateForLots_tender_not_found_by_cpid(host, port, prepared_cpid, payload_setStateForLots, response,
                                                  prepare_data, prepared_ev_ocid):
    payload = payload_setStateForLots(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        lots=[prepare_data(schema=schema_lot_for_request)]
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR-10.1.7.1/3",
        "description": f"Lots '[{payload['params']['lots'][0]['id']}]' do not found."
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code,description",
                         [
                             pytest.param("id", "", "DR-4/3", f"Data format mismatch. "
                                                              f"Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C17141'),
                                          id=" id as empty string"),

                             pytest.param("status", "", "DR-3/3",
                                          f"Attribute value mismatch with one of enum expected values. "
                                          f"Expected values: 'active, cancelled, complete', actual value: ''.",
                                          marks=pytestrail.case('C17142'),
                                          id=" status empty string"),

                             pytest.param("statusDetails", "", "DR-3/3",
                                          f"Attribute value mismatch with one of enum expected values."
                                          f" Expected values: 'empty', actual value: ''.",
                                          marks=pytestrail.case('C17143'),
                                          id=" status as complete")
                         ])
def test_setStateForLots_use_invalid_value_in_lots_array(host, port, response, prepare_data, payload_setStateForLots,
                                                         param, value, code, description):
    lot = [prepare_data(schema=schema_lot_for_request)]
    lot[0][param] = value

    payload = payload_setStateForLots(
        lots=lot
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": code,
        "description": description,
        "details": [{
            "name": f"Lot.{param}"
        }]
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
                                                         prepare_data):
    payload = payload_setStateForLots(
        lots=[prepare_data(schema=schema_lot_for_request)]
    )

    del payload['params']['lots'][0][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-02/3",
        "description": "Can not parse 'params'."
    }]

    assert actualresult == response.error


@pytestrail.case("C17151")
def test_setStateForLots_params_as_empty_object(host, port, response, payload_setStateForLots):
    payload = payload_setStateForLots()

    payload['params'] = {}

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-02/3",
        "description": "Can not parse 'params'."
    }]

    assert actualresult == response.error


@pytestrail.case("C17152")
def test_setStateForLots_lots_as_empty_array(host, port, response, payload_setStateForLots):
    payload = payload_setStateForLots()

    payload['params']['lots'] = []

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-10/3",
        "description": "Array is empty.",
        "details": [{"name": "lots"}]

    }]

    assert actualresult == response.error


@pytestrail.case("C17154")
def test_setStateForLots_request_does_not_contains_params_in_request(host, port, response, payload_setStateForLots):
    payload = payload_setStateForLots()

    del payload['params']

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "DR-1/3",
        "description": "Missing required attribute.",
        "details": [{
            "name": "params"
        }]
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, description",
                         [
                             pytest.param("cpid", "ocdst1s2t3-MD1580000000014",
                                          "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: 'ocdst1s2t3-MD1580000000014'.",
                                          marks=pytestrail.case('C20915'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD1580000000014EV1585642217593",
                                          "Data mismatch to pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: 'ocds-t1s2t3-MD1580000000014EV1585642217593'.",
                                          marks=pytestrail.case('C20916'),
                                          id=" by ocid")

                         ])
def test_setStateForLots_data_mismatch_to_the_pattern(host, port, response, payload_setStateForLots, param,
                                                      prepare_data, value, description):
    payload = payload_setStateForLots(
        lots=[prepare_data(schema=schema_lot_for_request)]
    )

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
