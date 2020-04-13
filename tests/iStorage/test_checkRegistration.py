import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8097')
def test_iStorage_if_there_is_registered_and_uploaded_document_in_request(host, port,
                                                                          response,
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

    assert actualresult == response.success


@pytestrail.case('C8195')
def test_iStorage_if_there_is_registered_and_not_uploaded_document_in_request(host, port,
                                                                              response,
                                                                              registering_document,
                                                                              upload_document,
                                                                              payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    payload = payload_check_registration(ids=[doc_id])
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C8100')
def test_iStorage_returns_successful_response_if_there_is_more_than_one_registered_document_in_request(host, port,
                                                                                                       response,
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

    assert actualresult == response.success


@pytestrail.case('C8103')
def test_iStorage_behavior_when_there_are_two_documents_with_the_same_id_in_request(host, port,
                                                                                    response,
                                                                                    registering_document,
                                                                                    upload_document,
                                                                                    payload_check_registration):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    payload = payload_check_registration(ids=[doc_id, doc_id])
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C8098')
def test_iStorage_if_at_least_one_document_from_request_is_not_registered(host, port,
                                                                          response,
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
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id_2}]' does not exist"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8105')
def test_iStorage_returns_if_the_request_contains_documentIds_value_that_does_not_match_the_pattern(
        host, port,
        response,
        prepared_entity_id,
        payload_check_registration):
    doc_id = str(prepared_entity_id())
    payload = payload_check_registration(ids=[doc_id])
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id}]' does not exist"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8109')
def test_iStorage_if_request_contains_empty_documentIds_array(port, host,
                                                              payload_check_registration,
                                                              response
                                                              ):
    payload = payload_check_registration(ids=[])
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


@pytestrail.case('C8108')
def test_iStorage_if_request_contains_empty_params_object(host, port,
                                                          response,
                                                          payload_check_registration):
    payload = payload_check_registration(ids=["1"])
    del payload['params']['documentIds']
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/14",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8640')
def test_on_iStorage_behavior_with_params_documentsIds_as_null_in_payload(host, port,
                                                                          response,
                                                                          payload_check_registration):
    payload = payload_check_registration(ids=["1"])
    payload['params']['documentIds'] = None
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/14",
            "description": "Can not parse 'params'."
        }
    ]
    assert actualresult == response.error


@pytestrail.case('C8223')
def test_iStorage_returns_response_with_status_error_if_request_contains_unregistered_document(host, port,
                                                                                               response,
                                                                                               payload_check_registration):
    payload = payload_check_registration(ids=["21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770"])
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": "Documents '[21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770]' does not exist"
        }
    ]

    assert actualresult == response.error
