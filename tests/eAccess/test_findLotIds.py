import random
from datetime import datetime

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param({"status": "complete"}, "complete",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8020')),

                             pytest.param({"status": "active"}, "active",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8025')),

                             pytest.param({"status": "unsuccessful"}, "unsuccessful",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8026')),

                             pytest.param({"status": "cancelled"}, "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8027')),

                             pytest.param({"status": "planning"}, "planning",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8028')),

                             pytest.param({"statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8029')),

                             pytest.param({"statusDetails": "awarded"}, "active", "awarded",
                                          marks=pytestrail.case('C8030')),

                             pytest.param({"status": "complete", "statusDetails": "empty"}, "complete", "empty",
                                          marks=pytestrail.case('C8031')),

                             pytest.param({"status": "active", "statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8032')),

                             pytest.param({"status": "active", "statusDetails": "awarded"}, "active", "awarded",
                                          marks=pytestrail.case('C8033')),

                             pytest.param({"status": "unsuccessful", "statusDetails": "empty"}, "unsuccessful",
                                          "empty",
                                          marks=pytestrail.case('C8034')),

                             pytest.param({"status": "cancelled", "statusDetails": "empty"}, "cancelled",
                                          "empty",
                                          marks=pytestrail.case('C8035')),

                             pytest.param({"status": "planning", "statusDetails": "empty"}, "planning",
                                          "empty",
                                          marks=pytestrail.case('C8036'))

                         ])
def test_eAccess_returns_lots_in_states(host, states, port, status, statusDetails, execute_insert_into_access_tender,
                                        prepared_cpid, response, prepared_owner,
                                        prepared_entity_id, prepared_token_entity,
                                        prepared_payload_findLotIds, data_tender,
                                        clear_access_tender_by_cpid):
    json_data = data_tender
    lot_id = prepared_entity_id()
    json_data['ocid'] = prepared_cpid
    json_data['tender']['lots'][0]['id'] = str(lot_id)
    json_data['tender']['lots'][0]['status'] = status
    json_data['tender']['lots'][0]['statusDetails'] = statusDetails
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=json_data,
        owner=prepared_owner
    )
    payload = prepared_payload_findLotIds(states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [f"{lot_id}"]

    assert actualresult == response.success


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param({"status": "complete"}, "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8048'),
                                          id='in status "complete"'),

                             pytest.param({"status": "active"}, "complete",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8049'),
                                          id='in status "active"'),

                             pytest.param({"status": "unsuccessful"}, "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8050'),
                                          id='in status "unsuccessful"'),

                             pytest.param({"status": "cancelled"}, "active",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8051'),
                                          id='in status "cancelled"'),

                             pytest.param({"status": "planning"}, "cancelled",
                                          random.choice(("unsuccessful", "awarded", "cancelled", "empty")),
                                          marks=pytestrail.case('C8052'),
                                          id='in status "planning"'),

                             pytest.param({"statusDetails": "empty"}, "active", "awarded",
                                          marks=pytestrail.case('C8053'),
                                          id='in statusDetails "empty"'),

                             pytest.param({"statusDetails": "awarded"}, "active", "empty",
                                          marks=pytestrail.case('C8054'),
                                          id='in statusDetails "awarded"'),

                             pytest.param({"status": "complete", "statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8055'),
                                          id='in "status": "complete" and "statusDetails": "empty"'),

                             pytest.param({"status": "active", "statusDetails": "empty"}, "complete", "empty",
                                          marks=pytestrail.case('C8056'),
                                          id='in "status": "active" and "statusDetails": "empty"'),

                             pytest.param({"status": "active", "statusDetails": "awarded"}, "active", "empty",
                                          marks=pytestrail.case('C8057'),
                                          id='in "status": "active" and "statusDetails": "awarded"'),

                             pytest.param({"status": "unsuccessful", "statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8058'),
                                          id='in "status": "unsuccessful", "statusDetails": "empty"'),

                             pytest.param({"status": "cancelled", "statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8059'),
                                          id='in "status": "cancelled" and "statusDetails": "empty"'),

                             pytest.param({"status": "planning", "statusDetails": "empty"}, "active", "empty",
                                          marks=pytestrail.case('C8060'),
                                          id='in "status": "planning" and "statusDetails": "empty"')
                         ])
def test_findLotIds_there_are_no_lots_in_DB(host, port, states, status, statusDetails,
                                            execute_insert_into_access_tender,
                                            prepared_cpid, prepared_owner, response,
                                            prepared_entity_id, prepared_token_entity,
                                            prepared_payload_findLotIds, data_tender, clear_access_tender_by_cpid):
    data = data_tender
    lotId = prepared_entity_id()
    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = str(lotId)
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
    payload = prepared_payload_findLotIds(states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("states,status,statusDetails",
                         [
                             pytest.param(({"status": "complete"}, {"status": "unsuccessful"}),
                                          marks=pytestrail.case('C8063'))
                         ])
def test_findLotIds_one_lot_in_the_required_state_from_request_is_presented_in_DB(host, port, states, status,
                                                                                  statusDetails,
                                                                                  execute_insert_into_access_tender,
                                                                                  prepared_cpid, prepared_owner,
                                                                                  prepared_entity_id,
                                                                                  prepared_token_entity,
                                                                                  data_two_lots_and_items,
                                                                                  prepared_payload_findLotIds,
                                                                                  data_tender, response,
                                                                                  clear_access_tender_by_cpid):
    lot_id_1, lot_id_2 = prepared_entity_id(), prepared_entity_id()
    json_data = data_tender
    json_data['tender'].update(data_two_lots_and_items)
    json_data['ocid'] = prepared_cpid
    json_data['tender']['lots'][0]['id'] = str(lot_id_1)
    json_data['tender']['lots'][0]['status'] = "complete"
    json_data['tender']['lots'][0]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))
    json_data['tender']['lots'][1]['id'] = str(lot_id_2)
    json_data['tender']['lots'][1]['status'] = "active"
    json_data['tender']['lots'][1]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=json_data,
        owner=prepared_owner
    )
    payload = prepared_payload_findLotIds(*states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [f"{lot_id_1}"]

    assert actualresult == response.success


@pytest.mark.parametrize("states",
                         [
                             pytest.param(({"status": "unsuccessful"}, {"status": "cancelled"}),
                                          marks=pytestrail.case('C8064'),
                                          id='when there are no lots in required states from request in the DB')
                         ])
def test_findLotIds_there_are_two_states_object_in_request(host, port, states,
                                                           execute_insert_into_access_tender,
                                                           prepared_cpid, response,
                                                           prepared_entity_id, prepared_token_entity,
                                                           prepared_owner, prepared_payload_findLotIds,
                                                           data_tender, data_two_lots_and_items,
                                                           clear_access_tender_by_cpid):
    lot_id_1, lot_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data_tender['tender'].update(data_two_lots_and_items)
    json_data = data_tender
    json_data['ocid'] = prepared_cpid

    json_data['tender']['lots'][0]['id'] = lot_id_1
    json_data['tender']['lots'][0]['status'] = "complete"
    json_data['tender']['lots'][0]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))

    json_data['tender']['lots'][1]['id'] = lot_id_2
    json_data['tender']['lots'][1]['status'] = "active"
    json_data['tender']['lots'][1]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=json_data,
        owner=prepared_owner
    )
    payload = prepared_payload_findLotIds(*states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8089')),
                             pytest.param("ocid", marks=pytestrail.case('C8090')),

                         ])
def test_findLotIds_request_does_not_contain_param_in_params(port, host, param,
                                                             prepared_request_id,
                                                             response,
                                                             prepared_payload_findLotIds):
    payload = prepared_payload_findLotIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,states,code,description",
                         [
                             pytest.param("status", {"status": "withdrawn"}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, unsuccessful, complete',"
                                          " actual value: 'withdrawn'.",
                                          marks=pytestrail.case('C8071'),
                                          id='when status:withdrawn'),

                             pytest.param("status", {"status": "", "statusDetails": "empty"}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values. "
                                          "Expected values: 'planning, active, cancelled, unsuccessful,"
                                          " complete', actual value: ''.",
                                          marks=pytestrail.case('C8470'),
                                          id='when status as empty string and statusDetails:empty'),

                             pytest.param("statusDetails", {"status": "active", "statusDetails": ""}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: ''.",
                                          marks=pytestrail.case('C8471'),
                                          id='when status:active and statusDetails as empty string'),

                             pytest.param("status", {"status": ""}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, unsuccessful,"
                                          " complete', actual value: ''.",
                                          marks=pytestrail.case('C8472'),
                                          id='when status as empty string'),

                             pytest.param("statusDetails", {"statusDetails": ""}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: ''.",
                                          marks=pytestrail.case('C8473'),
                                          id='when statusDetails as empty string'),

                             pytest.param("statusDetails", {"statusDetails": "withdrawn"}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: 'withdrawn'.",
                                          marks=pytestrail.case('C8072'),
                                          id='when statusDetails:withdrawn'),

                             pytest.param("status", {"status": "disqualified", "statusDetails": "empty"}, "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'planning, active, cancelled, "
                                          "unsuccessful, complete', actual value: 'disqualified'.",
                                          marks=pytestrail.case('C8073'),
                                          id='when status: disqualified, statusDetails: empty'),

                             pytest.param("statusDetails", {"status": "active", "statusDetails": "disqualified"},
                                          "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'awarded, empty', actual value: 'disqualified'.",
                                          marks=pytestrail.case('C8074'),
                                          id='when status: active, statusDetails: disqualified')
                         ])
def test_findLotIds_request_contains_states(port, host, param, states, code, description, response,
                                            prepared_payload_findLotIds):
    payload = prepared_payload_findLotIds(states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('cpid', "", "DR-5/3",
                                          "Data mismatch to pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: ''.",
                                          marks=pytestrail.case('C8474'), id='cpid as empty string'),
                             pytest.param("ocid", "", "DR-5/3",
                                          "Data mismatch to pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8475'), id='ocid as empty string')
                         ])
def test_findLotIds_data_mismatch_to_pattern(port, host, param, value, code, description, response,
                                             prepared_payload_findLotIds):
    payload = prepared_payload_findLotIds()
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


@pytestrail.case('C8088')
def test_findLotIds_request_does_not_contain_states_array(host, port, execute_insert_into_access_tender, prepared_cpid,
                                                          response, prepared_entity_id, prepared_token_entity,
                                                          prepared_payload_findLotIds, data_tender, prepared_owner,
                                                          clear_access_tender_by_cpid):
    lot_id = str(prepared_entity_id())
    data = data_tender
    data['ocid'] = prepared_cpid
    data['tender']['lots'][0]['id'] = lot_id
    data['tender']['lots'][0]['status'] = "cancelled"
    data['tender']['lots'][0]['statusDetails'] = "empty"
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )
    payload = prepared_payload_findLotIds()
    del payload['params']['states']
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [lot_id]

    assert actualresult == response.success


@pytestrail.case('C8062')
def test_findLotIds_there_two_states_objects_in_request(host, port, execute_insert_into_access_tender, prepared_cpid,
                                                        prepared_entity_id, prepared_token_entity, prepared_owner,
                                                        prepared_payload_findLotIds, data_tender, response,
                                                        clear_access_tender_by_cpid, data_two_lots_and_items):
    states = ({"status": "complete"}, {"status": "active"})
    lot_id_1, lot_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data_tender['tender'].update(data_two_lots_and_items)
    json_data = data_tender
    json_data['ocid'] = prepared_cpid
    json_data['tender']['lots'][0]['id'] = lot_id_1
    json_data['tender']['lots'][0]['status'] = "complete"
    json_data['tender']['lots'][0]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))
    json_data['tender']['lots'][1]['id'] = lot_id_2
    json_data['tender']['lots'][1]['status'] = "active"
    json_data['tender']['lots'][1]['statusDetails'] = random.choice(("unsuccessful", "awarded", "cancelled", "empty"))
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=json_data,
        owner=prepared_owner
    )
    payload = prepared_payload_findLotIds(*states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = [lot_id_1, lot_id_2]

    assert actualresult == response.success


@pytestrail.case('C8648')
def test_findLotIds_request_contains_status_object_instead_of_array_of_objects(port, host, response,
                                                                               prepared_payload_findLotIds):
    payload = prepared_payload_findLotIds()
    payload['params']['states'] = {}
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error["result"] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8964')
def test_findLotIds_request_contain_empty_states_array_of_objects(host, port, response, prepared_payload_findLotIds):
    states = {}
    payload = prepared_payload_findLotIds(states)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-9/3",
            "description": "Object is empty.",
            "details": [{"name": "states"}]
        }
    ]

    assert actualresult == response.error
