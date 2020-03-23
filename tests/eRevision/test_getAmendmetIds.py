from uuid import uuid4

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
        prepared_cpid, prepared_payload_getAmendmentIds,
        prepared_ev_ocid):
    payload = prepared_payload_getAmendmentIds(relatesTo=relatesTo)

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
                                                                                                       prepared_create_amendment,
                                                                                                       prepared_payload_getAmendmentIds,
                                                                                                       clear_revision_amendments_by_cpid
                                                                                                       ):
    prepared_create_amendment['id'] = f"{prepared_amendment_id}"
    prepared_create_amendment['relatesTo'] = relatesTo
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_getAmendmentIds(relatesTo=relatesTo)

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
                                                                                prepared_payload_getAmendmentIds,
                                                                                prepared_ev_ocid, prepared_cpid):
    payload = prepared_payload_getAmendmentIds()
    del payload['version']

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "1.0.0",
        "id": f"{prepared_request_id}",
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
                                                                                             prepared_create_amendment,
                                                                                             prepared_amendment_id,
                                                                                             prepared_request_id,
                                                                                             prepared_payload_getAmendmentIds):
    prepared_create_amendment['id'] = f"{prepared_amendment_id}"
    prepared_create_amendment['relatesTo'] = "Lot"
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_getAmendmentIds(relatesTo="lot")

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
                                                                                         prepared_payload_getAmendmentIds):
    payload = prepared_payload_getAmendmentIds(version=version)

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
                        "name": "version"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8384')
def test_the_eRevisions_behavior_without_id_in_payload(host, port,
                                                       prepared_payload_getAmendmentIds):
    payload = prepared_payload_getAmendmentIds()
    del payload['id']

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
def test_the_eRevisions_behavior_with_incorrect_id_in_payload(host, port, prepared_payload_getAmendmentIds,
                                                              id, code, description):
    payload = prepared_payload_getAmendmentIds(id=id)

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
def test_the_eRevisions_behavior_without_action_in_payload(port, host, prepared_payload_getAmendmentIds,
                                                           prepared_request_id):
    payload = prepared_payload_getAmendmentIds()
    del payload['action']

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
                                          "Expected values: 'getAmendmentIds, dataValidation, createAmendment',"
                                          " actual value: 'checkItems'.",
                                          marks=pytestrail.case('C8392')),
                             pytest.param(3.14, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'STRING',"
                                          " actual data type: 'NUMBER'.",
                                          marks=pytestrail.case('C8393')),
                             pytest.param(None, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'not null',"
                                          " actual data type: 'null'.",
                                          marks=pytestrail.case('C8394')),
                             pytest.param("", "DR-3/21",
                                          "Attribute value mismatch of 'action' with one of enum expected values."
                                          " Expected values: 'getAmendmentIds, dataValidation, createAmendment',"
                                          " actual value: ''.",
                                          marks=pytestrail.case('C8395')),
                             pytest.param(True, "DR-2/21",
                                          "Data type mismatch of attribute 'action'. Expected data type: 'STRING',"
                                          " actual data type: 'BOOLEAN'.",
                                          marks=pytestrail.case('C8396'))
                         ])
def test_the_eRevisions_behavior_with_invalid_action_in_payload(host, port, prepared_payload_getAmendmentIds,
                                                                prepared_request_id, action, code, description):
    payload = prepared_payload_getAmendmentIds(action=action)

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
def test_the_eRevision_does_not_returns_amendment_ids_without_params_in_payload(port, host,
                                                                                prepared_payload_getAmendmentIds,
                                                                                prepared_request_id):
    payload = prepared_payload_getAmendmentIds()
    del payload['params']

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


