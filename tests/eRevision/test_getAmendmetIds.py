import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.skip
@pytest.mark.parametrize("relatesTo",
                         [pytest.param("tender", marks=pytestrail.case('C8061')),
                          pytest.param("lot", marks=pytestrail.case('C8066'))])
def test_the_eRevision_does_not_return_amendment_ids_if_there_is_no_amendments_in_pending_status_for_(
        host, port, relatesTo,
        prepared_request_id,
        prepared_cpid,
        prepared_ev_ocid):
    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": relatesTo,
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }
    assert expectedresult == actualresult


@pytest.mark.parametrize("relatesTo",
                         [pytest.param("tender", marks=pytestrail.case('C8104')),
                          pytest.param("lot", marks=pytestrail.case('C8378'))])
def test_the_eRevision_return_amendment_ids_if_there_is_amendments_in_pending_cancellation_status_for_(port, host,
                                                                                                       relatesTo,
                                                                                                       execute_insert_into_revision_amendments,
                                                                                                       prepared_cpid,
                                                                                                       prepared_ev_ocid,
                                                                                                       prepared_amendment_id,
                                                                                                       prepared_request_id,
                                                                                                       clear_revision_amendments_by_cpid
                                                                                                       ):
    data = {
        "amendment": {
            "id": f"{prepared_amendment_id}",
            "date": "2019-04-01T10:00:00Z",
            "rationale": "Some_text",
            "description": "Some_text_2",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": relatesTo,
            "relatedItem": f"{prepared_ev_ocid}",
            "documents": [{
                "documentType": "cancellationDetails",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "string",
                "description": "string"
            }],
            "token": "ed8e86b9-82c9-4bcc-ac40-215317afa211",
            "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
    }
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": relatesTo,
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": [
            f"{prepared_amendment_id}"
        ]
    }
    assert expectedresult == actualresult, prepared_cpid


@pytest.mark.parametrize("relatesTo",
                         [pytest.param("tender", marks=pytestrail.case('C8067')),
                          pytest.param("lot", marks=pytestrail.case('C8067'))])
