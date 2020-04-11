import json
import uuid

import pytest
import pytest_check as check
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
    related_entity_id = prepared_entity_id()
    payload = prepared_payload_createAmendment(amendment_id=related_entity_id)
    payload['params']['operationType'] = operationType
    payload['params']['relatedEntityId'] = f"{related_entity_id}"

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = value

    assert actualresult['result'][param] == expectedresult, print(actualresult)


@pytest.mark.parametrize("operationType",
                         [
                             pytest.param("tenderCancellation", marks=pytestrail.case('C8341')),
                             pytest.param("lotCancellation", marks=pytestrail.case('C8614'))

                         ])
def test_the_eRevision_correctly_sets_value_for_result_relatedItem(port, host, operationType,
                                                                   prepared_entity_id,
                                                                   prepared_payload_createAmendment):
    related_entity_id = prepared_entity_id()
    payload = prepared_payload_createAmendment(amendment_id=related_entity_id)
    payload['params']['operationType'] = operationType
    payload['params']['relatedEntityId'] = f"{related_entity_id}"

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = f"{related_entity_id}"

    assert actualresult['result']['relatedItem'] == expectedresult, actualresult


@pytestrail.case('C8344')
def test_the_eRevision_sets_result_token(port, host, prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert uuid.UUID(actualresult['result']['token']), actualresult


@pytestrail.case('C8343')
def test_the_eRevision_correctly_sets_value_for_result_date(port, host,
                                                            prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult['result']['date'] == payload['params']['startDate'], actualresult


@pytest.mark.parametrize("param,code,description",
                         [
                             pytest.param("amendment", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8206')),
                             pytest.param("relatedEntityId", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8317')),
                             pytest.param("owner", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8228')),
                             pytest.param("ocid", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8227')),
                             pytest.param("cpid", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8222')),
                             pytest.param("startDate", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8221')),
                             pytest.param("operationType", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8220')),

                         ])
def test_on_impossibility_to_create_amendment_without_param_in_params(port, host, param, code, description,
                                                                      prepared_request_id,
                                                                      prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description
            }
        ]
    }

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("amendment", [], "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8281')),
                             pytest.param("owner", None, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8338')),

                             pytest.param("ocid", None, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8335')),
                             pytest.param("ocid", True, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'true'.",
                                          marks=pytestrail.case('C8334')),
                             pytest.param("ocid", 3.14, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: '3.14'.",
                                          marks=pytestrail.case('C8333')),
                             pytest.param("cpid", True, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: 'true'.",
                                          marks=pytestrail.case('C8331')),
                             pytest.param("cpid", 3.14, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: '3.14'.",
                                          marks=pytestrail.case('C8329')),
                             pytest.param("cpid", None, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8330')),
                             pytest.param("startDate", None, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8328')),
                             pytest.param("startDate", "", "DR-4/21",
                                          "Data format mismatch of attribute 'startDate'."
                                          " Expected data format: 'uuuu-MM-dd'T'HH:mm:ss'Z'', actual value: ''.",
                                          marks=pytestrail.case('C8327')),
                             pytest.param("startDate", 32, "DR-4/21",
                                          "Data format mismatch of attribute 'startDate'."
                                          " Expected data format: 'uuuu-MM-dd'T'HH:mm:ss'Z'', actual value: '32'.",
                                          marks=pytestrail.case('C8326')),
                             pytest.param("operationType", None, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8324')),
                             pytest.param("operationType", "", "DR-3/21",
                                          "Attribute value mismatch of 'operationType' "
                                          "with one of enum expected values. Expected values: "
                                          "'tenderCancellation, lotCancellation', actual value: ''.",
                                          marks=pytestrail.case('C8323')),
                             pytest.param("operationType", 233, "DR-3/21",
                                          "Attribute value mismatch of 'operationType' with one of enum expected values."
                                          " Expected values: 'tenderCancellation, lotCancellation', actual value: '233'.",
                                          marks=pytestrail.case('C8322')),
                             pytest.param("operationType", "checkItems", "DR-3/21",
                                          "Attribute value mismatch of 'operationType' with one of enum expected values."
                                          " Expected values: 'tenderCancellation, lotCancellation', actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8321')),
                             pytest.param("relatedEntityId", None, "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8320'))

                         ])
def test_on_impossibility_to_create_amendment_with_invalid_param_in_params(port, host, param, value, code,
                                                                           description, prepared_request_id,
                                                                           prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description
            }
        ]
    }

    if param in {"ocid", "cpid", "operationType", "startDate"} and value is not None:
        expectedresult['result'] = [
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

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("documents", {}, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8297')),
                             pytest.param("id", "", "DR-4/21",
                                          "Data format mismatch of attribute"
                                          " 'amendment.id'. Expected data format: 'UUID', actual value: ''.",
                                          marks=pytestrail.case('C8316')),
                             pytest.param("id", True, "DR-4/21",
                                          "Data format mismatch of attribute 'amendment.id'."
                                          " Expected data format: 'UUID', actual value: 'true'.",
                                          marks=pytestrail.case('C8315')),

                         ])
def test_on_impossibility_to_create_amendment_with_invalid_param_in_amendment(port, host, param, value, code,
                                                                              description, prepared_request_id,
                                                                              prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    payload['params']['amendment'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description
            }
        ]
    }
    if param == "id":
        param = "amendment.id"
        expectedresult['result'] = [
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

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,code,description",
                         [
                             pytest.param("rationale", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8207')),
                             pytest.param("id", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8218'))

                         ])
def test_on_impossibility_to_create_amendment_without_param_in_amendment(port, host, param, code, description,
                                                                         prepared_request_id,
                                                                         prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    del payload['params']['amendment'][param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description
            }
        ]
    }

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("documentType", 32.655, "DR-3/21",
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          " Expected values: 'cancellationDetails', actual value: '32.655'.",
                                          marks=pytestrail.case('C8298')),
                             pytest.param("documentType", False, "DR-3/21",
                                          "Attribute value mismatch of 'documentType' with one of enum expected values."
                                          " Expected values: 'cancellationDetails', actual value: 'false'.",
                                          marks=pytestrail.case('C8300')),
                             pytest.param("title", None, "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8306')),
                             pytest.param("id", None, "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8301')),
                             pytest.param("documentType", None, "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8210'))
                         ])
def test_on_impossibility_to_create_amendment_with_invalid_param_in_document(port, host, param, value, code,
                                                                             description, prepared_request_id,
                                                                             prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    payload['params']['amendment']['documents'][0][param] = value
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

    if value is None:
        expectedresult['result'] = [
            {
                "code": code,
                "description": description
            }
        ]

    assert actualresult == expectedresult


@pytest.mark.parametrize("param,code,description",
                         [

                             pytest.param("id", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8212')),
                             pytest.param("title", "RQ-1/21", "Error parsing 'params'",
                                          marks=pytestrail.case('C8213'))

                         ])
def test_on_impossibility_to_create_amendment_without_param_in_amendment_document(port, host, param, code, description,
                                                                                  prepared_request_id,
                                                                                  prepared_payload_createAmendment):
    payload = prepared_payload_createAmendment()
    del payload['params']['amendment']['documents'][0][param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description
            }
        ]
    }

    assert actualresult == expectedresult


@pytestrail.case('C8308')
def test_on_possibility_to_create_amendment_without_params_amendment_documents_description(port, host,
                                                                                           prepared_payload_createAmendment,
                                                                                           prepared_request_id):
    payload = prepared_payload_createAmendment()
    del payload['params']['amendment']['documents'][0]['description']

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = [{
        "documentType": "cancellationDetails",
        "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
        "title": "amendments documents title"

    }]
    check.equal(actualresult['status'], "success")
    assert all(item in expectedresult for item in actualresult['result']['documents']), actualresult


@pytestrail.case('C8209')
def test_on_possibility_to_create_amendment_for_tender_without_params_amendment_documents(port, host, prepared_ev_ocid,
                                                                                          prepared_request_id,
                                                                                          prepared_payload_createAmendment
                                                                                          ):
    payload = prepared_payload_createAmendment()
    del payload['params']['amendment']['documents']

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": {
            "rationale": "Some_string_1",
            "description": "Some_string_2",
            "date": "2020-02-28T16:14:54Z",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItem": f"{prepared_ev_ocid}"
        }
    }
    check.equal(expectedresult['status'], "success")
    check.equal(expectedresult['id'], f"{prepared_request_id}")

    assert all(item in actualresult['result'] for item in expectedresult['result']), actualresult


@pytestrail.case('C8208')
def test_on_possibility_to_create_amendment_for_tender_without_params_amendment_description(port, host,
                                                                                            prepared_ev_ocid,
                                                                                            prepared_request_id,
                                                                                            prepared_payload_createAmendment
                                                                                            ):
    payload = prepared_payload_createAmendment()
    del payload['params']['amendment']['description']

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": {
            "rationale": "Some_string_1",
            "documents": [
                {
                    "documentType": "cancellationDetails",
                    "id": "845b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                    "title": "amendments documents title",
                    "description": "amendments documents description"
                }
            ],
            "date": "2020-02-28T16:14:54Z",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "lot/tender",
            "relatedItem": "lot_id/tender_ocid"
        }
    }
    check.equal(expectedresult['status'], "success")
    check.equal(expectedresult['id'], f"{prepared_request_id}")

    assert all(item in actualresult['result'] for item in expectedresult['result']), actualresult


@pytest.mark.parametrize("param,value",
                         [
                             pytest.param("tender", "tenderCancellation", marks=pytestrail.case('C8649')),
                             pytest.param("lot", "lotCancellation", marks=pytestrail.case('C8650')),

                         ])
def test_the_eRevision_correctly_inserts_DB_record_for_tender_cancellation(port, host, param, value, prepared_entity_id,
                                                                           prepared_request_id, prepared_ev_ocid,
                                                                           prepared_cpid,
                                                                           prepared_payload_createAmendment,
                                                                           execute_select_revision_amendments_by_id):
    related_entity_id = prepared_entity_id()
    amendment_id = prepared_entity_id()
    payload = prepared_payload_createAmendment(amendment_id=amendment_id)
    payload['params']['relatedEntityId'] = f"{related_entity_id}"
    payload['params']['operationType'] = value

    requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    actual_result = execute_select_revision_amendments_by_id(cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                                             id=amendment_id).one()

    actual_data = json.loads(actual_result.data)

    expected_data = {
        "id": f"{amendment_id}",
        "date": "2020-02-28T16:14:54Z",
        "rationale": "Some_string_1",
        "description": "Some_string_2",
        "status": "pending",
        "type": "cancellation",
        "relatesTo": f"{param}",
        "relatedItem": f"{related_entity_id}",
        "token": f"{actual_data['token']}",
        "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "documents": [{
            "documentType": "cancellationDetails",
            "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
            "title": "amendments documents title",
            "description": "amendments documents description"
        }]
    }

    check.equal(actual_result.cpid, prepared_cpid)
    check.equal(actual_result.ocid, prepared_ev_ocid)
    check.equal(actual_result.id, amendment_id)
    check.equal(actual_data, expected_data)


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("rationale", 3.14, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8282')),
                             pytest.param("rationale", "", "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8283')),
                             pytest.param("rationale", True, "RQ-1/21",
                                          "Error parsing 'params'",
                                          marks=pytestrail.case('C8286'))
                         ])
def test_on_impossibility_to_create_amendment_with_invalid_param_rationale_in_amendment(port, host, param, value, code,
                                                                                        description,
                                                                                        prepared_request_id,
                                                                                        prepared_entity_id,
                                                                                        prepared_payload_createAmendment,
                                                                                        prepared_ev_ocid):
    amendment_id = prepared_entity_id()
    payload = prepared_payload_createAmendment(amendment_id=amendment_id)
    payload['params']['amendment'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    del actualresult['result']['token']

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": {
            "rationale": f"{value}",
            "description": "Some_string_2",
            "documents": [
                {
                    "documentType": "cancellationDetails",
                    "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                    "title": "amendments documents title",
                    "description": "amendments documents description"
                }
            ],
            "id": f"{amendment_id}",
            "date": "2020-02-28T16:14:54Z",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItem": f"{prepared_ev_ocid}",
        }
    }

    if f"{value}" == "True":
        expectedresult['result']['rationale'] = "true"

    assert actualresult == expectedresult