@pytest.mark.parametrize("params,code,description",
                         [
                             pytest.param([{}], "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('C8398')),
                             pytest.param({}, "RQ-1/21", "Error parsing 'params'", marks=pytestrail.case('C8399'))
                         ])
def test_the_eRevisions_behavior_with_params_as_array_of_objects_in_payload(host, port, code, description, params,
                                                                            prepared_payload_getAmendmentIds,
                                                                            prepared_request_id,
                                                                            ):
    payload = prepared_payload_getAmendmentIds()
    payload['params'] = params

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

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8400')
def test_the_eRevisions_behavior_without_params_status_in_payload(port, host, prepared_request_id, prepared_ev_ocid,
                                                                  prepared_cpid, prepared_amendment_id,
                                                                  prepared_create_amendment,
                                                                  prepared_payload_getAmendmentIds,
                                                                  execute_insert_into_revision_amendments,
                                                                  clear_revision_amendments_by_cpid):
    prepared_create_amendment['id'] = f"{prepared_amendment_id}"
    prepared_create_amendment['relatesTo'] = 'tender'
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_getAmendmentIds()
    del payload['params']['status']

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


@pytest.mark.parametrize("status,code,description",
                         [
                             pytest.param("activation", "DR-3/21",
                                          "Attribute value mismatch of 'status' with one of enum expected values."
                                          " Expected values: 'pending', actual value: 'activation'.",
                                          marks=pytestrail.case('C8408')),
                             pytest.param(12.33, "DR-3/21",
                                          "Attribute value mismatch of 'status' with one of enum expected values."
                                          " Expected values: 'pending', actual value: '12.33'.",
                                          marks=pytestrail.case('C8432')),
                             pytest.param("", "DR-3/21",
                                          "Attribute value mismatch of 'status' with one of enum expected values."
                                          " Expected values: 'pending', actual value: ''.",
                                          marks=pytestrail.case('C8434')),
                             pytest.param(True, "DR-3/21",
                                          "Attribute value mismatch of 'status' with one of enum expected values."
                                          " Expected values: 'pending', actual value: 'true'.",
                                          marks=pytestrail.case('C8436'))
                         ])
def test_the_eRevisions_behavior_with_invalid_params_status_in_payload(port, host, prepared_request_id,
                                                                       code, description, status,
                                                                       prepared_payload_getAmendmentIds):
    payload = prepared_payload_getAmendmentIds(status=status)

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
                        "name": "status"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8435')
def test_the_eRevisions_behavior_with_null_as_params_status_in_payload(port, host, prepared_request_id,
                                                                       prepared_amendment_id,
                                                                       prepared_ev_ocid, prepared_cpid,
                                                                       prepared_create_amendment,
                                                                       execute_insert_into_revision_amendments,
                                                                       clear_revision_amendments_by_cpid,
                                                                       prepared_payload_getAmendmentIds):
    prepared_create_amendment['id'] = f"{prepared_amendment_id}"
    prepared_create_amendment['relatesTo'] = 'tender'
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_getAmendmentIds(status=None)

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


@pytestrail.case('C8075')
def test_the_eRevisions_behavior_without_params_type_in_payload(port, host, prepared_amendment_id, prepared_ev_ocid,
                                                                execute_insert_into_revision_amendments, prepared_cpid,
                                                                prepared_create_amendment, prepared_request_id,
                                                                clear_revision_amendments_by_cpid,
                                                                prepared_payload_getAmendmentIds):
    data = prepared_create_amendment
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds()
    del payload['params']['type']

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


@pytest.mark.parametrize("type,code,description",
                         [
                             pytest.param("activation", "DR-3/21",
                                          "Attribute value mismatch of 'type' with one of enum expected values. "
                                          "Expected values: 'cancellation', actual value: 'activation'.",
                                          marks=pytestrail.case('C8437')),
                             pytest.param(12.33, "DR-3/21",
                                          "Attribute value mismatch of 'type' with one of enum expected values."
                                          " Expected values: 'cancellation', actual value: '12.33'.",
                                          marks=pytestrail.case('C8438')),
                             pytest.param("", "DR-3/21",
                                          "Attribute value mismatch of 'type' with one of enum expected values. "
                                          "Expected values: 'cancellation', actual value: ''.",
                                          marks=pytestrail.case('C8439')),
                             pytest.param(False, "DR-3/21",
                                          "Attribute value mismatch of 'type' with one of enum expected values. "
                                          "Expected values: 'cancellation', actual value: 'false'.",
                                          marks=pytestrail.case('C8441'))
                         ])
def test_the_eRevisions_behavior_with_invalid_params_type_in_payload(port, host, type, code, description,
                                                                     prepared_payload_getAmendmentIds,
                                                                     prepared_request_id):
    payload = prepared_payload_getAmendmentIds(type=type)

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
                        "name": "type"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8440')
def test_the_eRevisions_behavior_with_null_as_params_type_in_payload(port, host, prepared_create_amendment,
                                                                     prepared_cpid, prepared_ev_ocid,
                                                                     prepared_amendment_id, prepared_request_id,
                                                                     prepared_payload_getAmendmentIds,
                                                                     execute_insert_into_revision_amendments,
                                                                     clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(type=None)

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


@pytest.mark.parametrize("relatedTo,code,description",
                         [
                             pytest.param("bid", "DR-3/21",
                                          "Attribute value mismatch of 'relatesTo' with one of enum expected values."
                                          " Expected values: 'lot, tender', actual value: 'bid'.",
                                          marks=pytestrail.case('C8442')),
                             pytest.param(6.25, "DR-3/21",
                                          "Attribute value mismatch of 'relatesTo' with one of enum expected values."
                                          " Expected values: 'lot, tender', actual value: '6.25'.",
                                          marks=pytestrail.case('C8443')),
                             pytest.param(False, "DR-3/21",
                                          "Attribute value mismatch of 'relatesTo' with one of enum expected values."
                                          " Expected values: 'lot, tender', actual value: 'false'.",
                                          marks=pytestrail.case('C8444')),
                             pytest.param("", "DR-3/21",
                                          "Attribute value mismatch of 'relatesTo' with one of enum expected values."
                                          " Expected values: 'lot, tender', actual value: ''.",
                                          marks=pytestrail.case('C8446'))
                         ])
def test_the_eRevisions_behavior_with_invalid_params_relatesTo_in_payload(host, port, relatedTo, code, description,
                                                                          prepared_payload_getAmendmentIds,
                                                                          prepared_request_id):
    payload = prepared_payload_getAmendmentIds(relatesTo=relatedTo)

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
                        "name": "relatesTo"
                    }
                ]
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8445')
def test_the_eRevisions_behavior_with_null_as_params_relatesTo_in_payload(port, host, prepared_create_amendment,
                                                                          prepared_cpid, prepared_ev_ocid,
                                                                          prepared_amendment_id,
                                                                          prepared_request_id,
                                                                          prepared_payload_getAmendmentIds,
                                                                          execute_insert_into_revision_amendments,
                                                                          clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(relatesTo=None)

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


@pytest.mark.parametrize("param",
                         [
                             pytest.param("relatesTo", marks=pytestrail.case('C8076')),
                             pytest.param("relatedItems", marks=pytestrail.case('C8077'))
                         ])
def test_the_eRevisions_behavior_without_optional_params_in_payload(port, host, param, prepared_create_amendment,
                                                                    prepared_cpid, prepared_ev_ocid,
                                                                    prepared_amendment_id,
                                                                    prepared_request_id,
                                                                    prepared_payload_getAmendmentIds,
                                                                    execute_insert_into_revision_amendments,
                                                                    clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds()
    del payload['params'][param]

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


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8078')),
                             pytest.param("ocid", marks=pytestrail.case('C8457'))
                         ])
