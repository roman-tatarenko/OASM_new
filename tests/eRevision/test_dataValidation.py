import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize("operationType",
                         [
                             pytest.param("tenderCancellation", marks=pytestrail.case('C8111')),
                             pytest.param("lotCancellation", marks=pytestrail.case('C8112'))
                         ])
def test_on_dataValidation_with_a_valid_data(host, port, operationType, response,
                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['operationType'] = operationType
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param("amendment", marks=pytestrail.case('C8117')),
                             pytest.param("cpid", marks=pytestrail.case('C8126')),
                             pytest.param("ocid", marks=pytestrail.case('C8127')),
                             pytest.param("operationType", marks=pytestrail.case('C8128'))
                         ])
def test_on_dataValidation_without_param_in_params(host, port, param, prepared_request_id,
                                                   prepared_payload_dataValidation, response):
    payload = prepared_payload_dataValidation()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("rationale", marks=pytestrail.case('C8118')),
                             pytest.param("id", marks=pytestrail.case('C8625')),

                         ])
def test_on_dataValidation_without_required_attribute_in_amendment(host, port, param, prepared_request_id,
                                                                   prepared_payload_dataValidation, response):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("description", marks=pytestrail.case('C8119')),
                             pytest.param("documents", marks=pytestrail.case('C8120'))
                         ])
def test_on_dataValidation_without_optional_attribute_in_amendment(host, port, param,
                                                                   prepared_payload_dataValidation, response,
                                                                   prepared_cpid, prepared_ev_ocid):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param("documentType", marks=pytestrail.case('C8121')),
                             pytest.param("id", marks=pytestrail.case('C8123')),
                             pytest.param("title", marks=pytestrail.case('C8124'))
                         ])
def test_on_dataValidation_without_optional_attribute_in_amendment_documents(host, port, param, response,
                                                                             prepared_request_id,
                                                                             prepared_payload_dataValidation,
                                                                             ):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment']['documents'][0][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("description", marks=pytestrail.case('C8125'))
                         ])
def test_on_dataValidation_without_optional_params_in_amendment_documents_in_payload(host, port, param, response,

                                                                                     prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    del payload['params']['amendment']['documents'][0][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("documentType", "tenderNotice", marks=pytestrail.case('C8122'))
                         ])
def test_on_dataValidation_with_incorrect_params_amendment_documents_documentType_in_payload(host, port, param, value,
                                                                                             prepared_request_id,
                                                                                             response,
                                                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment']['documents'][0][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error["result"] = [
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

    assert actualresult == response.error


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("amendment", [{}], marks=pytestrail.case('C8140'))
                         ])
def test_on_dataValidation_with_inccorect_params_in_payload(host, port, param, value, prepared_request_id,
                                                            prepared_payload_dataValidation, response):
    payload = prepared_payload_dataValidation()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error["result"] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("rationale", "", marks=pytestrail.case('C8143')),
                             pytest.param("rationale", 3.14, marks=pytestrail.case('C8144')),
                             pytest.param("rationale", True, marks=pytestrail.case('C8145')),
                             pytest.param("description", "", marks=pytestrail.case('C8146')),
                             pytest.param("description", 3.14, marks=pytestrail.case('C8147')),
                             pytest.param("description", True, marks=pytestrail.case('C8148'))
                         ])
def test_on_dataValidation_with_inccorect_type_param_in_amendment_payload(host, port, param, value, response,
                                                                          prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("documents", {}, marks=pytestrail.case('C8149')),

                         ])
def test_on_dataValidation_with_amendment_documents_as_empty_object(host, port, param, value, prepared_request_id,
                                                                    prepared_payload_dataValidation, response):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,description",
                         [
                             pytest.param("documentType", 3.14,
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          " Expected values: 'cancellationDetails', actual value: '3.14'.",
                                          marks=pytestrail.case('C8151')),
                             pytest.param("documentType", True,
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          " Expected values: 'cancellationDetails', actual value: 'true'.",
                                          marks=pytestrail.case('C8152')),
                             pytest.param("documentType", "",
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          " Expected values: 'cancellationDetails', actual value: ''.",
                                          marks=pytestrail.case('C8153'))

                         ])
def test_on_dataValidation_with_inccorect_params_amendment_documents_documentType_in_payload(host, port, param, value,
                                                                                             description, response,
                                                                                             prepared_request_id,
                                                                                             prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment']['documents'][0][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


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
                                                                      response,
                                                                      prepared_payload_dataValidation):
    payload = prepared_payload_dataValidation()
    payload['params']['amendment']['documents'][0][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


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
                                                                           prepared_request_id, response):
    payload = prepared_payload_dataValidation()
    payload['params'][f'{param}'] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
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
