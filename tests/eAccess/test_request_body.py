import random

import pytest
import requests
from pytest_testrail.plugin import pytestrail

action_enum = ('findLotIds', 'checkAccessToTender', 'getLotStateByIds', 'responderProcessing', 'checkPersonesStructure',
               'getTenderState', 'setStateForLots', 'setStateForTender')


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8642')),
                             pytest.param("version", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8645')),
                             pytest.param("version", "", "DR-4/3",
                                          "Data format mismatch."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8466')),
                             pytest.param("id", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8643')),
                             pytest.param("id", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8646')),
                             pytest.param("id", "", "DR-4/3",
                                          "Data format mismatch."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8467')),
                             pytest.param("action", 3.14, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8644')),
                             pytest.param("action", True, "DR-2/3",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8647')),
                             pytest.param("action", "", "DR-3/3",
                                          "Attribute value mismatch with one of enum expected values."
                                          f" Expected values: '{', '.join(action_enum)}', actual value: ''.",
                                          marks=pytestrail.case('C8468'))
                         ])
def test_eAccess_returns_response_with_status_error_if_request_contains(port, host, param,
                                                                        value, code, request_template,
                                                                        description, response
                                                                        ):
    payload = request_template()
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [{"name": param}]
        }
    ]
    if param == "id":
        response.error['id'] = "00000000-0000-0000-0000-000000000000"

    if param == 'version':
        response.error['version'] = '1.0.0'

    assert actualresult == response.error


@pytestrail.case('C8087')
def test_findLotIds_request_does_not_contain_params_object(port, host, response, request_template):
    payload = request_template()
    payload['action'] = random.choice(action_enum)
    del payload['params']
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": 'DR-1/3',
            "description": "Missing required attribute.",
            "details": [{"name": "params"}]
        }
    ]

    assert actualresult == response.error
