import uuid

import pytest
import requests
from pytest_testrail.plugin import pytestrail

from resources.domain.amendment import schema_amendment


@pytestrail.case('C17059')
def test_getAmendmentByIds_get_one_amendment(port, host,
                                             execute_insert_into_revision_amendments,
                                             prepare_data, prepared_entity_id,
                                             prepared_cpid, prepared_ev_ocid,
                                             payload_getAmendmentByIds, response,
                                             clear_revision_amendments_by_cpid):
    amendment_id = str(prepared_entity_id())
    data = prepare_data(schema=schema_amendment)
    data['id'] = amendment_id
    execute_insert_into_revision_amendments(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        id=uuid.UUID(amendment_id),
        data=data
    )
    payload = payload_getAmendmentByIds(amendment_id)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    del data['token']
    del data['owner']

    assert actualresult['result'] == [data]


@pytestrail.case('C17061')
def test_getAmendmentByIds_get_many_amendments(port, host,
                                               prepare_data, prepared_entity_id,
                                               prepared_cpid, prepared_ev_ocid,
                                               payload_getAmendmentByIds, response,
                                               execute_insert_into_revision_amendments,
                                               clear_revision_amendments_by_cpid):
    amendment_ids = [str(prepared_entity_id()) for _ in range(1, 10)]
    data = prepare_data(schema=schema_amendment)
    for amendment_id in amendment_ids:
        data['id'] = amendment_id
        execute_insert_into_revision_amendments(
            cpid=prepared_cpid,
            ocid=prepared_ev_ocid,
            id=uuid.UUID(amendment_id),
            data=data
        )
    payload = payload_getAmendmentByIds(*amendment_ids)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    del data['token']
    del data['owner']

    for amendment_id in amendment_ids:
        data['id'] = amendment_id
        assert data in actualresult['result']


@pytestrail.case('C17067')
def test_setStateForAmendment_amendment_not_found_by_cpid(port, host,
                                                          payload_getAmendmentByIds,
                                                          prepared_entity_id, response):
    amendment_id = str(prepared_entity_id())
    payload = payload_getAmendmentByIds(amendment_id)
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'VR-10.2.5.1/21',
            'description': 'Amendment not found.',
            'details': [{'id': str(amendment_id)}]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C17065')
@pytest.mark.parametrize('amendment_id', ("", 1))
def test_setStateForAmendment_data_format_mismatch_of_attribute_amendment_id(port, host, amendment_id,
                                                                             payload_getAmendmentByIds,
                                                                             response):
    payload = payload_getAmendmentByIds(
        amendment_id
    )
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'DR-4/21',
            'description': "Data format mismatch of attribute 'amendmentIds'."
                           " Expected data format: 'uuid',"
                           f" actual value: '{amendment_id}'.",
            'details': [{'name': 'amendmentIds'}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C17062')),
                             pytest.param("ocid",
                                          marks=pytestrail.case('C17063')),
                             pytest.param("amendmentIds",
                                          marks=pytestrail.case('C17064'))
                         ])
def test_getAmendmentByIds_without_required_param(port, host, param,
                                                  payload_getAmendmentByIds,
                                                  response):
    payload = payload_getAmendmentByIds()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C17068')
def test_setStateForAmendment_with_empty_array_amendmentIds(port, host,
                                                            payload_getAmendmentByIds,
                                                            response):
    payload = payload_getAmendmentByIds()
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            'code': 'DR-10/21',
            'description': "Attribute 'amendmentIds' is an empty array.",
            'details': [{'name': 'amendmentIds'}]
        }
    ]

    assert actualresult == response.error
