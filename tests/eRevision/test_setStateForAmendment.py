import json

import pytest
import requests
from pytest_testrail.plugin import pytestrail

from resources.domain.amendment import schema_amendment


@pytest.mark.parametrize("status",
                         [
                             pytest.param("active",
                                          marks=pytestrail.case('C16968')),
                             pytest.param("cancelled",
                                          marks=pytestrail.case('C16969')),
                         ])
def test_setStateForAmendment_valid_status(port, host, status,
                                           prepared_cpid, prepared_ev_ocid, prepare_data,
                                           execute_insert_into_revision_amendments,
                                           execute_select_revision_amendments_by_id,
                                           prepared_entity_id,
                                           payload_setStateForAmendment, response):
    amendment_id = prepared_entity_id()
    data = prepare_data(schema=schema_amendment)
    data['id'] = str(amendment_id)
    execute_insert_into_revision_amendments(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        id=amendment_id,
        data=data
    )
    payload = payload_setStateForAmendment(
        amendmentId=amendment_id,
        status=status
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.success['result'] = {
        'id': str(amendment_id),
        "status": status
    }

    assert actualresult == response.success

    record = execute_select_revision_amendments_by_id(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        id=amendment_id
    ).one()

    json_data = json.loads(record.data)

    assert json_data['status'] == status


@pytestrail.case('C16977')
@pytest.mark.parametrize('amendment_id', ("", 1))
def test_setStateForAmendment_data_format_mismatch_of_attribute_amendment_id(port, host, amendment_id,
                                                                             payload_setStateForAmendment,
                                                                             response):
    payload = payload_setStateForAmendment(
        amendmentId=amendment_id,
        status='active'
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'DR-4/21',
            'description': "Data format mismatch of attribute 'amendment.id'."
                           " Expected data format: 'uuid',"
                           f" actual value: '{amendment_id}'.",
            'details': [{'name': 'amendment.id'}]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C16976')
@pytest.mark.parametrize('status', ("", 1))
def test_setStateForAmendment_mismatch_status_with_one_of_enum_expected_values(port, host, status,
                                                                               prepared_entity_id,
                                                                               payload_setStateForAmendment,
                                                                               response):
    amendment_id = prepared_entity_id()
    payload = payload_setStateForAmendment(
        amendmentId=amendment_id,
        status=status
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'DR-3/21',
            'description': "Attribute value mismatch of 'amendment.status'"
                           " with one of enum expected values."
                           " Expected values: 'active, cancelled',"
                           f" actual value: '{status}'.",
            'details': [{'name': 'amendment.status'}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C16971')),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C16972')),
                             pytest.param("amendment",
                                          marks=pytestrail.case('C16973'))
                         ])
def test_setStateForAmendment_without_required_param_in_params(port, host, param,
                                                               payload_setStateForAmendment,
                                                               response):
    payload = payload_setStateForAmendment()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("attribute",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case('C16974')),
                             pytest.param("status",
                                          marks=pytestrail.case('C16975'))
                         ])
def test_setStateForAmendment_without_required_attribute_in_amendment(port, host, attribute,
                                                                      payload_setStateForAmendment,
                                                                      response):
    payload = payload_setStateForAmendment()
    del payload['params']['amendment'][attribute]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytest.mark.xfail(reason='invalid code VR-VR-10.2.6.1/21')
@pytestrail.case('C16993')
def test_setStateForAmendment_amendment_not_found_by_cpid(port, host,
                                                          payload_setStateForAmendment,
                                                          prepared_entity_id, response):
    amendment_id = prepared_entity_id()
    payload = payload_setStateForAmendment(
        amendmentId=amendment_id,
        status='active'
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'VR-10.2.6.1/21',
            'description': 'Amendment not found.',
            'details': [{'id': str(amendment_id)}]
        }
    ]

    assert actualresult == response.error