def test_the_eRevisions_behavior_without_required_params_in_payload(port, host, param,
                                                                    prepared_request_id,
                                                                    prepared_payload_getAmendmentIds):
    payload = prepared_payload_getAmendmentIds()
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

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8452')
def test_the_eRevisions_behavior_with_invalid_params_cpid_in_payload(port, host, prepared_create_amendment,
                                                                     prepared_cpid, prepared_ev_ocid,
                                                                     prepared_amendment_id,
                                                                     prepared_request_id,
                                                                     prepared_payload_getAmendmentIds,
                                                                     execute_insert_into_revision_amendments,
                                                                     clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(cpid="ocds-t1s2t3-MD-0000000000000")

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("cpid", 3.66, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: '3.66'.",
                                          marks=pytestrail.case('C8453')),
                             pytest.param("cpid", True, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: 'true'.",
                                          marks=pytestrail.case('C8455')),
                             pytest.param("cpid", "", "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: ''.",
                                          marks=pytestrail.case('C8456')),
                             pytest.param("ocid", 3.66, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: '3.66'.",
                                          marks=pytestrail.case('C8459')),
                             pytest.param("ocid", True, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'true'.",
                                          marks=pytestrail.case('C8461')),
                             pytest.param("ocid", "", "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern:"
                                          " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case('C8462')),
                             pytest.param("ocid", "ocds-t1s2t3-MD-1580306096784-EV-1582034422826ghfg", "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: 'ocds-t1s2t3-MD-1580306096784-EV-1582034422826ghfg'.",
                                          marks=pytestrail.case('C8458'))

                         ])
def test_on_eRevisions_behavior_with_number_as_params_cpid_ocid_in_payload(port, host, param, value, code, description,
                                                                           prepared_payload_getAmendmentIds,
                                                                           prepared_request_id):
    payload = prepared_payload_getAmendmentIds()
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


@pytest.mark.parametrize("param,value,code",
                         [
                             pytest.param("cpid", None, "RQ-1/21", marks=pytestrail.case('C8454')),
                             pytest.param("ocid", None, "RQ-1/21", marks=pytestrail.case('C8460'))

                         ])
