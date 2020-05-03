from datetime import datetime
from random import randint

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C16941')
def test_findCANIds_without_search_params(port, host, payload_findCANIds, prepared_entity_id,
                                          execute_insert_into_contracting_can, prepared_cpid,
                                          clear_contracting_can_by_cpid):
    can_ids = [prepared_entity_id() for _ in range(randint(1, 10))]

    for can_id in can_ids:
        execute_insert_into_contracting_can(
            cp_id=prepared_cpid,
            can_id=can_id,
            award_id=prepared_entity_id(),
            created_date=datetime.now(),
            lot_id=prepared_entity_id(),
            status='pending',
            status_details='active',
            token_entity=prepared_entity_id(),
            owner=prepared_entity_id(),
        )
    payload = payload_findCANIds()
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()

    actualresult['result'].sort()
    can_ids.sort()

    assert actualresult['status'] == "success"
    assert actualresult['result'] == [str(can_id) for can_id in can_ids]


@pytestrail.case('C16942')
def test_findCANIds_without_search_params_and_without_record(port, host, payload_findCANIds, response):
    payload = payload_findCANIds()
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C16943')
@pytest.mark.parametrize('status', ('pending', 'unsuccessful', 'active', 'cancelled'))
@pytest.mark.parametrize('status_details', ('contractProject', 'unsuccessful', 'empty', 'active'))
def test_findCANIds_by_states(port, host, status, status_details, payload_findCANIds,
                              prepared_cpid, prepared_entity_id, response,
                              execute_insert_into_contracting_can, clear_contracting_can_by_cpid):
    can_id = prepared_entity_id()

    execute_insert_into_contracting_can(
        cp_id=prepared_cpid,
        can_id=can_id,
        award_id=prepared_entity_id(),
        created_date=datetime.now(),
        lot_id=prepared_entity_id(),
        status=status,
        status_details=status_details,
        token_entity=prepared_entity_id(),
        owner=prepared_entity_id(),
    )
    payload = payload_findCANIds(
        status=status,
        statusDetails=status_details
    )
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    response.success['result'] = [str(can_id)]

    assert actualresult == response.success


@pytestrail.case('C16944')
@pytest.mark.parametrize('status', ('pending', 'unsuccessful', 'active', 'cancelled'))
def test_findCANIds_by_states_status(port, host, status, payload_findCANIds, prepared_cpid, prepared_entity_id,
                                     response, execute_insert_into_contracting_can, clear_contracting_can_by_cpid):
    can_id = prepared_entity_id()

    execute_insert_into_contracting_can(
        cp_id=prepared_cpid,
        can_id=can_id,
        award_id=prepared_entity_id(),
        created_date=datetime.now(),
        lot_id=prepared_entity_id(),
        status=status,
        status_details="empty",
        token_entity=prepared_entity_id(),
        owner=prepared_entity_id(),
    )
    payload = payload_findCANIds(
        status=status
    )
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    response.success['result'] = [str(can_id)]

    assert actualresult == response.success


@pytestrail.case('C16945')
@pytest.mark.parametrize('status_details', ('contractProject', 'unsuccessful', 'empty', 'active'))
def test_findCANIds_by_states_statusDetails(port, host, status_details, payload_findCANIds,
                                            prepared_cpid, prepared_entity_id, response,
                                            execute_insert_into_contracting_can, clear_contracting_can_by_cpid):
    can_id = prepared_entity_id()

    execute_insert_into_contracting_can(
        cp_id=prepared_cpid,
        can_id=can_id,
        award_id=prepared_entity_id(),
        created_date=datetime.now(),
        lot_id=prepared_entity_id(),
        status='active',
        status_details=status_details,
        token_entity=prepared_entity_id(),
        owner=prepared_entity_id(),
    )
    payload = payload_findCANIds(
        statusDetails=status_details
    )
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    response.success['result'] = [str(can_id)]

    assert actualresult == response.success


@pytestrail.case('C16946')
def test_findCANIds_by_lotId(port, host, payload_findCANIds, prepared_cpid, prepared_entity_id,
                             execute_insert_into_contracting_can, clear_contracting_can_by_cpid):
    quantity = randint(1, 100)
    can_ids = [prepared_entity_id() for _ in range(quantity)]
    lot_ids = [str(prepared_entity_id()) for _ in range(quantity)]

    for i in range(quantity):
        execute_insert_into_contracting_can(
            cp_id=prepared_cpid,
            can_id=can_ids[i],
            award_id=prepared_entity_id(),
            created_date=datetime.now(),
            lot_id=lot_ids[i],
            status="active",
            status_details="empty",
            token_entity=prepared_entity_id(),
            owner=prepared_entity_id(),
        )
    payload = payload_findCANIds(
        *lot_ids
    )
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()

    actualresult['result'].sort()
    can_ids.sort()

    assert actualresult['status'] == "success"
    assert actualresult['result'] == [str(can_id) for can_id in can_ids]


