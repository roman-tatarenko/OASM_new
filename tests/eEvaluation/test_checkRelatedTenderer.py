import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('cpid', '', "DR-5/7", "Data mismatch to pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                                                " Actual value: ''.", id='cpid as empty string',
                                          marks=pytestrail.case('C13255')),
                             pytest.param('ocid', '', "DR-5/7", "Data mismatch to pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-"
                                                                "[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                                                " Actual value: ''.", id='ocid as empty string',
                                          marks=pytestrail.case('C13256'))
                         ])
def test_checkRelatedTenderer_value_of_param_mismatch_to_the_pattern(host, port, param, value, code, description,
                                                                     payload_checkRelatedTenderer, response):
    payload = payload_checkRelatedTenderer()
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


@pytestrail.case('C13252')
def test_checkRelatedTenderer_an_award_is_not_presented_in_the_DB(host, port, payload_checkRelatedTenderer, response,
                                                                  prepared_entity_id):
    award_id = str(prepared_entity_id())
    payload = payload_checkRelatedTenderer(
        awardId=award_id,
        requirementId=str(prepared_entity_id()),
        relatedTendererId="MD-IDNO-tenderer-id"
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.4.1/7",
            "description": "Award not found.",
            "details": [
                {
                    "id": award_id
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C15087')
def test_checkRelatedTenderer_in_DB_an_award_does_not_contain_array_of_requirement_responses(host, port, prepared_cpid,
                                                                                             payload_checkRelatedTenderer,
                                                                                             response, data_award,
                                                                                             prepared_token_entity,
                                                                                             prepared_owner,
                                                                                             prepared_entity_id,
                                                                                             execute_insert_into_evaluation_award):
    award_id = str(prepared_entity_id())
    related_tenderer_id = "MD-IDNO-tenderer-id"
    data_award['id'] = award_id
    json_data = data_award
    data_award['suppliers'][0]['id'] = related_tenderer_id
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
        relatedTendererId=related_tenderer_id
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13253')
def test_checkRelatedTenderer_tenderer_is_not_linked_to_award(host, port, payload_checkRelatedTenderer,
                                                              prepared_entity_id, data_award,
                                                              execute_insert_into_evaluation_award,
                                                              prepared_cpid, prepared_owner,
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
        relatedTendererId="MD-IDNO-tenderer-id"
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.4.2/7",
            "description": "Tenderer is not linked to award."
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C13254')
def test_checkRelatedTenderer_requirement_response_for_the_relevant_requirement_and_the_tenderer_has_been_created_before(
        host, port, payload_checkRelatedTenderer, execute_insert_into_evaluation_award, response, prepared_entity_id,
        data_award, prepared_cpid, prepared_token_entity, prepared_owner, data_requirementResponse
):
    award_id = str(prepared_entity_id())
    related_tenderer_id = "MD-IDNO-tenderer-id"
    requirement_id = str(prepared_entity_id())

    data_award['id'] = award_id
    data_award['suppliers'][0]['id'] = related_tenderer_id

    data_requirementResponse['relatedTenderer']['id'] = related_tenderer_id
    data_requirementResponse['relatedTenderer']['requirement'] = related_tenderer_id

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

    assert actualresult == response.error
