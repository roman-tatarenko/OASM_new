import random

import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = ('getAwardStateByIds', 'checkAccessToAward', 'checkRelatedTenderer', 'createRequirementResponse',
               'createUnsuccessfulAwards', 'closeAwardPeriod')


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", 3.14, "DR-2/7",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C12500'), id="version as number."),
                             pytest.param("version", True, "DR-2/7",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C12502"), id="version as boolean."),
                             pytest.param("version", "", "DR-4/7",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case("C12503"), id="version as empty str."),
                             # pytest.param("version", None, "DR-2/21",
                             #              "Data type mismatch of attribute 'version'."
                             #              " Expected data type: 'not null', actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="version as null."),
                             # pytest.param("version", "99.0.a", "DR-4/21",
                             #              "Data format mismatch of attribute 'version'."
                             #              " Expected data format: '00.00.00', actual value: '99.0.a'.",
                             #              marks=pytestrail.case(), id="version as '99.0.a'."),
                             pytest.param("id", 3.14, "DR-2/7",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C12505"), id="id as number."),
                             pytest.param("id", True, "DR-2/7",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C12507"), id="id as boolean."),
                             pytest.param("id", "", "DR-4/7",
                                          "Data format mismatch of attribute 'id'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C12508"), id="id as empty str."),
                             # pytest.param("id", None, "DR-2/21",
                             #              "Data type mismatch of attribute 'id'."
                             #              " Expected data type: 'not null', actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="id as null."),
                             pytest.param("action", 3.14, "DR-2/7",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case("C12513"), id="action as number."),
                             pytest.param("action", True, "DR-2/7",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case("C12512"), id="action as boolean."),
                             pytest.param("action", "", "DR-3/7",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}', actual value: ''.",
                                          marks=pytestrail.case("C12509"), id="action as empty str."),
                             pytest.param("action", "getAmendmentIds", "DR-3/7",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}',"
                                          f" actual value: 'getAmendmentIds'.",
                                          marks=pytestrail.case("C12511"), id="action != val enum."),
                             # pytest.param("action", None, "DR-2/21",
                             #              "Data type mismatch of attribute 'action'. Expected data type: 'not null',"
                             #              " actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="action as null."),

                         ])
def test_on_eEvaluation_with_invalid_param(port, host, param, value, code, description, request_template, response):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
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
                             pytest.param("version", marks=pytestrail.case("C12501")),
                             pytest.param("id", marks=pytestrail.case("C12506")),
                             pytest.param("action", marks=pytestrail.case("C12510")),
                             pytest.param("params", marks=pytestrail.case("C13194"))
                         ])
def test_on_eEvaluation_without_param(port, host, param, request_template, response):
    payload = request_template()
    if param == 'params':
        payload['action'] = random.choice(action_enum)
    del payload[param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [{"code": "DR-1/7",
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
                             # pytest.param([{}], "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('')),
                             pytest.param({}, "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('C13242'))
                         ])
def test_the_eEvaluation_behavior_with_params_as_array_of_objects_in_payload(host, port, code, description, params,
                                                                             request_template, response
                                                                             ):
    payload = request_template()
    payload['action'] = random.choice(action_enum)
    payload['params'] = params
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [{"code": code,
                                 "description": description}]

    assert actualresult == response.error
