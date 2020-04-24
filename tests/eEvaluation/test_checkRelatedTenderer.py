from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C15087')
def test_checkRelatedTenderer_award_does_not_contains_array_of_requirement_responses(host, port,
                                                                                     payload_checkRelatedTenderer,
                                                                                     execute_insert_into_evaluation_award,
                                                                                     response, prepared_owner,
                                                                                     prepared_entity_id, data_award,
                                                                                     prepared_cpid,
                                                                                     prepared_tenderer_id,
                                                                                     prepared_token_entity,
                                                                                     data_requirementResponse):
    award_id = str(prepared_entity_id())
    requirement_id = str(prepared_entity_id())
    related_tenderer_id = prepared_tenderer_id()

    data_award['id'] = award_id
    data_award['suppliers'][0]['id'] = related_tenderer_id

    json_data = data_award
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=json_data,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=requirement_id,
        relatedTendererId=related_tenderer_id
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C16732')
def test_checkRelatedTenderer_with_requirement_response_for_two_tenderer_for_one_requirement(host, port,
                                                                                             payload_checkRelatedTenderer,
                                                                                             execute_insert_into_evaluation_award,
                                                                                             response,
                                                                                             prepared_entity_id,
                                                                                             data_award, data_supplier,
                                                                                             prepared_cpid,
                                                                                             prepared_tenderer_id,
                                                                                             prepared_token_entity,
                                                                                             prepared_owner,
                                                                                             data_requirementResponse):
    award_id, requirement_id = [str(prepared_entity_id()) for _ in range(2)]
    related_tenderer_ids = [prepared_tenderer_id() for _ in range(2)]

    data_award.update({"requirementResponses": [data_requirementResponse]})
    data_award['suppliers'].append(data_supplier)

    data_award['id'] = award_id
    data_award['suppliers'][0]['id'] = related_tenderer_ids[0]
    data_award['suppliers'][0]['id'] = related_tenderer_ids[1]
    data_requirementResponse['relatedTenderer']['id'] = related_tenderer_ids[0]
    data_requirementResponse['requirement']['id'] = requirement_id

    json_data = data_award
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=json_data,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=requirement_id,
        relatedTendererId=related_tenderer_ids[1]
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13254')
def test_checkRelatedTenderer_duplicate_requirement_response(host, port, payload_checkRelatedTenderer,
                                                             execute_insert_into_evaluation_award, response,
                                                             prepared_entity_id, data_award, prepared_cpid,
                                                             prepared_token_entity, prepared_owner,
                                                             data_requirementResponse, prepared_tenderer_id):
    award_id = str(prepared_entity_id())
    requirement_id = str(prepared_entity_id())
    related_tenderer_id = prepared_tenderer_id()

    data_award['id'] = award_id
    data_award['suppliers'][0]['id'] = related_tenderer_id

    data_requirementResponse['relatedTenderer']['id'] = related_tenderer_id
    data_requirementResponse['requirement']['id'] = requirement_id

    data_award.update({"requirementResponses": [data_requirementResponse]})

    json_data = data_award
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=json_data,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=requirement_id,
        relatedTendererId=related_tenderer_id
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "VR-10.4.4.3/7",
        "description": "Duplicate requirement response."
    }]

    assert actualresult == response.error


@pytestrail.case('C13253')
def test_checkRelatedTenderer_tenderer_is_not_linked_to_award(host, port, payload_checkRelatedTenderer,
                                                              prepared_entity_id, data_award,
                                                              execute_insert_into_evaluation_award,
                                                              prepared_cpid, prepared_owner, prepared_tenderer_id,
                                                              prepared_token_entity, response):
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    json_data = data_award
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=prepared_token_entity,
        json_data=json_data,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=str(prepared_entity_id()),
        relatedTendererId=prepared_tenderer_id()
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.4.2/7",
            "description": "Tenderer is not linked to award."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-0000000000000",
                                          marks=pytestrail.case('C13252'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-0000000000000-AC-0000000000000",
                                          marks=pytestrail.case('C16590'),
                                          id="by stage"),

                             pytest.param("awardId", f"{uuid4()}",
                                          marks=pytestrail.case('C16637'),
                                          id="by award.id"),

                         ])
def test_checkRelatedTenderer_award_not_found(host, port, param, value, payload_checkRelatedTenderer,
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


@pytest.mark.parametrize("param",
                         [
                             pytest.param('cpid', marks=pytestrail.case('C16796')),
                             pytest.param('ocid', marks=pytestrail.case('C16801')),
                             pytest.param('awardId', marks=pytestrail.case('C16802')),
                             pytest.param('requirementId', marks=pytestrail.case('C16803')),
                             pytest.param('relatedTendererId', marks=pytestrail.case('C16804'))
                         ])
def test_checkRelatedTenderer_request_does_not_contains_param(host, port, param, payload_checkRelatedTenderer,
                                                              response):
    payload = payload_checkRelatedTenderer()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'RQ-1/7',
            'description': "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,description",
                         [
                             pytest.param('cpid', '', "Data mismatch of attribute 'cpid' to the pattern:"
                                                      " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                                      " Actual value: ''.",
                                          marks=pytestrail.case('C13255'),
                                          id='cpid as empty string'),

                             pytest.param('ocid', '', "Data mismatch of attribute 'ocid' to the pattern:"
                                                      " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-"
                                                      "[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                                      " Actual value: ''.",
                                          marks=pytestrail.case('C13256'),
                                          id='ocid as empty string')
                         ])
def test_checkRelatedTenderer_value_of_param_mismatch_to_the_pattern(host, port, param, value, description,
                                                                     payload_checkRelatedTenderer, response):
    payload = payload_checkRelatedTenderer()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-5/7",
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,description",
                         [
                             pytest.param('awardId', '',
                                          "Data format mismatch of attribute 'awardId'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C16805'),
                                          id='awarId as empty string'),

                             pytest.param('requirementId', '',
                                          "Data format mismatch of attribute 'requirementId'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C16806'),
                                          id='requirementId as empty string')
                         ])
def test_checkRelatedTenderer_data_format_mismatch_of_attribute(host, port, param, value, description,
                                                                payload_checkRelatedTenderer, response):
    payload = payload_checkRelatedTenderer()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-4/7",
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error
