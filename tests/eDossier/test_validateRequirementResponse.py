import pytest
from pytest_testrail.plugin import pytestrail
import requests
from uuid import uuid4


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("number", 22.3,
                                          marks=pytestrail.case("C14118"),
                                          id="value dataType is number"),

                             pytest.param("integer", 22,
                                          marks=pytestrail.case("C14119"),
                                          id="value dataType is integer"),

                             pytest.param("boolean", False,
                                          marks=pytestrail.case("C14120"),
                                          id="value dataType is boolean"),

                             pytest.param("string", "30",
                                          marks=pytestrail.case("C14121"),
                                          id="value dataType is string")

                         ])
def test_validateRequirementResponse_check_of_the_validation(host, port, execute_insert_into_dossier_tenders,
                                                             prepared_cpid, data_create_criteria, prepared_owner,
                                                             payload_validateRequirementResponse, response, param,
                                                             value, ):
    data = data_create_criteria
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['dataType'] = param
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id'] = str(uuid4())
    requirement_id = data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id']
    execute_insert_into_dossier_tenders(
        cp_id=prepared_cpid,
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_validateRequirementResponse(
        value=value,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case("C16318")
def test_validateRequirementResponse_cpid_does_not_present_in_DB(host, port, payload_validateRequirementResponse,
                                                                 response, prepared_cpid):
    payload = payload_validateRequirementResponse(
        cpid=prepared_cpid
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.3/19",
            "description": "Requirements not found by cpid '" + str(prepared_cpid) + "'.",
        }
    ]
    assert actualresult == response.error


@pytestrail.case("C14122")
def test_validateRequirementResponse_requirement_does_not_present_in_DB(host, port, data_create_criteria,
                                                                        execute_insert_into_dossier_tenders,
                                                                        prepared_owner, prepared_cpid,
                                                                        payload_validateRequirementResponse,
                                                                        response):
    cpid = prepared_cpid
    requirement_id = str(uuid4())
    data = data_create_criteria
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=prepared_owner
    )
    payload = payload_validateRequirementResponse(
        cpid=cpid,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.1/19",
            "description": "Requirement with id '" + requirement_id + "' not found.",
            "details": [
                {
                    "id": requirement_id
                }
            ]
        }
    ]
    assert actualresult == response.error


@pytestrail.case("C14124")
def test_validateRequirementResponse_requirement_as_award_criteria_price_only(host, port,
                                                                              data_create_criteria,
                                                                              execute_insert_into_dossier_tenders,
                                                                              prepared_owner, prepared_cpid,
                                                                              payload_validateRequirementResponse,
                                                                              response):
    cpid = prepared_cpid
    requirement_id = str(uuid4())
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data={"awardCriteria": "priceOnly", "awardCriteriaDetails": "automated"},
        owner=prepared_owner
    )
    payload = payload_validateRequirementResponse(
        cpid=cpid,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.3/19",
            "description": "Requirements not found by cpid '" + str(prepared_cpid) + "'.",
        }
    ]
    assert actualresult == response.error


@pytestrail.case("C14123")
def test_validateRequirementResponse_dataType_mismatch_for_requirement(host, port, execute_insert_into_dossier_tenders,
                                                                       prepared_cpid, data_create_criteria,
                                                                       prepared_owner,
                                                                       payload_validateRequirementResponse, response):
    cpid = prepared_cpid
    data = data_create_criteria
    requirement = data['criteria'][0]['requirementGroups'][0]['requirements'][0]
    requirement['dataType'] = "boolean"
    requirement['id'] = str(uuid4())
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id'] = str(uuid4())
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_validateRequirementResponse(
        cpid=cpid,
        value=22.9,
        requirement_id=requirement['id']
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.2/19",
            "description": "Data type mismatch. Expected data type: 'boolean', actual data type: 'number'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C14125")
def test_validateRequirementResponse_unexpected_criteria_source(host, port, execute_insert_into_dossier_tenders,
                                                                prepared_cpid, prepared_owner,
                                                                data_create_two_criteria_and_conversion,
                                                                payload_validateRequirementResponse, response):
    cpid = prepared_cpid
    data = data_create_two_criteria_and_conversion
    data['criteria'][0]['source'] = "tenderer"
    data['criteria'][1]['source'] = "procuringEntity"
    requirement_1 = data['criteria'][0]['requirementGroups'][0]['requirements'][0]
    requirement_2 = data['criteria'][1]['requirementGroups'][0]['requirements'][0]
    requirement_1['dataType'], requirement_2['dataType'] = "integer", "boolean"
    requirement_1['id'], requirement_2['id'] = [str(uuid4()) for _ in range(2)]

    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_validateRequirementResponse(
        cpid=cpid,
        value=22,
        requirement_id=requirement_1['id']
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.4/19",
            "description": "Unexpected criteria.source value. Expected: 'procuringEntity', actual: 'tenderer'."
        }
    ]

    assert actualresult == response.error


# Сервис ожидает ocid
@pytestrail.case("C14127")
def test_validateRequirementResponse_cpid_of_param_mismatch_to_the_pattern(host, port,
                                                                           payload_validateRequirementResponse,
                                                                           response):
    payload = payload_validateRequirementResponse(
        cpid="ocds-t1s2t3MD1587566903091"
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-5/19",
            "description": "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                           "Actual value: 'ocds-t1s2t3MD1587566903091'.",
            "details": [
                {
                    "name": "cpid"
                }
            ]
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case("C16319"),
                                          id="request without cpid attribute"),

                             pytest.param("requirementResponse",
                                          marks=pytestrail.case("C16384"),
                                          id="request without requirementResponse object")

                         ])
def test_validateRequirementResponse_without_param_in_params(port, host, response, param,
                                                             payload_validateRequirementResponse,
                                                             ):
    payload = payload_validateRequirementResponse()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."

        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case("C16385"),
                                          id="request without requirementResponse.id attribute"),

                             pytest.param("value",
                                          marks=pytestrail.case("C16386"),
                                          id="request without requirementResponse.value attribute"),

                             pytest.param("requirement",
                                          marks=pytestrail.case("C16387"),
                                          id="request without requirementResponse.requirement object"),

                         ])
def test_validateRequirementResponse_without_param_in_params_id_value_requirement(port, host, response, param,
                                                                                  payload_validateRequirementResponse,
                                                                                  ):
    payload = payload_validateRequirementResponse()
    del payload['params']['requirementResponse'][param]
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."

        }
    ]
    assert actualresult == response.error


# В работе
@pytestrail.case("C16388")
def test_validateRequirementResponse_without_param_in_params_requirement_id(host, port,
                                                                            payload_validateRequirementResponse,
                                                                            response):
    payload = payload_validateRequirementResponse()
    payload['params'] = {
            "requirementResponse": {
                "id": "string",
                "value": 22,
                "requirement": {
                    "id": str(uuid4())
                }
            }
        }

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."
        }
    ]
    assert actualresult == response.error


