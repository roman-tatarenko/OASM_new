from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytest.mark.parametrize('relatesTo',
                         [pytest.param('tender', marks=pytestrail.case('C8104')),
                          pytest.param('lot', marks=pytestrail.case('C8378'))])
def test_the_eRevision_return_amendment_ids_if_there_is_amendments_in_pending_cancellation_status_for_(port, host,
                                                                                                       relatesTo,
                                                                                                       execute_insert_into_revision_amendments,
                                                                                                       prepared_cpid,
                                                                                                       prepared_ev_ocid,
                                                                                                       prepared_entity_id,
                                                                                                       prepared_request_id,
                                                                                                       prepared_create_amendment,
                                                                                                       prepared_payload_findAmendmentIds,
                                                                                                       clear_revision_amendments_by_cpid,
                                                                                                       response
                                                                                                       ):
    amendment_id = prepared_entity_id()
    prepared_create_amendment['id'] = f"{amendment_id}"
    prepared_create_amendment['relatesTo'] = relatesTo
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=prepared_create_amendment)
    payload = prepared_payload_findAmendmentIds(relatesTo=relatesTo)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


@pytestrail.case('C8391')
def test_the_eRevision_return_amendment_ids_if_there_is_amendments_in_pending_status_for_lot(host, port, response,
                                                                                             execute_insert_into_revision_amendments,
                                                                                             clear_revision_amendments_by_cpid,
                                                                                             prepared_cpid,
                                                                                             prepared_ev_ocid,
                                                                                             prepared_create_amendment,
                                                                                             prepared_entity_id,
                                                                                             prepared_request_id,
                                                                                             prepared_payload_findAmendmentIds):
    amendment_id = prepared_entity_id()
    prepared_create_amendment['id'] = f"{amendment_id}"
    prepared_create_amendment['relatesTo'] = 'Lot'
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_findAmendmentIds(relatesTo='lot')
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


@pytestrail.case('C8400')
def test_the_eRevisions_behavior_without_params_status_in_payload(port, host, prepared_request_id, prepared_ev_ocid,
                                                                  prepared_cpid, prepared_entity_id,
                                                                  prepared_create_amendment, response,
                                                                  prepared_payload_findAmendmentIds,
                                                                  execute_insert_into_revision_amendments,
                                                                  clear_revision_amendments_by_cpid):
    amendment_id = prepared_entity_id()
    prepared_create_amendment['id'] = f"{amendment_id}"
    prepared_create_amendment['relatesTo'] = 'tender'
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=prepared_create_amendment)
    payload = prepared_payload_findAmendmentIds()
    del payload['params']['status']
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


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
                                                                       code, description, status, response,
                                                                       prepared_payload_findAmendmentIds):
    payload = prepared_payload_findAmendmentIds(status=status)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


@pytestrail.case('C8435')
def test_the_eRevisions_behavior_with_null_as_params_status_in_payload(port, host, prepared_request_id,
                                                                       prepared_entity_id,
                                                                       prepared_ev_ocid, prepared_cpid,
                                                                       prepared_create_amendment,
                                                                       execute_insert_into_revision_amendments,
                                                                       clear_revision_amendments_by_cpid,
                                                                       prepared_payload_findAmendmentIds):
    amendment_id = prepared_entity_id()
    prepared_create_amendment['id'] = f"{amendment_id}"
    prepared_create_amendment['relatesTo'] = 'tender'
    prepared_create_amendment['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=prepared_create_amendment)

    payload = prepared_payload_findAmendmentIds(status=None)

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": [
            f"{amendment_id}"
        ]
    }

    assert expectedresult == actualresult, actualresult


@pytestrail.case('C8075')
def test_the_eRevisions_behavior_without_params_type_in_payload(port, host, prepared_entity_id, prepared_ev_ocid,
                                                                execute_insert_into_revision_amendments, prepared_cpid,
                                                                prepared_create_amendment, prepared_request_id,
                                                                clear_revision_amendments_by_cpid,
                                                                prepared_payload_findAmendmentIds):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = f"{amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"

    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=data)

    payload = prepared_payload_findAmendmentIds()
    del payload['params']['type']

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    expectedresult = {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success",
        "result": [
            f"{amendment_id}"
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
                                                                     prepared_payload_findAmendmentIds,
                                                                     prepared_request_id, response):
    payload = prepared_payload_findAmendmentIds(type=type)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


@pytestrail.case('C8440')
def test_the_eRevisions_behavior_with_null_as_params_type_in_payload(port, host, prepared_create_amendment,
                                                                     prepared_cpid, prepared_ev_ocid,
                                                                     prepared_entity_id, prepared_request_id,
                                                                     prepared_payload_findAmendmentIds,
                                                                     execute_insert_into_revision_amendments,
                                                                     clear_revision_amendments_by_cpid, response):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = f"{amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=data)
    payload = prepared_payload_findAmendmentIds(type=None)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


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
                                                                          prepared_payload_findAmendmentIds,
                                                                          prepared_request_id, response):
    payload = prepared_payload_findAmendmentIds(relatesTo=relatedTo)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
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

    assert actualresult == response.error


