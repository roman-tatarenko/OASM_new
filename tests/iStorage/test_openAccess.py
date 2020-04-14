import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8186')
def test_iStorage_returns_successful_response_if_there_is_registered_and_uploaded_document(host, port,
                                                                                           registering_document,
                                                                                           upload_document, response,
                                                                                           payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    url = registration_data['data']['url']
    upload_document(dir_path=dir_path, file_name=file_name, doc_id=doc_id)
    date_published = "2020-04-10T06:55:03Z"
    payload = payload_openAccess(ids=[doc_id], datePublished=date_published)
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.success["result"] = [{
        "id": doc_id,
        "datePublished": date_published,
        "uri": url
    }]

    assert actualresult == response.success


@pytestrail.case('C8196')
def test_iStorage_returns_successful_response_if_there_is_registered_and_not_uploaded_document(host, port,
                                                                                               registering_document,
                                                                                               response,
                                                                                               payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    url = registration_data['data']['url']
    date_published = "2020-04-10T06:55:03Z"
    payload = payload_openAccess(ids=[doc_id], datePublished=date_published)
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.success["result"] = [{
        "id": doc_id,
        "datePublished": date_published,
        "uri": url
    }]

    assert actualresult == response.success


@pytestrail.case('C8187')
def test_iStorage_returns_successful_response_if_there_more_than_one_document(host, port,
                                                                              registering_document,
                                                                              response,
                                                                              payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    date_published = "2020-04-10T06:55:03Z"
    registration_data_1 = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id_1 = registration_data_1['data']['id']
    url_1 = registration_data_1['data']['url']
    registration_data_2 = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id_2 = registration_data_2['data']['id']
    url_2 = registration_data_2['data']['url']
    payload = payload_openAccess(ids=[doc_id_1, doc_id_2], datePublished=date_published)
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.success["result"] = [{
        "id": doc_id_1,
        "datePublished": date_published,
        "uri": url_1
    },
        {
            "id": doc_id_2,
            "datePublished": date_published,
            "uri": url_2
        }
    ]

    assert all(item in response.success["result"] for item in actualresult['result'])


@pytestrail.case('C8188')
def test_iStorage_behavior_when_there_are_two_documents_with_the_same_id_in_request(host, port,
                                                                                    registering_document,
                                                                                    upload_document, response,
                                                                                    payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    date_published = "2020-04-10T06:55:03Z"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    url = registration_data['data']['url']
    payload = payload_openAccess(ids=[doc_id, doc_id], datePublished=date_published)
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.success["result"] = [{
        "id": doc_id,
        "datePublished": date_published,
        "uri": url
    }]

    assert actualresult == response.success


@pytestrail.case('C8189')
def test_iStorage_if_at_least_one_document_from_request_is_not_registered(host, port,
                                                                          registering_document,
                                                                          response, prepared_entity_id,
                                                                          payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data_1 = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id_1 = registration_data_1['data']['id']
    doc_id_2 = str(prepared_entity_id())
    payload = payload_openAccess(ids=[doc_id_1, doc_id_2], datePublished="2020-04-10T06:55:03Z")
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id_2}]' does not exist"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8199')
def test_iStorage_returns_response_with_status_error_if_request_contains_unregistered_document(host, port,
                                                                                               response,
                                                                                               payload_openAccess):
    payload = payload_openAccess(ids=["21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770"],
                                 datePublished="2020-04-10T06:55:03Z")
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": "Documents '[21ce3aa5-1e3c-4d17-89d2-483dbe323e96-1584686037770]' does not exist"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8194')
def test_iStorage_returns_response_with_status_error_if_request_contains_empty_params_object(host, port,
                                                                                             response,
                                                                                             payload_openAccess):
    payload = payload_openAccess(ids=["1"], datePublished="2020-04-10T06:55:03Z")
    del payload['params']['documentIds']
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-01/14",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8191')
def test_iStorage_if_the_request_contains_documentIds_value_that_does_not_match_the_pattern(
        host, port,
        response,
        prepared_entity_id,
        payload_openAccess):
    doc_id = str(prepared_entity_id())
    payload = payload_openAccess(ids=[doc_id], datePublished="2020-04-10T06:55:03Z")
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-01/14",
            "description": f"Documents '[{doc_id}]' does not exist"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C8197')
def test_iStorage_if_access_to_document_from_request_has_been_opened_before(host, port,
                                                                            registering_document,
                                                                            upload_document, response,
                                                                            payload_openAccess):
    dir_path = "tests/iStorage/data/"
    file_name = "cofeebreak2.pdf"
    registration_data = registering_document(dir_path=dir_path, file_name=file_name)
    doc_id = registration_data['data']['id']
    url = registration_data['data']['url']
    upload_document(dir_path=dir_path, file_name=file_name, doc_id=doc_id)
    date_published = "2020-04-10T06:55:03Z"
    payload = payload_openAccess(ids=[doc_id], datePublished=date_published)
    requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    actualresult = requests.post(f'{host}:{port.iStorage}/command2', json=payload).json()
    response.success["result"] = [{
        "id": doc_id,
        "datePublished": date_published,
        "uri": url
    }]

    assert actualresult == response.success
