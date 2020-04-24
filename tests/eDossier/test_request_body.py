import random

import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = ('validateRequirementResponse',)


@pytest.mark.parametrize("param, value, description",
                         [
                             pytest.param("version", "",
                                          "Data format mismatch. Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case("C14103"),
                                          id="version as empty string"),

                             pytest.param("id", "",
                                          "Data format mismatch. Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C14104"),
                                          id="id as empty string")

                         ])
def test_validateRequirementResponse_data_format_mismatch(port, host, response, param,
                                                          request_template, value, description):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-4/19",
            "description": description,
            "details": [{"name": param}]
        }
    ]
    if param == "version":
        response.error['version'] = '1.0.0'
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    assert actualresult == response.error


@pytestrail.case("C14105")
def test_validateRequirementResponse_mismatch_with_one_of_enum_expected_values(port, host, response,
                                                                               request_template):
    payload = request_template(action="")
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-3/19",
            "description": "Attribute value mismatch with one of enum expected values."
                           f" Expected values: '{', '.join(action_enum)}', actual value: ''.",
            "details": [
                {
                    "name": "action"
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, description",
                         [
                             pytest.param("version", 22.9,
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14106"),
                                          id="version as number"),

                             pytest.param("id", 22.9,
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14107"),
                                          id="id as number"),

                             pytest.param("action", 22.9,
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C14108"),
                                          id="action as number"),

                             pytest.param("version", False,
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14109"),
                                          id="version as boolean"),

                             pytest.param("id", False,
                                          "Data type mismatch. Expected data type: 'STRING', "
                                          "actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14110"),
                                          id="id as boolean"),

                             pytest.param("action", False,
                                          "Data type mismatch. Expected data type: "
                                          "'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C14111"),
                                          id="action as boolean")

                         ])
def test_validateRequirementResponse_data_type_mismatch_of_the_attribute(port, host, response, param, value,
                                                                         request_template, description):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-2/19",
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
                                          id="request without action attribute"),

                             pytest.param("params",
                                          marks=pytestrail.case("C14113"),
                                          id="without params object")

                         ])
def test_validateRequirementResponse_missing_required_attribute(port, host, response, param, request_template):
    payload = request_template(action=random.choice(action_enum))
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


@pytestrail.case("C14116")
def test_validateRequirementResponse_with_empty_params_object(port, host, response, request_template):
    payload = request_template(
        action=random.choice(action_enum),
        params={}
    )

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
                                                                              request_template):
    payload = request_template(action="Invalid")

    actualresult = requests.post(f'{host}:{port.eDossier}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-3/19",
            "description": "Attribute value mismatch with one of enum expected values."
                           f" Expected values: '{', '.join(action_enum)}', actual value: 'Invalid'.",
            "details": [
                {
                    "name": "action"
                }
            ]
        }
    ]

    assert actualresult == response.error
