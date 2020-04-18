import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = "updateRecord"


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", 3.14, "DR-2/2",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8241'), id="version as number."),
                             pytest.param("version", True, "DR-2/2",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8239'), id="version as boolean."),
                             pytest.param("version", "", "DR-4/2",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8242'), id="version as empty str."),
                             # pytest.param("version", None, "DR-2/2",
                             #              "Data type mismatch of attribute 'version'."
                             #              " Expected data type: 'not null', actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="version as null."),
                             # pytest.param("version", "99.0.a", "DR-4/2",
                             #              "Data format mismatch of attribute 'version'."
                             #              " Expected data format: '00.00.00', actual value: '99.0.a'.",
                             #              marks=pytestrail.case(), id="version as '99.0.a'."),
                             pytest.param("id", 3.14, "DR-2/2",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8246'), id="id as number."),
                             pytest.param("id", True, "DR-2/2",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8248'), id="id as boolean."),
                             pytest.param("id", "", "DR-4/2",
                                          "Data format mismatch of attribute 'id'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8244'), id="id as empty str."),
                             # pytest.param("id", None, "DR-2/2",
                             #              "Data type mismatch of attribute 'id'."
                             #              " Expected data type: 'not null', actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="id as null."),
                             pytest.param("action", 3.14, "DR-2/2",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8253'), id="action as number."),
                             pytest.param("action", True, "DR-2/2",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8254'), id="action as boolean."),
                             pytest.param("action", "", "DR-3/2",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{action_enum}', actual value: ''.",
                                          marks=pytestrail.case('C8251'), id="action as empty str."),
                             pytest.param("action", "checkItems", "DR-3/2",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          f" Expected values: '{action_enum}', actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8250'), id="action != val enum."),
                             # pytest.param("action", None, "DR-2/2",
                             #              "Data type mismatch of attribute 'action'. Expected data type: 'not null',"
                             #              " actual data type: 'null'.",
                             #              marks=pytestrail.case(), id="action as null."),

                         ])
def test_on_eNotice_with_invalid_param(port, host, param, value, code, description, request_template, response):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
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
                             pytest.param("version", marks=pytestrail.case('C8230')),
                             pytest.param("id", marks=pytestrail.case('C8231')),
                             pytest.param("action", marks=pytestrail.case('C8233')),
                             pytest.param("params", marks=pytestrail.case('C8259'))
                         ])
def test_on_eNotice_without_param(port, host, param, request_template, response):
    payload = request_template()
    if param == 'params':
        payload['action'] = action_enum
    del payload[param]
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    response.error['result'] = [{"code": "DR-1/2",
                                 "description": f"Missing required attribute '{param}'.",
                                 "details": [{"name": param}]}]
    # if request contain invalid param id then service set id(uuid) as 'null' in response
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"
    # if request contain invalid param version then service set version as '1.0.0' in response
    if param == "version":
        response.error['version'] = '1.0.0'

    assert actualresult == response.error
