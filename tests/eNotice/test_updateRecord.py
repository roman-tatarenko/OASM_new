import json
from datetime import datetime

import pytest
import pytest_check as check
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C8226')
def test_on_possibility_to_update_record_with_a_valid_data_all_attributes_if_amendment_from_request_relates_to_tender(
        host, port, execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
        prepared_release_id, payload_notice_compiled_release, execute_select_notice_compiled_release,
        prepared_data_add_EV_before_SendAcForVerification, response):
    data = prepared_data_add_EV_before_SendAcForVerification

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid, json_data=data,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_release_id, stage='EV', status='active')

    payload = payload_notice_compiled_release()
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    result = execute_select_notice_compiled_release(cpid=prepared_cpid, ocid=prepared_ev_ocid).one()

    amendment_db = json.loads(result.json_data)['tender']['amendments'][0]
    amendment_request = json.loads(payload['params']['data'])['tender']['amendments'][0]
    del amendment_request['token']

    check.equal(amendment_request, amendment_db)
    check.equal(actualresult, response.success)


@pytestrail.case('C8375')
def test_on_possibility_to_update_record_with_a_valid_data_all_attributes_if_amendment_from_request_relates_to_lot(
        host, port, execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
        prepared_release_id, payload_notice_compiled_release, execute_select_notice_compiled_release,
        data_for_test_notice_compiled_release,
        prepared_data_add_EV_before_SendAcForVerification, response):
    data = prepared_data_add_EV_before_SendAcForVerification

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid, json_data=data,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_release_id, stage='EV', status='active')

    json_data = data_for_test_notice_compiled_release
    json_data['tender']['amendments'][0]['relatesTo'] = 'lot'

    payload = payload_notice_compiled_release(data=json_data)
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    result = execute_select_notice_compiled_release(cpid=prepared_cpid, ocid=prepared_ev_ocid).one()

    amendment_db = json.loads(result.json_data)['tender']['amendments'][0]
    amendment_request = json.loads(payload['params']['data'])['tender']['amendments'][0]
    del amendment_request['token']

    check.equal(amendment_request, amendment_db)
    check.equal(actualresult, response.success)


@pytest.mark.parametrize("param",
                         [

                             pytest.param("description",
                                          marks=pytestrail.case('C8256')),
                             pytest.param("documents",
                                          marks=pytestrail.case('C8257'))

                         ])
def test_on_a_possibility_to_update_record_without_params_tender_amendments_description(
        host, port, execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
        prepared_release_id, payload_notice_compiled_release, execute_select_notice_compiled_release,
        data_for_test_notice_compiled_release, param,
        prepared_data_add_EV_before_SendAcForVerification, response):
    data = prepared_data_add_EV_before_SendAcForVerification

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid, json_data=data,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_release_id, stage='EV', status='active')

    json_data = data_for_test_notice_compiled_release
    del json_data['tender']['amendments'][0][param]

    payload = payload_notice_compiled_release(data=json_data)
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    result = execute_select_notice_compiled_release(cpid=prepared_cpid, ocid=prepared_ev_ocid).one()

    amendment_db = json.loads(result.json_data)['tender']['amendments'][0]
    amendment_request = json.loads(payload['params']['data'])['tender']['amendments'][0]
    del amendment_request['token']

    check.equal(amendment_request, amendment_db)
    check.equal(actualresult, response.success)


@pytestrail.case('C8258')
def test_on_possibility_to_update_record_without_params_tender_amendments_documents_description(
        host, port, execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
        prepared_release_id, payload_notice_compiled_release, execute_select_notice_compiled_release,
        data_for_test_notice_compiled_release,
        prepared_data_add_EV_before_SendAcForVerification, response):
    data = prepared_data_add_EV_before_SendAcForVerification

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid, json_data=data,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_release_id, stage='EV', status='active')

    json_data = data_for_test_notice_compiled_release
    del json_data['tender']['amendments'][0]['documents'][0]['description']

    payload = payload_notice_compiled_release(data=json_data)
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    result = execute_select_notice_compiled_release(cpid=prepared_cpid, ocid=prepared_ev_ocid).one()

    amendment_db = json.loads(result.json_data)['tender']['amendments'][0]
    amendment_request = json.loads(payload['params']['data'])['tender']['amendments'][0]
    del amendment_request['token']

    check.equal(amendment_request, amendment_db)
    check.equal(actualresult, response.success)


@pytestrail.case('C8314')
def test_eNotice_adds_amendment_object_after_release_updating_if_release_already_has_an_array_of_amendments(
        host, port, execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
        prepared_release_id, payload_notice_compiled_release, execute_select_notice_compiled_release,
        data_for_test_notice_compiled_release,
        data_ev_with_amendment, response):
    data = data_ev_with_amendment

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid, json_data=data,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_release_id, stage='EV', status='active')

    payload = payload_notice_compiled_release()
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    result = execute_select_notice_compiled_release(cpid=prepared_cpid, ocid=prepared_ev_ocid).one()
    amendment_db = json.loads(result.json_data)['tender']['amendments']
    amendment_request = json.loads(payload['params']['data'])['tender']['amendments'][0]
    del amendment_request['token']
    amendment_data = data['tender']['amendments'][0]
    check.equal(actualresult, response.success)

    assert all(item in amendment_db for item in [amendment_request, amendment_data])


@pytest.mark.parametrize("param",
                         [
                             pytest.param("tender", marks=pytestrail.case('C8260')),
                             pytest.param("ocid", marks=pytestrail.case('C8261')),
                             pytest.param("cpid", marks=pytestrail.case('C8262'))
                         ])
def test_on_there_is_response_with_status_error_if_request_does_not_contain(
        host, port, param, payload_notice_compiled_release,
        data_for_test_notice_compiled_release, response):
    del data_for_test_notice_compiled_release[param]

    payload = payload_notice_compiled_release(data=data_for_test_notice_compiled_release)
    actualresult = requests.post(f'{host}:{port.eNotice}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/2",
            "description": "Can not parse 'data'."
        }
    ]

    assert actualresult == response.error
