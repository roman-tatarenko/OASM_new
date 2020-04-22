import pytest
from pytest_testrail.plugin import pytestrail
import requests


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
                                                             value, prepared_entity_id):
    cpid = prepared_cpid
    data = data_create_criteria
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['dataType'] = param
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id'] = str(prepared_entity_id)
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=prepared_owner
    )

    requirement_id = data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id']
    payload = payload_validateRequirementResponse(
        value=value,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param, value, code, description, Id",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-8888888888888",
                                          "VR-10.5.1.3/19",
                                          "Requirement with cpid 'ocds-t1s2t3-MD-8888888888888' not found.",
                                          "ocds-t1s2t3-MD-8888888888888",
                                          marks=pytestrail.case("C16318"),
                                          id="cpid does not present in DB"),

                             pytest.param("id", "e3a9cb88-8888-9fdc-9cea-9dc1d99df99e", "VR-10.5.1.1/19",
                                          "Requirement with id 'e3a9cb88-8888-9fdc-9cea-9dc1d99df99e' not found.",
                                          "e3a9cb88-8888-9fdc-9cea-9dc1d99df99e",
                                          marks=pytestrail.case("C14122"),
                                          id="requirement does not present in DB"),

                             pytest.param("id", "e3a9cb88-8888-9fdc-9cea-9dc1d99df99e", "VR-10.5.1.1/19",
                                          "Requirement with id 'e3a9cb88-8888-9fdc-9cea-9dc1d99df99e' not found.",
                                          "e3a9cb88-8888-9fdc-9cea-9dc1d99df99e",
                                          marks=pytestrail.case("C14124"),
                                          id="award criteria:price only")

                         ])
def test_validateRequirementResponse_requirement_does_not_present_in_DB(host, port,
                                                                        execute_insert_into_dossier_tenders,
                                                                        prepared_cpid, data_create_criteria,
                                                                        prepared_owner,
                                                                        payload_validateRequirementResponse, response,
                                                                        param, value, code, description, Id,
                                                                        prepared_entity_id):
    cpid = prepared_cpid
    data = data_create_criteria
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_validateRequirementResponse()
    payload['params'][param] = value
    payload['params']['requirementResponse']['requirement'][param] = value

    cpid = prepared_cpid
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data={"awardCriteria": "priceOnly", "awardCriteriaDetails": "automated"},
        owner=prepared_owner
    )

    payload['params']['requirementResponse']['requirement'][param] = value

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()

    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "id": Id
                }
            ]
        }
    ]
    assert actualresult == response.error


@pytestrail.case("C14123")
def test_validateRequirementResponse_dataType_mismatch_for_requirement(host, port, execute_insert_into_dossier_tenders,
                                                                       prepared_cpid, data_create_criteria,
                                                                       prepared_owner,
                                                                       payload_validateRequirementResponse, response,
                                                                       prepared_entity_id):
    owner = prepared_owner
    cpid = prepared_cpid
    data = data_create_criteria
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['dataType'] = 'boolean'
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id'] = str(prepared_entity_id)
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=owner
    )

    requirement_id = data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id']
    payload = payload_validateRequirementResponse(
        cpid=cpid,
        value=22.9,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.2/19",
            "description": "Requirement.dataType mismatch. AsNumber(value=22.9) "
                           "!= com.procurement.dossier.application.model.data.NoneValue@4ae3c593"
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C14125")
def test_validateRequirementResponse_unexpected_criteria_source(host, port, execute_insert_into_dossier_tenders,
                                                                prepared_cpid, prepared_owner,
                                                                data_create_two_criteria_and_conversion,
                                                                payload_validateRequirementResponse, response,
                                                                prepared_entity_id):
    owner = prepared_owner
    cpid = prepared_cpid
    data = data_create_two_criteria_and_conversion
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['dataType'] = 'integer'
    data['criteria'][0]['source'] = "tenderer"
    data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id'] = str(prepared_entity_id)
    data['criteria'][1]['requirementGroups'][0]['requirements'][0]['dataType'] = 'boolean'
    data['criteria'][1]['source'] = "procuringEntity"
    data['criteria'][1]['requirementGroups'][0]['requirements'][0]['id'] = str(prepared_entity_id)
    execute_insert_into_dossier_tenders(
        cp_id=cpid,
        json_data=data,
        owner=owner
    )

    requirement_id = data['criteria'][0]['requirementGroups'][0]['requirements'][0]['id']
    payload = payload_validateRequirementResponse(
        cpid=cpid,
        value=22,
        requirement_id=requirement_id
    )

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.5.1.4/19",
            "description": "Unexpected criteria.source value. Expected: 'procuringEntity', actual: 'tenderer'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("cpid", "ocds-t1s2t3MD1587566903091", "DR-5/19",
                                          "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: 'ocds-t1s2t3MD1587566903091'.",
                                          marks=pytestrail.case("C14127"),
                                          id="cpid of param mismatch to the pattern"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-1580003704318EV1586476007102", "DR-5/19",
                                          "Data mismatch to pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: 'ocds-t1s2t3-MD-1580003704318EV1586476007102'.",
                                          marks=pytestrail.case("C14128"),
                                          id="ocid of param mismatch to the pattern")
                         ])