def test_on_eRevisions_behavior_with_null_as_params_cpid_in_payload(port, host, param, value, code,
                                                                    prepared_payload_getAmendmentIds,
                                                                    prepared_request_id):
    payload = prepared_payload_getAmendmentIds()
    payload['params'][f'{param}'] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error",
        "result": [
            {
                "code": code,
                "description": "Error parsing 'params'"
            }
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytest.mark.parametrize("params",
                         [
                             pytest.param(("relatesTo", "relatedItems"), marks=pytestrail.case('C8615')),
                             pytest.param(("relatesTo", "relatedItems", "type"), marks=pytestrail.case('C8623')),
                             pytest.param(("relatesTo", "relatedItems", "type", "status"),
                                          marks=pytestrail.case('C8622')),
                             pytest.param(("relatesTo", "relatedItems", "status"), marks=pytestrail.case('C8624')),
                             pytest.param(["relatesTo"], marks=pytestrail.case('C8617')),

                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender(host, port, params,
                                                                  prepared_create_amendment,
                                                                  prepared_cpid, prepared_amendment_id,
                                                                  prepared_ev_ocid, prepared_request_id,
                                                                  prepared_payload_getAmendmentIds,
                                                                  execute_insert_into_revision_amendments,
                                                                  clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['relatedItem'] = f"{prepared_ev_ocid}"

    amendmentId1 = uuid4()
    data['id'] = f"{amendmentId1}"
    data['relatesTo'] = 'tender'

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendmentId1,
                                            data=data)

    amendmentId2 = uuid4()
    data['id'] = f"{amendmentId2}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendmentId2,
                                            data=data)

    payload = prepared_payload_getAmendmentIds()

    for param in params:
        del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = [
        f"{amendmentId1}",
        f"{amendmentId2}"
    ]

    assert all(item in expectedresult for item in actualresult['result']), actualresult


@pytestrail.case('C8618')
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_tender_in_params_relatesTo_and_two_ids_in_params_relatedItems(
        host, port,
        prepared_create_amendment,
        prepared_cpid, prepared_amendment_id,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_getAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment
    data['relatedItem'] = f"{prepared_ev_ocid}"

    amendmentId1 = uuid4()
    data['id'] = f"{amendmentId1}"
    data['relatesTo'] = 'tender'

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendmentId1,
                                            data=data)

    amendmentId2 = uuid4()
    data['id'] = f"{amendmentId2}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendmentId2,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(relatesTo="tender")

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = [
        f"{amendmentId1}"
    ]

    assert all(item in expectedresult for item in actualresult['result']), actualresult


@pytest.mark.parametrize("relatesTo,lotId,tenderId",
                         [
                             pytest.param("tender", uuid4(), uuid4(), marks=pytestrail.case('C8619')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_tender_in_params_relatesTo_and_lotId_in_params_relatedItems(
        host, port, relatesTo, lotId, tenderId,
        prepared_create_amendment,
        prepared_cpid,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_getAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment
    data['relatedItem'] = f"{tenderId}"

    data['id'] = f"{tenderId}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=tenderId,
                                            data=data)

    data['relatedItem'] = f"{lotId}"
    data['id'] = f"{lotId}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=lotId,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(relatesTo=relatesTo, relatedItems=f"{lotId}")

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("relatesTo,lotId,tenderId",
                         [
                             pytest.param("lot", uuid4(), uuid4(), marks=pytestrail.case('C8620')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_lot_in_params_relatesTo_and_tender_id_in_params_relatedItems(
        host, port, relatesTo, lotId, tenderId,
        prepared_create_amendment,
        prepared_cpid,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_getAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment
    data['relatedItem'] = f"{tenderId}"

    data['id'] = f"{tenderId}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=tenderId,
                                            data=data)

    data['relatedItem'] = f"{lotId}"
    data['id'] = f"{lotId}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=lotId,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(relatesTo=relatesTo, relatedItems=f"{tenderId}")

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }

    assert actualresult == expectedresult, actualresult


@pytest.mark.parametrize("relatesTo,lotId",
                         [
                             pytest.param("lot", uuid4(), marks=pytestrail.case('C8621')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_lot_in_params_relatesTo_and_tender_id_in_params_relatedItems(
        host, port, relatesTo, lotId,
        prepared_create_amendment,
        prepared_cpid, prepared_amendment_id,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_getAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment
    data['relatedItem'] = f"{lotId}"

    data['id'] = f"{lotId}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=lotId,
                                            data=data)

    data['relatedItem'] = f"{lotId}"
    data['id'] = f"{prepared_amendment_id}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=prepared_amendment_id,
                                            data=data)

    payload = prepared_payload_getAmendmentIds(relatesTo=relatesTo, relatedItems=f"{lotId}")

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = [
        f"{lotId}",
        f"{prepared_amendment_id}"
    ]

    assert all(item in expectedresult for item in actualresult['result']), actualresult
