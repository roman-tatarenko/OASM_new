import random

import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = ("findAmendmentIds", "dataValidation", "createAmendment", "CheckAccessToAmendment",
               "getMainPartOfAmendmentByIds", "setStateForAmendment")


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8235', 'C8131', 'C8379'), id="version as number."),
                             pytest.param("version", True, "DR-2/21",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8236', 'C8130', 'C8380'), id="version as boolean."),
                             pytest.param("version", "", "DR-4/21",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8234', 'C8132', 'C8382'), id="version as empty str."),
                             pytest.param("version", None, "DR-2/21",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8381'), id="version as null."),
                             pytest.param("version", "99.0.a", "DR-4/21",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: '99.0.a'.",
                                          marks=pytestrail.case('C8232'), id="version as '99.0.a'."),
                             pytest.param("id", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8238', 'C8134', 'C8386'), id="id as number."),
                             pytest.param("id", True, "DR-2/21",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8240', 'C8135', 'C8387'), id="id as boolean."),
                             pytest.param("id", "", "DR-4/21",
                                          "Data format mismatch of attribute 'id'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8243', 'C8133', 'C8389'), id="id as empty str."),
                             pytest.param("id", None, "DR-2/21",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8388'), id="id as null."),
                             pytest.param("action", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8245', 'C8138', 'C8393'), id="action as number."),
                             pytest.param("action", True, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8252', 'C8139', 'C8396'), id="action as boolean."),
                             pytest.param("action", "", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}', actual value: ''.",
                                          marks=pytestrail.case('C8247', 'C8137', 'C8395'), id="action as empty str."),
                             pytest.param("action", "checkItems", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}', actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8249', 'C8392', 'C8136'), id="action != val enum."),
                             pytest.param("action", None, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'not null',"
                                          " actual data type: 'null'.",
                                          marks=pytestrail.case('C8394'), id="action as null."),

                         ])
def test_on_eRevision_with_invalid_param(port, host, param, value, code, description, request_template, response):
    payload = request_template
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
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
                             pytest.param("version", marks=pytestrail.case('C8202', 'C8113', 'C8067')),
                             pytest.param("id", marks=pytestrail.case('C8203', 'C8384', 'C8114')),
                             pytest.param("action", marks=pytestrail.case('C8204', 'C8115', 'C8390')),
                             pytest.param("params", marks=pytestrail.case('C8205', 'C8116', 'C8397'))
                         ])
def test_on_eRevision_without_param(port, host, param, request_template, response):
    payload = request_template
    if param == 'params':
        payload['action'] = random.choice(action_enum)
    del payload[param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [{"code": "DR-1/21",
                                 "description": f"Missing required attribute '{param}'.",
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
                             pytest.param([{}], "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('C8398')),
                             pytest.param({}, "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('C8399'))
                         ])
def test_the_eRevisions_behavior_with_params_as_array_of_objects_in_payload(host, port, code, description, params,
                                                                            request_template, response
                                                                            ):
    payload = request_template
    payload['action'] = random.choice(action_enum)
    payload['params'] = params
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [{"code": code,
                                 "description": description}]

    assert actualresult == response.error, actualresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("version", "99.0.0", marks=pytestrail.case('C8129'))
                         ])
def test_on_dataValidation_with_incorrect_version_in_payload(host, port, param, value,
                                                             response_success,
                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload[param] = value
    actual_result = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expected_result = response_success
    expected_result[param] = value

    assert actual_result == expected_result, actual_result