def test_the_eRevision_does_not_return_amendment_ids_without_version_in_payload(port, host, relatesTo,
                                                                                prepared_request_id,
                                                                                prepared_ev_ocid, prepared_cpid):
    payload = {
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": relatesTo,
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "1.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "error",
        "result": [
            {
                "code": "DR-1/21",
                "description": "Missing required attribute 'version'.",
                "details": [
                    {
                        "name": "version"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8391')
def test_the_eRevision_return_amendment_ids_if_there_is_amendments_in_pending_status_for_lot(host, port,
                                                                                             execute_insert_into_revision_amendments,
                                                                                             clear_revision_amendments_by_cpid,
                                                                                             prepared_cpid,
                                                                                             prepared_ev_ocid,
                                                                                             prepared_amendment_id,
                                                                                             prepared_request_id):
    data = {
        "amendment": {
            "id": f"{prepared_amendment_id}",
            "date": "2019-04-01T10:00:00Z",
            "rationale": "Some_text",
            "description": "Some_text_2",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "lot",
            "relatedItem": f"{prepared_ev_ocid}",
            "documents": [{
                "documentType": "cancellationDetails",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "string",
                "description": "string"
            }],
            "token": "ed8e86b9-82c9-4bcc-ac40-215317afa211",
            "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
    }

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "lot",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": [
            f"{prepared_amendment_id}"
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("version,code,description",
                         [pytest.param(3, "DR-2/21",
                                       "Data type mismatch of attribute 'version'. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                       marks=pytestrail.case('C8379')),
                          pytest.param(False, "DR-2/21",
                                       "Data type mismatch of attribute 'version'. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                       marks=pytestrail.case('C8380')),
                          pytest.param(None, "DR-2/21",
                                       "Data type mismatch of attribute 'version'. Expected data type: 'not null', actual data type: 'null'.",
                                       marks=pytestrail.case('C8381')),
                          pytest.param("", "DR-4/21",
                                       "Data format mismatch of attribute 'version'. Expected data format: '00.00.00', actual value: ''.",
                                       marks=pytestrail.case('C8382'))
                          ])
def test_the_eRevisions_does_not_returns_amendment_ids_with_incorrect_version_in_payload(host, port, version, code,
                                                                                         description,
                                                                                         prepared_request_id,
                                                                                         prepared_ev_ocid,
                                                                                         prepared_cpid):
    payload = {
        "version": version,
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description,
                "details": [
                    {
                        "name": "version"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8384')
def test_the_eRevisions_behavior_without_id_in_payload(host, port, prepared_ev_ocid,
                                                       prepared_cpid):
    payload = {
        "version": "2.0.0",
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "error",
        "result": [
            {
                "code": "DR-1/21",
                "description": "Missing required attribute 'id'.",
                "details": [
                    {
                        "name": "id"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("id,code,description",
                         [pytest.param(3.14, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                       marks=pytestrail.case('C8386')),
                          pytest.param(False, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                       marks=pytestrail.case('C8387')),
                          pytest.param(None, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'not null', actual data type: 'null'.",
                                       marks=pytestrail.case('C8388')),
                          pytest.param("", "DR-4/21",
                                       "Data format mismatch of attribute 'id'. Expected data format: 'uuid', actual value: ''.",
                                       marks=pytestrail.case('C8389'))
                          ])
def test_the_eRevisions_behavior_with_incorrect_id_in_payload(host, port, prepared_ev_ocid,
                                                              prepared_cpid, id, code, description):
    payload = {
        "version": "2.0.0",
        "id": id,
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description,
                "details": [
                    {
                        "name": "id"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("id,code,description",
                         [pytest.param(3.14, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                       marks=pytestrail.case('C8386')),
                          pytest.param(False, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                       marks=pytestrail.case('C8387')),
                          pytest.param(None, "DR-2/21",
                                       "Data type mismatch of attribute 'id'. Expected data type: 'not null', actual data type: 'null'.",
                                       marks=pytestrail.case('C8388')),
                          pytest.param("", "DR-4/21",
                                       "Data format mismatch of attribute 'id'. Expected data format: 'uuid', actual value: ''.",
                                       marks=pytestrail.case('C8389'))
                          ])
def test_the_eRevisions_behavior_with_incorrect_id_in_payload(host, port, prepared_ev_ocid,
                                                              prepared_cpid, id, code, description):
    payload = {
        "version": "2.0.0",
        "id": id,
        "action": "getAmendmentIds",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": "00000000-0000-0000-0000-000000000000",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": description,
                "details": [
                    {
                        "name": "id"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8390')
def test_the_eRevisions_behavior_without_action_in_payload(port, host, prepared_ev_ocid, prepared_cpid,
                                                           prepared_request_id):
    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-1/21",
                "description": "Missing required attribute 'action'.",
                "details": [
                    {
                        "name": "action"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("action,code,description",
                         [
                             pytest.param("checkItems", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values. "
                                          "Expected values: 'getAmendmentIds, dataValidation, createAmendment', actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8392')),
                             pytest.param(3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'STRING', actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8393')),
                             pytest.param(None, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'not null', actual data type: 'null'.",
                                          marks=pytestrail.case('C8394')),
                             pytest.param("", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values: 'getAmendmentIds, dataValidation, createAmendment', actual value: ''.",
                                          marks=pytestrail.case('C8395')),
                             pytest.param(True, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'STRING', actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8396'))
                         ])
def test_the_eRevisions_behavior_with_invalid_action_in_payload(host, port, prepared_ev_ocid, prepared_request_id,
                                                                prepared_cpid, action, code, description):
    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": action,
        "params": {
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItems": [f"{prepared_ev_ocid}"],
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}"
        }
    }
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
                        "name": "action"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8397')
def test_the_eRevision_does_not_returns_amendment_ids_without_params_in_payload(port, host, prepared_request_id):
    payload = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "getAmendmentIds"
    }
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": "DR-1/21",
                "description": "Missing required attribute 'params'.",
                "details": [
                    {
                        "name": "params"
                    }
                ]
            }
        ]
    }
    assert expectedresult == actualresult, actualresult
