from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("operationType",
                         [
                             pytest.param("tenderCancellation", marks=pytestrail.case('C8111')),
                             pytest.param("lotCancellation", marks=pytestrail.case('C8112'))
                         ])
def test_on_dataValidation_with_a_valid_data(host, port, operationType, prepared_request_id,
                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['operationType'] = operationType
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,version",
                         [
                             pytest.param("version", "1.0.0", marks=pytestrail.case('C8113')),
                             pytest.param("id", "2.0.0", marks=pytestrail.case('C8114')),
                             pytest.param("action", "2.0.0", marks=pytestrail.case('C8115')),
                             pytest.param("params", "2.0.0", marks=pytestrail.case('C8116'))
                         ])
def test_on_dataValidation_without_attribute_in_payload(host, port, param, version, prepared_request_id,
                                                        prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    del payload[param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    if param == "id":
        prepared_request_id = '00000000-0000-0000-0000-000000000000'

    expectedresult = {
        "version": version,
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-1/21",
                "description": f"Missing required attribute '{param}'.",
                "details": [
                    {
                        "name": param
                    }
                ]
            }
        ]
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("amendment", marks=pytestrail.case('C8117')),
                             pytest.param("cpid", marks=pytestrail.case('C8126')),
                             pytest.param("ocid", marks=pytestrail.case('C8127')),
                             pytest.param("operationType", marks=pytestrail.case('C8128'))
                         ])
def test_on_dataValidation_without_params_in_payload(host, port, param, prepared_request_id,
                                                     prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("rationale", marks=pytestrail.case('C8118')),
                             pytest.param("id", marks=pytestrail.case('C8625')),

                         ])
def test_on_dataValidation_without_required_params_in_amendment_in_payload(host, port, param, prepared_request_id,
                                                                           prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("description", marks=pytestrail.case('C8119')),
                             pytest.param("documents", marks=pytestrail.case('C8120'))
                         ])
def test_on_dataValidation_without_optional_params_in_amendment_in_payload(host, port, param, prepared_request_id,
                                                                           prepared_amendment_id,
                                                                           prepared_cpid, prepared_ev_ocid):
    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "dataValidation",
        "params": {
            "amendment": {
                "rationale": "Some_string_1",
                "description": "Some_string_2",
                "documents": [
                    {
                        "documentType": "cancellationDetails",
                        "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                        "title": "string",
                        "description": "string"
                    }
                ],
                "id": f"{prepared_amendment_id}"
            },
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}",
            "operationType": "tenderCancellation"
        }
    }
    del payload['params']['amendment'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("documentType", marks=pytestrail.case('C8121')),
                             pytest.param("id", marks=pytestrail.case('C8123')),
                             pytest.param("title", marks=pytestrail.case('C8124'))
                         ])
def test_on_dataValidation_without_optional_params_in_amendment_documents_in_payload(host, port, param,
                                                                                     prepared_request_id,
                                                                                     prepared_payload_dataValidation,
                                                                                     ):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment']['documents'][0][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param",
                         [
                             pytest.param("description", marks=pytestrail.case('C8125'))
                         ])
def test_on_dataValidation_without_optional_params_in_amendment_documents_in_payload(host, port, param,
                                                                                     prepared_request_id,
                                                                                     prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    del payload['params']['amendment']['documents'][0][param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("documentType", "tenderNotice", marks=pytestrail.case('C8122'))
                         ])
def test_on_dataValidation_with_incorrect_params_amendment_documents_documentType_in_payload(host, port, param, value,
                                                                                             prepared_request_id,
                                                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['params']['amendment']['documents'][0][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-3/21",
                "description": "Attribute value mismatch of 'documentType' with one of enum expected values."
                               " Expected values: 'cancellationDetails', actual value: 'tenderNotice'.",
                "details": [
                    {
                        "name": "documentType"
                    }
                ]
            }
        ]
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("version", "99.0.0", marks=pytestrail.case('C8129'))
                         ])
def test_on_dataValidation_with_incorrect_version_in_payload(host, port, param, value,
                                                             prepared_request_id,
                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['version'] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "99.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("version", True, "DR-2/21", "Data type mismatch of attribute 'version'."
                                                                      " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8130')),
                             pytest.param("version", 3.14, "DR-2/21", "Data type mismatch of attribute 'version'."
                                                                      " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8131')),
                             pytest.param("version", "", "DR-4/21", "Data format mismatch of attribute 'version'."
                                                                    " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8132'))
                         ])
def test_on_dataValidation_with_version_type_value_in_payload(host, port, param, value, code, description,
                                                              prepared_request_id,
                                                              prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

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

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,value,code,description,id",
                         [
                             pytest.param("id", True, "DR-2/21", "Data type mismatch of attribute 'id'."
                                                                 " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          "00000000-0000-0000-0000-000000000000",
                                          marks=pytestrail.case('C8135')),
                             pytest.param("id", 3.14, "DR-2/21", "Data type mismatch of attribute 'id'."
                                                                 " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          '00000000-0000-0000-0000-000000000000',
                                          marks=pytestrail.case('C8134')),
                             pytest.param("id", "", "DR-4/21", "Data format mismatch of attribute 'id'."
                                                               " Expected data format: 'uuid', actual value: ''.",
                                          '00000000-0000-0000-0000-000000000000',
                                          marks=pytestrail.case('C8133')),
                             pytest.param("action", "checkItems", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values: 'getAmendmentIds, dataValidation, createAmendment', actual value: 'checkItems'.",
                                          uuid4(),
                                          marks=pytestrail.case('C8136')),
                             pytest.param("action", "", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values: 'getAmendmentIds, dataValidation, createAmendment', actual value: ''.",
                                          uuid4(),
                                          marks=pytestrail.case('C8137')),
                             pytest.param("action", 3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          uuid4(),
                                          marks=pytestrail.case('C8138')),
                             pytest.param("action", True, "DR-2/21",
                                          "Data type mismatch of attribute 'action'."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          uuid4(),
                                          marks=pytestrail.case('C8139'))
                         ])
def test_on_dataValidation_with_id_type_value_in_payload(host, port, param, value, code, description, id,
                                                         prepared_request_id,
                                                         prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation(id=id)

    payload[param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{id}",
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

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("amendment", [{}], marks=pytestrail.case('C8140'))
                         ])
def test_on_dataValidation_with_inccorect_params_in_payload(host, port, param, value, prepared_request_id,
                                                            prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("rationale", "", marks=pytestrail.case('C8143')),
                             pytest.param("rationale", 3.14, marks=pytestrail.case('C8144')),
                             pytest.param("rationale", True, marks=pytestrail.case('C8145')),
                             pytest.param("description", "", marks=pytestrail.case('C8146')),
                             pytest.param("description", 3.14, marks=pytestrail.case('C8147')),
                             pytest.param("description", True, marks=pytestrail.case('C8148'))
                         ])