@pytestrail.case('C8445')
def test_the_eRevisions_behavior_with_null_as_params_relatesTo_in_payload(port, host, prepared_create_amendment,
                                                                          prepared_cpid, prepared_ev_ocid,
                                                                          prepared_entity_id, response,
                                                                          prepared_request_id,
                                                                          prepared_payload_findAmendmentIds,
                                                                          execute_insert_into_revision_amendments,
                                                                          clear_revision_amendments_by_cpid):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = f"{amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=data)
    payload = prepared_payload_findAmendmentIds(relatesTo=None)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param("relatesTo", marks=pytestrail.case('C8076')),
                             pytest.param("relatedItems", marks=pytestrail.case('C8077'))
                         ])
def test_the_eRevisions_behavior_without_optional_params_in_payload(port, host, param, prepared_create_amendment,
                                                                    prepared_cpid, prepared_ev_ocid,
                                                                    prepared_entity_id, response,
                                                                    prepared_request_id,
                                                                    prepared_payload_findAmendmentIds,
                                                                    execute_insert_into_revision_amendments,
                                                                    clear_revision_amendments_by_cpid):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = f"{amendment_id}"
    data['relatesTo'] = 'tender'
    data['relatedItem'] = f"{prepared_ev_ocid}"
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=data)
    payload = prepared_payload_findAmendmentIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        f"{amendment_id}"
    ]

    assert actualresult == response.success


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid", marks=pytestrail.case('C8078')),
                             pytest.param("ocid", marks=pytestrail.case('C8457'))
                         ])
def test_the_eRevisions_behavior_without_required_params_in_payload(port, host, param, response,
                                                                    prepared_request_id,
                                                                    prepared_payload_findAmendmentIds):
    payload = prepared_payload_findAmendmentIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


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
                                                                           prepared_payload_findAmendmentIds,
                                                                           prepared_request_id, response):
    payload = prepared_payload_findAmendmentIds()
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


@pytest.mark.parametrize("param,value,code",
                         [
                             pytest.param("cpid", None, "RQ-1/21", marks=pytestrail.case('C8454')),
                             pytest.param("ocid", None, "RQ-1/21", marks=pytestrail.case('C8460'))

                         ])
