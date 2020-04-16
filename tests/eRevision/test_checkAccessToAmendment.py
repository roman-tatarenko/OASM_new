import json

from pytest_testrail.plugin import pytestrail
import requests


@pytestrail.case('C15031')
def test_checkAccessToAmendment_check_access_to_amendment_of_tender(host, port, execute_insert_into_revision_amendments,
                                                                    prepared_create_amendment, prepared_cpid,
                                                                    prepared_ev_ocid, prepared_entity_id,
                                                                    payload_checkAccessToAmendment,
                                                                    prepared_token_entity, prepared_owner,
                                                                    response):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = 'tender'
    data['relatedItem'] = prepared_ev_ocid
    data['token'] = str(prepared_token_entity)
    data['owner'] = prepared_owner
    execute_insert_into_revision_amendments(cpid=prepared_cpid, ocid=prepared_ev_ocid, id=amendment_id, data=data)
    payload = payload_checkAccessToAmendment(amendmentId=str(amendment_id), token=data['token'], owner=data['owner'])
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success, print(json.dumps(data))


@pytestrail.case('C15035')
def test_checkAccessToAmendment_check_access_to_amendment_of_second_lot(host, port,
                                                                        execute_insert_into_revision_amendments,
                                                                        prepared_create_amendment, prepared_cpid,
                                                                        prepared_ev_ocid, prepared_entity_id,
                                                                        payload_checkAccessToAmendment,
                                                                        prepared_token_entity, prepared_owner,
                                                                        response):
    cpid = prepared_cpid
    ocid = prepared_ev_ocid
    amendment_id = prepared_entity_id()
    lot_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = 'lot'
    data['relatedItem'] = str(lot_id)
    data['token'] = str(prepared_token_entity)
    data['owner'] = str(prepared_owner)
    execute_insert_into_revision_amendments(cpid=cpid, ocid=ocid, id=amendment_id, data=data)

    amendment_id_2 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()
    data_2 = prepared_create_amendment
    data_2['id'] = str(amendment_id_2)
    data_2['relatesTo'] = 'lot'
    data_2['relatedItem'] = str(lot_id_2)
    data_2['token'] = data['token']
    data_2['owner'] = data['owner']
    execute_insert_into_revision_amendments(cpid=cpid, ocid=ocid, id=amendment_id_2, data=data_2)

    payload = payload_checkAccessToAmendment(cpid=cpid, ocid=ocid, token=data_2['token'], owner=data_2['owner'],
                                             amendmentId=str(amendment_id_2))

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success, print(json.dumps(data))


@pytestrail.case('C15036')
def test_checkAccessToAmendment_use_invalid_cpid(host, port, prepared_cpid, prepared_ev_ocid, prepared_entity_id,
                                                 payload_checkAccessToAmendment, prepared_token_entity, prepared_owner,
                                                 response):
    amendment_id = prepared_entity_id()

    payload = payload_checkAccessToAmendment(cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                             token=str(prepared_token_entity),
                                             owner=prepared_owner, amendmentId=str(amendment_id))

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [
        {"code": "VR-10.2.4.3/21", "description": "Amendment not found.", "details": [{"id": str(amendment_id)}]}]

    assert actualresult == response.error


@pytestrail.case('C15040')
def test_checkAccessToAmendment_use_empty_string_value_for_params_cpid(host, port, prepared_cpid, prepared_ev_ocid,
                                                                       prepared_entity_id,
                                                                       payload_checkAccessToAmendment,
                                                                       prepared_token_entity, prepared_owner, response):
    amendment_id = prepared_entity_id()
    payload = payload_checkAccessToAmendment(cpid='', ocid=prepared_ev_ocid, token=str(prepared_token_entity),
                                             owner=prepared_owner, amendmentId=str(amendment_id))
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [{"code": "DR-5/21",
                                 "description": "Data mismatch of attribute 'cpid' to the pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: ''.",
                                 "details": [{"name": "cpid"}]}]

    assert actualresult == response.error


@pytestrail.case('C15041')
def test_checkAccessToAmendment_use_number_value_for_params_cpid(host, port, prepared_cpid, prepared_ev_ocid,
                                                                 prepared_entity_id,
                                                                 payload_checkAccessToAmendment,
                                                                 prepared_token_entity, prepared_owner, response):
    amendment_id = prepared_entity_id()
    payload = payload_checkAccessToAmendment(cpid=22.9, ocid=prepared_ev_ocid, token=str(prepared_token_entity),
                                             owner=prepared_owner, amendmentId=str(amendment_id))
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [{"code": "DR-5/21",
                                 "description": "Data mismatch of attribute 'cpid' to the pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: '22.9'.",
                                 "details": [{"name": "cpid"}]}]

    assert actualresult == response.error


@pytestrail.case('C15042')
def test_theckAccessToAmendment_use_boolean_value_for_params_cpid(host, port, prepared_cpid, prepared_ev_ocid,
                                                                  prepared_entity_id,
                                                                  payload_checkAccessToAmendment,
                                                                  prepared_token_entity, prepared_owner, response):
    amendment_id = prepared_entity_id()
    payload = payload_checkAccessToAmendment(cpid=True, ocid=prepared_ev_ocid, token=str(prepared_token_entity),
                                             owner=prepared_owner, amendmentId=str(amendment_id))
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [{"code": "DR-5/21",
                                 "description": "Data mismatch of attribute 'cpid' to the pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: 'true'.",
                                 "details": [{"name": "cpid"}]}]

    assert actualresult == response.error


@pytestrail.case('C15043')
def test_checkAccessToAmendment_mismatch_to_the_pattern_of_params_cpid_value(host, port,
                                                                             prepared_ev_ocid,
                                                                             prepared_entity_id,
                                                                             payload_checkAccessToAmendment,
                                                                             prepared_token_entity, prepared_owner,
                                                                             response):
    amendment_id = prepared_entity_id()
    payload = payload_checkAccessToAmendment(cpid='ocdst1s2t3MD-1589999909002', ocid=prepared_ev_ocid,
                                             token=str(prepared_token_entity),
                                             owner=prepared_owner, amendmentId=str(amendment_id))
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [{"code": "DR-5/21",
                                 "description": "Data mismatch of attribute 'cpid' to the pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. Actual value: 'ocdst1s2t3MD-1589999909002'.",
                                 "details": [{"name": "cpid"}]}]

    assert actualresult == response.error


@pytestrail.case('C15044')
def test_checkAccessToAmendment_use_invalid_ocid(host, port, execute_insert_into_revision_amendments,
                                                 prepared_create_amendment, prepared_cpid,
                                                 prepared_ev_ocid, prepared_entity_id,
                                                 payload_checkAccessToAmendment,
                                                 prepared_token_entity, prepared_owner,
                                                 response):
    cpid = prepared_cpid
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = 'tender'
    data['relatedItem'] = prepared_ev_ocid
    data['token'] = str(prepared_token_entity)
    data['owner'] = prepared_owner
    execute_insert_into_revision_amendments(cpid=cpid, ocid=prepared_ev_ocid, id=amendment_id, data=data)
    payload = payload_checkAccessToAmendment(cpid=cpid, ocid='ocds-t1s2t3-MD-9999999909999-EV-9999999909999',
                                             amendmentId=str(amendment_id),
                                             token=data['token'], owner=data['owner'])

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    response.error['result'] = [
        {"code": "VR-10.2.4.3/21", "description": "Amendment not found.", "details": [{"id": str(amendment_id)}]}]

    assert actualresult == response.error
