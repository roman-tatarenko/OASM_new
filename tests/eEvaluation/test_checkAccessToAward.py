from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C10470')
def test_checkAccessToAward_a_request_contains_param_values_which_are_presented_in_DB(port, host, data_award,
                                                                                      payload_checkAccessToAward,
                                                                                      prepared_cpid, prepared_owner,
                                                                                      prepared_token_entity,
                                                                                      prepared_entity_id, response,
                                                                                      execute_insert_into_evaluation_award):
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    data_award['token'] = str(prepared_token_entity)

    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkAccessToAward(awardId=award_id)
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("token", uuid4(), "VR-10.4.2.1/7",
                                          "Request token doesn't match token from the database.",
                                          marks=pytestrail.case('C10471'),
                                          id="token"),

                             pytest.param("owner", uuid4(), "VR-10.4.2.2/7",
                                          "Request owner doesn't match owner from the database.",
                                          marks=pytestrail.case('C10472'),
                                          id="owner")
                         ])
def test_checkAccessToAward_a_request_contains_invalid(port, host, data_award, param, value, code, description,
                                                       payload_checkAccessToAward, prepared_cpid, prepared_owner,
                                                       prepared_token_entity, prepared_entity_id, response,
                                                       execute_insert_into_evaluation_award):
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    data_award['token'] = str(prepared_token_entity)
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkAccessToAward(award_id)
    payload['params'][param] = str(value)
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    response.error['result'] = [{
        "code": code,
        "description": description
    }]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-0000000000000",
                                          marks=pytestrail.case('C10474'),
                                          id="by cpid"),

                             pytest.param("awardId", str(uuid4()),
                                          marks=pytestrail.case('C10473'),
                                          id="by awardId")
                         ])
def test_checkAccessToAward_award_is_not_present_in_DB(port, host, payload_checkAccessToAward, param, value,
                                                       prepared_entity_id, data_award, prepared_token_entity,
                                                       prepared_cpid, prepared_owner,
                                                       execute_insert_into_evaluation_award, response):
    award_id = str(prepared_entity_id())
    data_award['id'] = str(prepared_entity_id())
    data_award['token'] = str(prepared_token_entity)
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkAccessToAward(awardId=award_id)
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.2.3/7",
            "description": "Award not found.",
            "details": [{"id": payload['params']['awardId']}]
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C12516')),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C12517')),
                             pytest.param("token",
                                          marks=pytestrail.case('C12518')),
                             pytest.param("owner",
                                          marks=pytestrail.case('C12519')),
                             pytest.param("awardId",
                                          marks=pytestrail.case('C12520')),

                         ])
def test_checkAccessToAward_a_request_does_not_contain(port, host, param, payload_checkAccessToAward, response):
    payload = payload_checkAccessToAward()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/7",
            "description": "Error parsing 'params'"
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('cpid', '', "DR-5/7", "Data mismatch of attribute 'cpid' to the pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                                                " Actual value: ''.",
                                          id='cpid as empty string',
                                          marks=pytestrail.case('C16392')),

                             pytest.param('ocid', '', "DR-5/7", "Data mismatch of attribute 'ocid' to the pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-"
                                                                "[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                                                " Actual value: ''.",
                                          id='ocid as empty string',
                                          marks=pytestrail.case('C14101')),

                             pytest.param('token', '', "DR-4/7", "Data format mismatch of attribute 'token'."
                                                                 " Expected data format: 'uuid', actual value: ''.",
                                          id='token as empty string',
                                          marks=pytestrail.case('C14101'))
                         ])
def test_checkAccessToAward_mismatch_to_the_pattern(host, port, param, value, code, description,
                                                    payload_checkAccessToAward, response):
    payload = payload_checkAccessToAward()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('token', '', "DR-4/7", "Data format mismatch of attribute 'token'."
                                                                 " Expected data format: 'uuid', actual value: ''.",
                                          id='token as empty string',
                                          marks=pytestrail.case('C16396')),

                             pytest.param('owner', '', "DR-4/7", "Data format mismatch of attribute 'owner'."
                                                                 " Expected data format: 'uuid', actual value: ''.",
                                          id='owner as empty string',
                                          marks=pytestrail.case('C16397')),

                             pytest.param('awardId', '', "DR-4/7", "Data format mismatch of attribute 'awardId'."
                                                                   " Expected data format: 'uuid', actual value: ''.",
                                          id='awardId as empty string',
                                          marks=pytestrail.case('C16398')),
                         ])
def test_checkAccessToAward_data_format_mismatch_of_attribute(host, port, param, value, code, description,
                                                              payload_checkAccessToAward, response):
    payload = payload_checkAccessToAward()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error