def test_on_dataValidation_with_inccorect_type_param_in_amendment_payload(host, port, param, value, prepared_request_id,
                                                                          prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("documents", {}, marks=pytestrail.case('C8149')),

                         ])
def test_on_dataValidation_with_params_amendment_documents_in_payload(host, port, param, value, prepared_request_id,
                                                                      prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['params']['amendment'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("documents", {}, marks=pytestrail.case('C8149')),

                         ])
def test_on_dataValidation_with_params_amendment_documents_in_payload(host, port, param, value, prepared_request_id,
                                                                      prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['params']['amendment'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "RQ-1/21",
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value,description",
                         [
                             pytest.param("documentType", 3.14,
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          f" Expected values: 'cancellationDetails', actual value: '3.14'.",
                                          marks=pytestrail.case('C8151')),
                             pytest.param("documentType", True,
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          f" Expected values: 'cancellationDetails', actual value: 'true'.",
                                          marks=pytestrail.case('C8152')),
                             pytest.param("documentType", "",
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          f" Expected values: 'cancellationDetails', actual value: ''.",
                                          marks=pytestrail.case('C8153'))

                         ])
def test_on_dataValidation_with_inccorect_params_amendment_documents_documentType_in_payload(host, port, param, value,
                                                                                             description,
                                                                                             prepared_request_id,
                                                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['params']['amendment']['documents'][0][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-3/21",
                "description": description,
                "details": [
                    {
                        "name": f"{param}"
                    }
                ]
            }
        ]
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("id", 3.14, marks=pytestrail.case('C8155')),
                             pytest.param("id", True, marks=pytestrail.case('C8156')),
                             pytest.param("title", 3.14, marks=pytestrail.case('C8158')),
                             pytest.param("title", True, marks=pytestrail.case('C8159')),
                             pytest.param("title", "", marks=pytestrail.case('C8157')),
                             pytest.param("description", 3.14, marks=pytestrail.case('C8160')),
                             pytest.param("description", True, marks=pytestrail.case('C8161')),
                             pytest.param("description", "", marks=pytestrail.case('C8162')),

                         ])
def test_on_dataValidation_with_params_amendment_documents_in_payload(host, port, param, value,
                                                                      prepared_request_id,
                                                                      prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()

    payload['params']['amendment']['documents'][0][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, payload


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("cpid", 3.66, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: '3.66'.",
                                          marks=pytestrail.case('C8163')),
                             pytest.param("cpid", True, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: 'true'.",
                                          marks=pytestrail.case('C8164')),
                             pytest.param("cpid", "", "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: ''.",
                                          marks=pytestrail.case('C8165')),
                             pytest.param("ocid", 3.66, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: '3.66'.",
                                          marks=pytestrail.case('C8167')),
                             pytest.param("ocid", True, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'true'.",
                                          marks=pytestrail.case('C8168')),
                             pytest.param("ocid", "", "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8169')),

                             pytest.param("operationType", True, "DR-3/21",
                                          "Attribute value mismatch of 'operationType' with one of enum expected values."
                                          " Expected values: 'tenderCancellation, lotCancellation', actual value: 'true'.",
                                          marks=pytestrail.case('C8171')),
                             pytest.param("operationType", 3.14, "DR-3/21",
                                          "Attribute value mismatch of 'operationType' with one of enum expected values."
                                          " Expected values: 'tenderCancellation, lotCancellation', actual value: '3.14'.",
                                          marks=pytestrail.case('C8170')),
                             pytest.param("operationType", "", "DR-3/21",
                                          "Attribute value mismatch of 'operationType' with one of enum expected values."
                                          " Expected values: 'tenderCancellation, lotCancellation', actual value: ''.",
                                          marks=pytestrail.case('C8172'))

                         ])
def test_on_eRevisions_behavior_with_number_as_params_cpid_ocid_in_payload(port, host, param, value, code, description,
                                                                           prepared_payload_dataValidation,
                                                                           prepared_request_id):
    payload = prepared_payload_dataValidation()
    payload['params'][f'{param}'] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
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

    assert expectedresult == actualresult, actualresult
