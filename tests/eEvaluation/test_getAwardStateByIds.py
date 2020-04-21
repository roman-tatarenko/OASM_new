from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C13188')
def test_getAwardStateByIds_the_award_is_present_in_DB(port, host, data_award, payload_getAwardStateByIds, response,
                                                       execute_insert_into_evaluation_award, prepared_cpid,
                                                       prepared_entity_id, prepared_owner):
    award_id = str(prepared_entity_id())
    data_award['id'] = award_id
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=uuid4(),
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_getAwardStateByIds(award_id)
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": award_id,
            "status": "pending",
            "statusDetails": "awaiting"
        }
    ]

    assert actualresult == response.success


@pytestrail.case('C13190')
def test_getAwardStateByIds_two_awards_is_present_in_DB(port, host, data_award, payload_getAwardStateByIds, response,
                                                        execute_insert_into_evaluation_award, prepared_cpid,
                                                        prepared_entity_id, prepared_owner):
    award_id_1, award_id_2 = str(prepared_entity_id()), str(prepared_entity_id())
    data_award['id'] = award_id_1
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=uuid4(),
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    data_award['id'] = award_id_2
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=uuid4(),
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    payload = payload_getAwardStateByIds(award_id_1, award_id_2)
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.success['result'] = [
        {
            "id": award_id_1,
            "status": "pending",
            "statusDetails": "awaiting"
        },
        {
            "id": award_id_2,
            "status": "pending",
            "statusDetails": "awaiting"
        }
    ]

    assert all(item in response.success['result'] for item in actualresult['result'])


@pytestrail.case('C13189')
def test_getAwardStateByIds_one_award_is_not_present_in_DB(port, host, data_award, payload_getAwardStateByIds, response,
                                                           execute_insert_into_evaluation_award, prepared_cpid,
                                                           prepared_entity_id, prepared_owner):
    award_id_db = str(prepared_entity_id())
    data_award['id'] = award_id_db
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=uuid4(),
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    award_id_random = str(prepared_entity_id())
    payload = payload_getAwardStateByIds(award_id_db, award_id_random)
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.1.1/7",
            "description": "Award not found.",
            "details": [{"id": award_id_random}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-9999999999999",
                                          marks=pytestrail.case('C13244'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-9999999999999-EV-9999999999999",
                                          marks=pytestrail.case('C16300'),
                                          id="by ocid"),
                             # None for array awardIds.
                             pytest.param(None, None,
                                          marks=pytestrail.case('C13243'),
                                          id="by awardId")
                         ])
def test_getAwardStateByIds_the_award_is_not_present_in_DB(port, host, param, value, data_award, prepared_entity_id,
                                                           payload_getAwardStateByIds, response, prepared_owner,
                                                           execute_insert_into_evaluation_award, prepared_cpid):
    execute_insert_into_evaluation_award(
        cp_id=prepared_cpid,
        stage='EV',
        token_entity=uuid4(),
        json_data=data_award,
        owner=prepared_owner,
        status='pending',
        status_details='awaiting'
    )
    award_id = str(prepared_entity_id())
    payload = payload_getAwardStateByIds(award_id)
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.4.1.1/7",
            "description": "Award not found.",
            "details": [{"id": award_id}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C16298')),

                             pytest.param("ocid",
                                          marks=pytestrail.case('C16297')),

                             pytest.param("awardIds",
                                          marks=pytestrail.case('C16296'))
                         ])
def test_getAwardStateByIds_without_param_in_params(port, host, param, payload_getAwardStateByIds, response):
    payload = payload_getAwardStateByIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/7",
            "description": "Error parsing 'params'"

        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("awardIds", "",
                                          marks=pytestrail.case("C13191"),
                                          id="awardIds as empty string")

                         ])
def test_getAwardStateByIds_data_type_mismatch_of_attribute_awardIds(port, host, param, value,
                                                                     payload_getAwardStateByIds, response):
    payload = payload_getAwardStateByIds()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/7",
            "description": "Error parsing 'params'"

        }
    ]
    assert actualresult == response.error


@pytestrail.case("C16301")
def test_getAwardStateByIds_attribute_awardIds_as_empty_array(port, host, payload_getAwardStateByIds, response):
    payload = payload_getAwardStateByIds()
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-10/7",
            "description": "Attribute 'awardIds' is an empty array.",
            "details": [{"name": "awardIds"}]
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C16302")
def test_getAwardStateByIds_param_awardId_mismatch_to_the_pattern(port, host, payload_getAwardStateByIds,
                                                                  response):
    payload = payload_getAwardStateByIds("")
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-4/7",
            "description": "Data format mismatch of attribute 'awardIds'."
                           " Expected data format: 'uuid', actual value: ''.",
            "details": [{"name": "awardIds"}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [

                             pytest.param("cpid", "", "DR-5/7",
                                          "Data mismatch of attribute 'cpid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: ''.",
                                          marks=pytestrail.case("C13193"),
                                          id="cpid as empty string")
                         ])
def test_getAwardStateByIds_param_cpid_mismatch_to_the_pattern(port, host, param, value, code, description,
                                                               payload_getAwardStateByIds, response,
                                                               prepared_entity_id):
    payload = payload_getAwardStateByIds(str(prepared_entity_id()))
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
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
                             pytest.param("ocid", "", "DR-5/7",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: ''.",
                                          marks=pytestrail.case("C13192"),
                                          id="ocid as empty string")
                         ])
def test_getAwardStateByIds_param_ocid_mismatch_to_the_pattern(port, host, param, value, code, description,
                                                               payload_getAwardStateByIds, prepared_entity_id,
                                                               response):
    payload = payload_getAwardStateByIds(str(prepared_entity_id()))
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]

    assert actualresult == response.error