def test_validateRequirementResponse_cpid_ocid_of_param_mismatch_to_the_pattern(host, port, param, value, code,
                                                                                payload_validateRequirementResponse,
                                                                                prepared_cpid, description, response):
    payload = payload_validateRequirementResponse()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()

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


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case("C16319"),
                                          id="request without cpid attribute"),

                             pytest.param("ocid",
                                          marks=pytestrail.case("C16320"),
                                          id="request without ocid attribute"),

                             pytest.param("requirementResponse",
                                          marks=pytestrail.case("C16384"),
                                          id="request without requirementResponse object"),

                         ])
def test_validateRequirementResponse_without_param_in_params_cpid_ocid_reqResponse(port, host, response, param,
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


@pytest.mark.parametrize("param",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case("C16388"),
                                          id="request without requirementResponse.id attribute")

                         ])
def test_validateRequirementResponse_without_param_in_params_requirement_id(port, host, response, param,
                                                                            payload_validateRequirementResponse
                                                                            ):
    payload = payload_validateRequirementResponse()
    del payload['params']['requirementResponse']['requirement'][param]
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("version", "", "DR-4/19",
                                          "Data format mismatch. Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case("C14103"),
                                          id="version as empty string"),

                             pytest.param("id", "", "DR-4/19",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C14104"),
                                          id="id as empty string")

                         ])
def test_validateRequirementResponse_data_format_mismatch(port, host, response, param,
                                                          request_template, value, code, description):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]
    if param == "version":
        response.error['version'] = '1.0.0'
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("action", "", "DR-3/19",
                                          "Attribute value mismatch with one of enum expected values. "
                                          "Expected values: 'validateRequirementResponse', actual value: ''.",
                                          marks=pytestrail.case("C14105"),
                                          id="action as empty string")

                         ])
def test_validateRequirementResponse_mismatch_with_one_of_enum_expected_values(port, host, response, param,
                                                                               request_template, value, code,
                                                                               description):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("version", 22.9, "DR-2/19",
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14106"),
                                          id="version as number"),

                             pytest.param("id", 22.9, "DR-2/19",
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14107"),
                                          id="id as number"),

                             pytest.param("action", 22.9, "DR-2/19",
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14108"),
                                          id="action as number"),

                             pytest.param("version", False, "DR-2/19",
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14109"),
                                          id="version as boolean"),

                             pytest.param("id", False, "DR-2/19",
                                          "Data type mismatch. Expected data type: 'STRING', "
                                          "actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14110"),
                                          id="id as boolean"),

                             pytest.param("action", False, "DR-2/19",
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14111"),
                                          id="action as boolean")

                         ])
def test_validateRequirementResponse_data_type_mismatch_of_the_attribute(port, host, response, param, value, code,
                                                                         request_template, description):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]
    if param == "version":
        response.error['version'] = '1.0.0'
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("version",
                                          marks=pytestrail.case("C14112"),
                                          id="request without version attribute"),

                             pytest.param("id",
                                          marks=pytestrail.case("C14114"),
                                          id="request without id attribute"),

                             pytest.param("action",
                                          marks=pytestrail.case("C14115"),
                                          id="request without action attribute")

                         ])
def test_validateRequirementResponse_missing_required_attribute(port, host, response, param, request_template):
    payload = request_template()
    del payload[param]
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-1/19",
            "description": "Missing required attribute.",
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    if param == "version":
        response.error['version'] = '1.0.0'
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    assert actualresult == response.error


@pytestrail.case("C14113")
def test_validateRequirementResponse_missing_required_attribute_request_without_params_object(port, host, response,
                                                                                              payload_validateRequirementResponse):
    payload = payload_validateRequirementResponse()
    del payload['params']
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-1/19",
            "description": "Missing required attribute.",
            "details": [
                {
                    "name": "params"
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C14116")
def test_validateRequirementResponse_with_empty_params_object(port, host, response,
                                                              payload_validateRequirementResponse):
    payload = payload_validateRequirementResponse()
    payload['params'] = {}
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C14117")
def test_validateRequirementResponse_mismatch_of_enum_values_incorrect_action(port, host, response,
                                                                              payload_validateRequirementResponse):
    payload = payload_validateRequirementResponse()
    payload['params'] = {}
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/19",
            "description": "Can not parse 'params'.."
        }
    ]

    assert actualresult == response.error