def test_on_eRevisions_behavior_with_null_as_params_cpid_in_payload(port, host, param, value, code,
                                                                    prepared_payload_findAmendmentIds,
                                                                    prepared_request_id, response):
    payload = prepared_payload_findAmendmentIds()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error["result"] = [
        {
            "code": code,
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("params",
                         [
                             pytest.param(("relatesTo", "relatedItems"), marks=pytestrail.case('C8615'),
                                          id="relatesTo/relatedItems"),
                             pytest.param(("relatesTo", "relatedItems", "type"), marks=pytestrail.case('C8623')),
                             pytest.param(("relatesTo", "relatedItems", "type", "status"),
                                          marks=pytestrail.case('C8622')),
                             pytest.param(("relatesTo", "relatedItems", "status"), marks=pytestrail.case('C8624')),
                             pytest.param(["relatesTo"], marks=pytestrail.case('C8617'))
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender(host, port, params,
                                                                  prepared_create_amendment,
                                                                  prepared_cpid, prepared_entity_id,
                                                                  prepared_ev_ocid, prepared_request_id,
                                                                  prepared_payload_findAmendmentIds,
                                                                  execute_insert_into_revision_amendments,
                                                                  clear_revision_amendments_by_cpid):
    data = prepared_create_amendment
    data['relatedItem'] = f"{prepared_ev_ocid}"
    amendment_id_1 = prepared_entity_id()
    data['id'] = f"{amendment_id_1}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id_1,
                                            data=data)
    amendment_id_2 = prepared_entity_id()
    data['id'] = f"{amendment_id_2}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id_2,
                                            data=data)
    payload = prepared_payload_findAmendmentIds()
    for param in params:
        del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = [
        f"{amendment_id_1}",
        f"{amendment_id_2}"
    ]

    assert all(item in expectedresult for item in actualresult['result'])


@pytestrail.case('C8618')
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_tender_in_params_relatesTo_and_two_ids_in_params_relatedItems(
        host, port,
        prepared_create_amendment,
        prepared_cpid, prepared_entity_id,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_findAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment
    data['relatedItem'] = f"{prepared_ev_ocid}"
    amendment_id_1 = prepared_entity_id()
    data['id'] = f"{amendment_id_1}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id_1,
                                            data=data)
    amendment_id_2 = prepared_entity_id()
    data['id'] = f"{amendment_id_2}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id_2,
                                            data=data)
    payload = prepared_payload_findAmendmentIds(relatesTo="tender")
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = [
        f"{amendment_id_1}"
    ]

    assert all(item in expectedresult for item in actualresult['result'])


@pytest.mark.parametrize("relatesTo,lotId,tenderId",
                         [
                             pytest.param("tender", uuid4(), uuid4(), marks=pytestrail.case('C8619')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_tender_in_params_relatesTo_and_lotId_in_params_relatedItems(
        host, port, relatesTo, lotId, tenderId,
        prepared_create_amendment,
        prepared_cpid,
        prepared_ev_ocid, response,
        prepared_payload_findAmendmentIds,
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
    payload = prepared_payload_findAmendmentIds(relatesTo=relatesTo, relatedItems=f"{lotId}")
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("relatesTo,lotId,tenderId",
                         [
                             pytest.param("lot", uuid4(), uuid4(), marks=pytestrail.case('C8620')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_lot_in_params_relatesTo_and_tender_id_in_params_relatedItems(
        host, port, relatesTo, lotId, tenderId,
        prepared_create_amendment,
        prepared_cpid,
        prepared_ev_ocid, response,
        prepared_payload_findAmendmentIds,
        execute_insert_into_revision_amendments,
):
    data = prepared_create_amendment()
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
    payload = prepared_payload_findAmendmentIds(relatesTo=relatesTo, relatedItems=f"{tenderId}")
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("relatesTo,lotId",
                         [
                             pytest.param("lot", uuid4(), marks=pytestrail.case('C8621')),
                         ])
def test_on_eRevisions_behavior_with_two_amendmets_for_one_tender_with_lot_in_params_relatesTo_and_tender_id_in_params_relatedItems(
        host, port, relatesTo, lotId,
        prepared_create_amendment,
        prepared_cpid, prepared_entity_id,
        prepared_ev_ocid, prepared_request_id,
        prepared_payload_findAmendmentIds,
        execute_insert_into_revision_amendments,
):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['relatedItem'] = f"{lotId}"
    data['id'] = f"{lotId}"
    data['relatesTo'] = 'tender'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=lotId,
                                            data=data)
    data['relatedItem'] = f"{lotId}"
    data['id'] = f"{amendment_id}"
    data['relatesTo'] = 'lot'
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id,
                                            data=data)
    payload = prepared_payload_findAmendmentIds(relatesTo=relatesTo, relatedItems=f"{lotId}")
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    expectedresult = [
        f"{lotId}",
        f"{amendment_id}"
    ]

    assert all(item in expectedresult for item in actualresult['result']), actualresult


@pytestrail.case('C16939')
@pytest.mark.parametrize('status', ('pending', 'active', 'cancelled'))
@pytest.mark.parametrize('relatesTo', ('lot', 'tender'))
def test_findAmendmentIds_by_param_status(host, port, status, response, relatesTo,
                                          execute_insert_into_revision_amendments,
                                          clear_revision_amendments_by_cpid,
                                          prepared_cpid,
                                          prepared_ev_ocid,
                                          prepared_create_amendment,
                                          prepared_entity_id,
                                          prepared_request_id,
                                          prepared_payload_findAmendmentIds):
    amendment_id = prepared_entity_id()
    prepared_create_amendment['id'] = str(amendment_id)
    prepared_create_amendment['status'] = status
    prepared_create_amendment['relatesTo'] = relatesTo
    prepared_create_amendment['relatedItem'] = prepared_ev_ocid
    execute_insert_into_revision_amendments(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        id=amendment_id,
        data=prepared_create_amendment
    )
    payload = prepared_payload_findAmendmentIds(
        relatesTo=relatesTo,
        status=status
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = [
        str(amendment_id)
    ]

    assert actualresult == response.success