@pytestrail.case('C16947')
@pytest.mark.parametrize('status', ('pending', 'unsuccessful', 'active', 'cancelled'))
@pytest.mark.parametrize('status_details', ('contractProject', 'unsuccessful', 'empty', 'active'))
def test_findCANIds_by_lotId_and_states(port, host, status, status_details, payload_findCANIds,
                                        prepared_cpid, prepared_entity_id, execute_insert_into_contracting_can,
                                        clear_contracting_can_by_cpid):
    quantity = randint(1, 10)
    can_ids = [prepared_entity_id() for _ in range(quantity)]
    lot_ids = [str(prepared_entity_id()) for _ in range(quantity)]

    for i in range(quantity):
        execute_insert_into_contracting_can(
            cp_id=prepared_cpid,
            can_id=can_ids[i],
            award_id=prepared_entity_id(),
            created_date=datetime.now(),
            lot_id=lot_ids[i],
            status=status,
            status_details=status_details,
            token_entity=prepared_entity_id(),
            owner=prepared_entity_id(),
        )
    payload = payload_findCANIds(
        lot_ids[0],
        status=status,
        statusDetails=status_details,
    )
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()

    assert actualresult['status'] == "success"
    assert actualresult['result'] == [str(can_ids[0])]


@pytestrail.case('C16948')
def test_findCANIds_by_two_states(port, host, payload_findCANIds,
                                  prepared_cpid, prepared_entity_id,
                                  execute_insert_into_contracting_can,
                                  clear_contracting_can_by_cpid):
    quantity = 3
    states = [('pending', 'contractProject'), ('active', 'unsuccessful'), ('cancelled', 'empty')]
    can_ids = [prepared_entity_id() for _ in range(quantity)]
    lot_ids = [str(prepared_entity_id()) for _ in range(quantity)]

    for i in range(quantity):
        execute_insert_into_contracting_can(
            cp_id=prepared_cpid,
            can_id=can_ids[i],
            award_id=prepared_entity_id(),
            created_date=datetime.now(),
            lot_id=lot_ids[i],
            status=states[i][0],
            status_details=states[i][1],
            token_entity=prepared_entity_id(),
            owner=prepared_entity_id(),
        )
    payload = payload_findCANIds()
    payload['params']['states'] = [
        {'status': states[0][0]},
        {'statusDetails': states[1][1]}
    ]
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()

    del can_ids[2]
    actualresult['result'].sort()
    can_ids.sort()

    assert actualresult['status'] == "success"
    assert actualresult['result'] == [str(can_id) for can_id in can_ids]


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C16949')),
                             pytest.param("ocid", marks=pytestrail.case('C16950'))
                         ])
def test_findCANIds_without_required_param(port, host, param, payload_findCANIds, response):
    payload = payload_findCANIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'RQ-1/9',
            'description': "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C16951')
def test_findCANIds_with_param_lotIds_as_empty_array(port, host, payload_findCANIds, response):
    payload = payload_findCANIds()
    payload['params']['lotIds'] = []
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'DR-10/9',
            'description': "Attribute 'lotIds' is an empty array.",
            'details': [{'name': 'lotIds'}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.xfail(reason='Internal Server Error')
@pytestrail.case('C16952')
def test_findCANIds_with_lotId_null(port, host, payload_findCANIds, response):
    payload = payload_findCANIds()
    payload['params']['lotIds'] = [None]
    actualresult = requests.post(f'{host}:{port.eContracting}/command2', json=payload).json()
    # {'timestamp': '2020-05-02T23:07:24.246+0000',
    # 'status': 500, 'error': 'Internal Server Error',
    # 'message': 'Parameter specified as non-null is null:
    # method com.procurement.contracting.application.
    # model.can.FindCANIdsParams$Companion$tryCreate$lotIdsParsed$1.invoke, parameter lotId',
    # 'path': '/command2'}
    assert actualresult['status'] != 500
    assert actualresult['status'] == 'error'
