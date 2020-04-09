import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8097')
def test_iStorage_returns_successful_response_if_there_is_registered_and_uploaded_document_in_request(host, port,
                                                                                                      response_success,
                                                                                                      registering_document,
                                                                                                      upload_document,
                                                                                                      payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"

    registration_data = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id = registration_data['data']['id']

    upload_document(dir_path=dir_path, file_name=file_name, doc_id=doc_id)

    payload = payload_check_registration(ids=[doc_id])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response_success


@pytestrail.case('C8195')
def test_iStorage_returns_successful_response_if_there_is_registered_and_not_uploaded_document_in_request(host, port,
                                                                                                          response_success,
                                                                                                          registering_document,
                                                                                                          upload_document,
                                                                                                          payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"

    registration_data = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id = registration_data['data']['id']

    payload = payload_check_registration(ids=[doc_id])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response_success


@pytestrail.case('C8100')
def test_iStorage_returns_successful_response_if_there_is_more_than_one_registered_document_in_request(host, port,
                                                                                                       response_success,
                                                                                                       registering_document,
                                                                                                       upload_document,
                                                                                                       payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"

    registration_data_1 = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id_1 = registration_data_1['data']['id']

    registration_data_2 = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id_2 = registration_data_2['data']['id']

    payload = payload_check_registration(ids=[doc_id_1, doc_id_2])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response_success


@pytestrail.case('C8103')
def test_iStorage_behavior_when_there_are_two_documents_with_the_same_id_in_request(host, port,
                                                                                    response_success,
                                                                                    registering_document,
                                                                                    upload_document,
                                                                                    payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"

    registration_data = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id = registration_data['data']['id']

    payload = payload_check_registration(ids=[doc_id, doc_id])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response_success


@pytestrail.case('C8098')
def test_iStorage_returns_response_with_status_error_if_at_least_one_document_from_request_is_not_registered(host, port,
                                                                                                             response_error,
                                                                                                             registering_document,
                                                                                                             upload_document,
                                                                                                             prepared_entity_id,
                                                                                                             payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"

    registration_data = registering_document(dir_path=dir_path, file_name=file_name)

    doc_id_1 = registration_data['data']['id']
    doc_id_2 = str(prepared_entity_id())

    payload = payload_check_registration(ids=[doc_id_1, doc_id_2])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id_2}]' does not exist"
        }
    ]

    assert actualresult == response_error


@pytestrail.case('C8105')
def test_iStorage_returns_response_with_status_error_if_the_request_contains_documentIds_value_that_does_not_match_the_pattern(
        host, port,
        response_error,
        prepared_entity_id,
        payload_check_registration):
    doc_id = str(prepared_entity_id())

    payload = payload_check_registration(ids=[doc_id])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id}]' does not exist"
        }
    ]

    assert actualresult == response_error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("id", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8631')),
                             pytest.param("id", True, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8634')),
                             pytest.param("id", "", "DR-4/14",
                                          "Data format mismatch."
                                          " Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case('C8632')),
                             pytest.param("id", None, "DR-2/14",
                                          "Data type mismatch. Expected data type:"
                                          " 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8633')),
                             pytest.param("action", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8637')),
                             pytest.param("action", True, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8635')),
                             pytest.param("action", "", "DR-3/14",
                                          "Attribute value mismatch with one of enum expected values."
                                          " Expected values: 'checkRegistration, openAccess', actual value: ''.",
                                          marks=pytestrail.case('C8638')),
                             pytest.param("action", None, "DR-2/14",
                                          "Data type mismatch. Expected data type:"
                                          " 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8639')),
                             pytest.param("version", 3.14, "DR-2/14",
                                          "Data type mismatch."
                                          " Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8629')),
                             pytest.param("version", None, "DR-2/14",
                                          "Data type mismatch. Expected data type:"
                                          " 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8627')),
                             pytest.param("version", "", "DR-4/14",
                                          "Data format mismatch."
                                          " Expected data format: '00.00.00', actual value: ''.",
                                          marks=pytestrail.case('C8628'))
                         ])
def test_on_iStorage_behavior_with(port, host, param, value, code, description,
                                   response_error, prepared_entity_id,
                                   payload_check_registration):
    payload = payload_check_registration(ids=[str(prepared_entity_id)])

    payload[param] = value

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
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

    if param == "id":
        response_error['id'] = "00000000-0000-0000-0000-000000000000"
    if param in {'action', "id"}:
        response_error['version'] = '2.0.0'

        assert actualresult == response_error, print(actualresult)


@pytest.mark.parametrize("param",
                         [
                             pytest.param("action", marks=pytestrail.case('C8636')),
                             pytest.param("version", marks=pytestrail.case('C8626')),
                             pytest.param("params", marks=pytestrail.case('C8107'))

                         ])
def test_on_there_is_response_with_status_error_if_request_does_not_contain(port, host, param,
                                                                            payload_check_registration,
                                                                            response_error, prepared_entity_id
                                                                            ):
    payload = payload_check_registration(ids=[str(prepared_entity_id)])

    del payload[param]

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "DR-1/14",
            "description": "Missing required attribute.",
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]
    if param in {"version"}:
        response_error['version'] = '1.0.0'

    assert actualresult == response_error


@pytestrail.case('C8109')
def test_iStorage_returns_response_with_status_error_if_request_contains_empty_documentIds_array(port, host,
                                                                                                 payload_check_registration,
                                                                                                 response_error
                                                                                                 ):
    payload = payload_check_registration(ids=[])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "DR-10/14",
            "description": "Array is empty.",
            "details": [
                {
                    "name": "documentIds"
                }
            ]
        }
    ]

    assert actualresult == response_error


@pytestrail.case('C8108')
def test_iStorage_returns_response_with_status_error_if_request_contains_empty_params_object(host, port,
                                                                                             response_error,
                                                                                             payload_check_registration):
    payload = payload_check_registration(ids=["1"])

    del payload['params']['documentIds']

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "RQ-01/14",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response_error


@pytestrail.case('C8640')
def test_on_iStorage_behavior_with_params_documentsIds_as_null_in_payload(host, port,
                                                                          response_error,
                                                                          payload_check_registration):
    payload = payload_check_registration(ids=["1"])

    payload['params']['documentIds'] = None

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "RQ-01/14",
            "description": "Can not parse 'params'."
        }
    ]
    assert actualresult == response_error


@pytestrail.case('C8223')
def test_iStorage_returns_response_with_status_error_if_request_contains_unregistered_document(host, port,
                                                                                               response_error,
                                                                                               payload_check_registration):
    payload = payload_check_registration(ids=["21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770"])

    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    response_error['result'] = [
        {
            "code": "VR-01/14",
            "description": "Documents '[21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770]' does not exist"
        }
    ]

    assert actualresult == response_error
