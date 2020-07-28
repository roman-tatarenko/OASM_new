from datetime import datetime

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C16559')
def test_getTenderState_get_tender_state_by_cpid_and_stage(port, host, data_tender, execute_insert_into_access_tender,
                                                           payload_getTenderState, prepared_cpid, prepared_owner,
                                                           prepared_token_entity, response):
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data_tender,
        owner=prepared_owner
    )
    payload = payload_getTenderState()
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "status": "active",
        "statusDetails": "clarification"
    }

    assert actualresult == response.success


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-0000000000000",
                                          marks=pytestrail.case('C16560'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-0000000000000-AC-0000000000000",
                                          marks=pytestrail.case('C16561'),
                                          id="by ocid"),

                         ])
def test_getTenderState_tender_not_found(port, host, param, value, data_tender, execute_insert_into_access_tender,
                                         payload_getTenderState, prepared_cpid, prepared_owner,
                                         prepared_token_entity,
                                         response):
    execute_insert_into_access_tender(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data_tender,
        owner=prepared_owner
    )
    payload = payload_getTenderState()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'VR-10.1.8.1/3',
            'description': f"Tender not found by cpid '{payload['params']['cpid']}' "
                           f"and ocid '{payload['params']['ocid']}'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C16562')
@pytest.mark.parametrize('value', ('', 1))
def test_getTenderState_cpid_mismatch_to_the_pattern(port, host, value,
                                                     payload_getTenderState, response):
    payload = payload_getTenderState(cpid=value)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-5/3",
            "description": "Data mismatch to pattern: "
                           "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                           f" Actual value: '{value}'.",
            "details": [{"name": "cpid"}]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C16563')
@pytest.mark.parametrize('value', ('', 1))
def test_getTenderState_ocid_mismatch_to_the_pattern(port, host, value, payload_getTenderState, response):
    payload = payload_getTenderState(ocid=value)
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-5/3",
            "description": "Data mismatch to pattern: "
                           "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                           f" Actual value: '{value}'.",
            "details": [{"name": "ocid"}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C16564')),

                             pytest.param("ocid",
                                          marks=pytestrail.case('C16565'))
                         ])
def test_getTenderState_request_does_not_contains_param(port, host, param, payload_getTenderState, response):
    payload = payload_getTenderState()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'RQ-02/3',
            'description': "Can not parse 'params'."
        }
    ]
    assert actualresult == response.error
