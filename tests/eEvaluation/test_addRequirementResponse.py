import json
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail

from resources.domain.requirementResponse import schema_requirementResponse


@pytestrail.case('C13260')
def test_addRequirementResponse_add_first_requirementResponse(port, host, execute_insert_into_evaluation_award,
                                                              execute_select_evaluation_award_by_token_entity,
                                                              payload_addRequirementResponse, prepared_cpid,
                                                              prepared_token_entity, data_award, prepared_owner,
                                                              prepared_entity_id, response):
    stage = 'EV'
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage=stage,
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_addRequirementResponse(
        award_id=award_id,
        requirementResponse_id=prepared_entity_id(),
        relatedTenderer_id=prepared_entity_id(),
        requirement_id=prepared_entity_id()
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success

    record = execute_select_evaluation_award_by_token_entity(
        cp_id=prepared_cpid,
        stage=stage,
        token_entity=prepared_token_entity
    ).one()
    award = json.loads(record.json_data)

    assert award['requirementResponses'][0] == payload['params']['award']['requirementResponse']


@pytestrail.case('C16841')
def test_addRequirementResponse_add_two_requirementResponse(port, host, execute_insert_into_evaluation_award,
                                                            execute_select_evaluation_award_by_token_entity,
                                                            payload_addRequirementResponse, prepared_cpid,
                                                            prepared_token_entity, data_award, prepared_owner,
                                                            prepared_entity_id, response):
    stage = 'EV'
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    data_award.update({"requirementResponses": [schema_requirementResponse]})

    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage=stage,
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_addRequirementResponse(
        award_id=award_id,
        requirementResponse_id=prepared_entity_id(),
        relatedTenderer_id=prepared_entity_id(),
        requirement_id=prepared_entity_id()
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success

    record = execute_select_evaluation_award_by_token_entity(
        cp_id=prepared_cpid,
        stage=stage,
        token_entity=prepared_token_entity
    ).one()
    actual_award = json.loads(record.json_data)

    assert actual_award['requirementResponses'][1] == payload['params']['award']['requirementResponse']


@pytest.mark.parametrize("name,param,value,code,description",
                         [
                             pytest.param('awardId', 'id', '', "DR-4/7",
                                          "Data format mismatch of attribute 'awardId'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          id='awardId as empty string',
                                          marks=pytestrail.case('C13266'))
                         ])
def test_addRequirementResponse_data_format_mismatch_of_attribute_awardId(port, host, name, param, value, code,
                                                                          description,
                                                                          prepared_entity_id,
                                                                          payload_addRequirementResponse, response):
    payload = payload_addRequirementResponse(
        award_id=prepared_entity_id(),
        requirementResponse_id=prepared_entity_id(),
        relatedTenderer_id=prepared_entity_id(),
        requirement_id=prepared_entity_id()
    )
    payload['params']['award'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": name
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("name,param,value,code,description",
                         [
                             pytest.param('requirementResponseId', 'id', '', "DR-4/7",
                                          "Data format mismatch of attribute 'requirementResponseId'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          id='awardId as empty string',
                                          marks=pytestrail.case('C13267'))
                         ])
def test_addRequirementResponse_data_format_mismatch_of_attribute_requirementResponse_id(port, host, name, param, value,
                                                                                         code, description,
                                                                                         prepared_entity_id,
                                                                                         payload_addRequirementResponse,
                                                                                         response):
    payload = payload_addRequirementResponse(
        award_id=prepared_entity_id(),
        requirementResponse_id=prepared_entity_id(),
        relatedTenderer_id=prepared_entity_id(),
        requirement_id=prepared_entity_id()
    )
    payload['params']['award']['requirementResponse'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": name
                }
            ]
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("name,param,value,code,description",
                         [
                             pytest.param('requirementId', 'id', '', "DR-4/7",
                                          "Data format mismatch of attribute 'requirementId'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          id='awardId as empty string',
                                          marks=pytestrail.case('C13268'))
                         ])
def test_addRequirementResponse_data_format_mismatch_of_attribute_requirement_id(port, host, name, param, value, code,
                                                                                 description,
                                                                                 prepared_entity_id,
                                                                                 payload_addRequirementResponse,
                                                                                 response):
    payload = payload_addRequirementResponse(
        award_id=prepared_entity_id(),
        requirementResponse_id=prepared_entity_id(),
        relatedTenderer_id=prepared_entity_id(),
        requirement_id=prepared_entity_id()
    )
    payload['params']['award']['requirementResponse']['requirement'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": name
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-0000000000000",
                                          marks=pytestrail.case('C13261'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-0000000000000-AC-0000000000000",
                                          marks=pytestrail.case('C16840'),
                                          id="by stage"),

                             pytest.param("awardId", f"{uuid4()}",
                                          marks=pytestrail.case('C13269'),
                                          id="by identifier"),

                         ])
def test_addRequirementResponse_award_not_found(host, port, param, value, payload_checkRelatedTenderer,
                                                response, execute_insert_into_evaluation_award,
                                                prepared_entity_id, prepared_cpid, prepared_tenderer_id,
                                                prepared_token_entity, data_award, prepared_owner):
    award_id = str(prepared_entity_id())
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=str(prepared_entity_id()),
        relatedTendererId=prepared_tenderer_id()
    )
    print(award_id)
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.4.1/7",
            "description": "Award not found.",
            "details": [
                {
                    "id": payload['params']['awardId']
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C13262')
@pytest.mark.parametrize('value', ('', 1))
def test_addRequirementResponse_cpid_mismatch_to_the_pattern(port, host, value,
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


@pytestrail.case('C13263')
@pytest.mark.parametrize('value', ('', 1))
def test_addRequirementResponse_ocid_mismatch_to_the_pattern(port, host, value, payload_getTenderState, response):
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
