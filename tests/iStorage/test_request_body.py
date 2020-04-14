import random

import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = ("checkRegistration", "openAccess")


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8629'), id="version as number."),
                             # pytest.param("version", True, "DR-2/14",
                             #              "Data type mismatch."
                             #              " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                             #              marks=pytestrail.case(), id="version as boolean."),
                             pytest.param("version", "", "DR-4/14",
                                          "Data format mismatch."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8628'), id="version as empty str."),
                             pytest.param("version", None, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8627'), id="version as null."),
                             # pytest.param("version", "99.0.a", "DR-4/14",
                             #              "Data format mismatch of attribute 'version'."
                             #              " Expected data format: '00.00.00', actual value: '99.0.a'.",
                             #              marks=pytestrail.case(), id="version as '99.0.a'."),
                             # pytest.param("id", 3.14, "DR-2/14",
                             #              "Data type mismatch of attribute 'id'."
                             #              " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                             #              marks=pytestrail.case(), id="id as number."),
                             pytest.param("id", True, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8634'), id="id as boolean."),
                             pytest.param("id", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8631'), id="id as number."),
                             pytest.param("id", "", "DR-4/14",
                                          "Data format mismatch."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8632'), id="id as empty str."),
                             pytest.param("id", None, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8633'), id="id as null."),
                             pytest.param("action", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8637'), id="action as number."),
                             pytest.param("action", True, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8635'), id="action as boolean."),
                             pytest.param("action", "", "DR-3/14",
                                          "Attribute value mismatch with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}', actual value: ''.",
                                          marks=pytestrail.case('C8638'), id="action as empty str."),
                             # pytest.param("action", "checkItems", "DR-3/14",
                             #              "Attribute value mismatch with one of enum expected values."
                             #              f" Expected values: '{', '.join(action_enum)}', actual value: 'checkItems'.",
                             #              marks=pytestrail.case(), id="action != val enum."),
                             pytest.param("action", None, "DR-2/14",
                                          "Data type mismatch. Expected data type: 'not null',"
                                          " actual data type: 'null'.",
                                          marks=pytestrail.case('C8639'), id="action as null."),

                         ])
def test_on_iStorage_with_invalid_param(port, host, param, value, code, description, request_template, response):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [{"code": code,
                                 "description": description,
                                 "details": [{"name": param}]}]
    # if request contain invalid param id then service set id(uuid) as 'null' in response
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    # if request contain invalid param version then service set version as '1.0.0' in response
    if param == 'version':
        response.error['version'] = '1.0.0'

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("version", marks=pytestrail.case('C8626')),
                             # pytest.param("id", marks=pytestrail.case()),
                             pytest.param("action", marks=pytestrail.case('C8636')),
                             pytest.param("params", marks=pytestrail.case('C8107', 'C8192'))
                         ])
def test_on_iStorage_without_param(port, host, param, request_template, response):
    payload = request_template()
    if param == 'params':
        payload['action'] = random.choice(action_enum)
    del payload[param]
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [{"code": "DR-1/14",
                                 "description": "Missing required attribute.",
                                 "details": [{"name": param}]}]
    # if request contain invalid param id then service set id(uuid) as 'null' in response
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    # if request contain invalid param version then service set version as '1.0.0' in response
    if param == "version":
        response.error['version'] = '1.0.0'

    assert actualresult == response.error


@pytest.mark.parametrize("params,code,description",
                         [
                             # pytest.param([{}], "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case()),
                             pytest.param({}, "RQ-01/14", "Can not parse 'params'.", marks=pytestrail.case('C8193'))
                         ])
def test_the_iStorage_behavior_with_params_as_array_of_objects_in_payload(host, port, code, description, params,
                                                                          request_template, response
                                                                          ):
    payload = request_template()
    payload['action'] = random.choice(action_enum)
    payload['params'] = params
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [{"code": code,
                                 "description": description}]

    assert actualresult == response.error, actualresult

# @pytest.mark.parametrize("param,value",
#                          [
#                              pytest.param("version", "99.0.0", marks=pytestrail.case())
#                          ])
# def test_on_dataValidation_with_incorrect_version_in_payload(host, port, param, value,
#                                                              response_success,
#                                                              prepared_payload_dataValidation):
#     payload = prepared_payload_dataValidation()
#     payload[param] = value
#     actual_result = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
#     expected_result = response_success
#     expected_result[param] = value
#
#     assert actual_result == expected_result, actual_result
