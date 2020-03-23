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
                             pytest.param("id", marks=pytestrail.case('C8625'))
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
