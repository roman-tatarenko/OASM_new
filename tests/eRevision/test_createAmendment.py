import uuid

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("param,value,operationType",
                         [
                             pytest.param("status", "pending", "tenderCancellation", marks=pytestrail.case('C8201')),
                             pytest.param("type", "cancellation", "tenderCancellation", marks=pytestrail.case('C8339')),
                             pytest.param("relatesTo", "tender", "tenderCancellation", marks=pytestrail.case('C8340')),
                             pytest.param("relatesTo", "lot", "lotCancellation", marks=pytestrail.case('C8341'))

                         ])
def test_on_eRevision_is_assign_pending_value_for_result_status(port, host, param, value, operationType,
                                                                prepared_entity_id,
                                                                prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    payload['params']['operationType'] = operationType
    payload['params']['relatedEntityId'] = f"{prepared_entity_id}"

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = value

    assert actualresult['result'][param] == expectedresult, actualresult


@pytest.mark.parametrize("operationType",
                         [
                             pytest.param("tenderCancellation", marks=pytestrail.case('C8341')),
                             pytest.param("lotCancellation", marks=pytestrail.case('C8614'))

                         ])
def test_the_eRevision_correctly_sets_value_for_result_relatedItem(port, host, operationType,
                                                                   prepared_entity_id,
                                                                   prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    payload['params']['operationType'] = operationType
    payload['params']['relatedEntityId'] = f"{prepared_entity_id}"

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = f"{prepared_entity_id}"

    assert actualresult['result']['relatedItem'] == expectedresult, actualresult


@pytestrail.case('C8344')
def test_the_eRevision_sets_result_token(port, host,
                                         prepared_entity_id,
                                         prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert uuid.UUID(actualresult['result']['token']), actualresult


@pytestrail.case('C8343')
def test_the_eRevision_correctly_sets_value_for_result_date(port, host,
                                                            prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult['result']['date'] == payload['params']['startDate'], actualresult


@pytest.mark.parametrize("param,code,description",
                         [
                             pytest.param("version", "DR-1/21",
                                          "Missing required attribute 'version'.",
                                          marks=pytestrail.case('C8202')),
                             pytest.param("id", "DR-1/21",
                                          "Missing required attribute 'id'.",
                                          marks=pytestrail.case('C8203')),
                             pytest.param("action", "DR-1/21",
                                          "Missing required attribute 'action'.",
                                          marks=pytestrail.case('C8204')),
                             pytest.param("params", "DR-1/21",
                                          "Missing required attribute 'params'.",
                                          marks=pytestrail.case('C8205'))

                         ])
def test_on_impossibility_to_create_amendment_without_params_in_payload(port, host, param, code, description,
                                                                        prepared_request_id,
                                                                        prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    del payload[param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
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
    }

    if param == "id":
        expectedresult['id'] = "00000000-0000-0000-0000-000000000000"

    if param in {"action", "params", "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", "99.0.a", "DR-4/21",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: '99.0.a'.",
                                          marks=pytestrail.case('C8232')),
                             pytest.param("version", "", "DR-4/21",
                                          "Data format mismatch of attribute 'version'."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8234')),
                             pytest.param("version", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8235')),
                             pytest.param("version", True, "DR-2/21",
                                          "Data type mismatch of attribute 'version'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8236')),
                             pytest.param("id", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8238')),
                             pytest.param("id", True, "DR-2/21",
                                          "Data type mismatch of attribute 'id'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8240')),
                             pytest.param("id", "", "DR-4/21",
                                          "Data format mismatch of attribute 'id'."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8243')),
                             pytest.param("action", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8245')),
                             pytest.param("action", "", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values:"
                                          " 'getAmendmentIds, dataValidation, createAmendment', actual value: ''.",
                                          marks=pytestrail.case('C8247')),
                             pytest.param("action", "checkItems", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values: 'getAmendmentIds, dataValidation, createAmendment',"
                                          " actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8249')),
                             pytest.param("action", True, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8252')),

                         ])
def test_on_impossibility_to_create_amendment_with_invalid_version_in_payload(port, host, param, value, code,
                                                                              description, prepared_request_id,
                                                                              prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment
    payload[param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
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
    }

    if param == "id":
        expectedresult['id'] = "00000000-0000-0000-0000-000000000000"

    if param in {'action', "id"}:
        expectedresult['version'] = '2.0.0'

    assert actualresult == expectedresult
