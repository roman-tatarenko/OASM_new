import json
import uuid
from datetime import datetime
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case("C16416")
def test_createUnsuccessfulAwards_create_unsuccessful_award_for_one_lot(port, host, payload_createUnsuccessfulAwards,
                                                                        prepared_entity_id, prepared_cpid,
                                                                        execute_select_evaluation_award_by_cpid):
    lot_id = str(prepared_entity_id())
    date = (datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%SZ')
    payload = payload_createUnsuccessfulAwards(
        lot_id,
        date=date
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    unsuccessful_award = actualresult['result'][0]

    assert actualresult['status'] == 'success'
    assert uuid.UUID(actualresult['result'][0]['id'])
    assert unsuccessful_award['date'] == date
    assert unsuccessful_award['title'] == "Lot is not awarded"
    assert unsuccessful_award['description'] == "Other reasons (discontinuation of procedure)"
    assert unsuccessful_award['status'] == "unsuccessful"
    assert unsuccessful_award['statusDetails'] == "lotCancelled"
    assert unsuccessful_award['relatedLots'][0] == lot_id

    record = execute_select_evaluation_award_by_cpid(
        cp_id=prepared_cpid
    ).one()

    assert record.stage == 'EV'
    assert record.status == "unsuccessful"
    assert record.status_details == "lotCancelled"

    json_data = json.loads(record.json_data)

    assert uuid.UUID(json_data['id'])
    assert json_data['date'] == date
    assert json_data['title'] == "Lot is not awarded"
    assert json_data['description'] == "Other reasons (discontinuation of procedure)"
    assert json_data['status'] == "unsuccessful"
    assert json_data['statusDetails'] == "lotCancelled"
    assert json_data['relatedLots'][0] == lot_id


@pytestrail.case("C16417")
def test_createUnsuccessfulAwards_create_unsuccessful_award_for_more_then_one_lot(port, host,
                                                                                  payload_createUnsuccessfulAwards,
                                                                                  prepared_entity_id
                                                                                  ):
    lot_ids = [str(uuid4()) for _ in range(100)]
    date = (datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%SZ')
    payload = payload_createUnsuccessfulAwards(
        *lot_ids,
        date=date
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    unsuccessful_awards = actualresult['result']

    assert actualresult['status'] == 'success'

    for i in range(len(lot_ids)):
        assert uuid.UUID(actualresult['result'][i]['id'])
        assert unsuccessful_awards[i]['date'] == date
        assert unsuccessful_awards[i]['title'] == "Lot is not awarded"
        assert unsuccessful_awards[i]['description'] == "Other reasons (discontinuation of procedure)"
        assert unsuccessful_awards[i]['status'] == "unsuccessful"
        assert unsuccessful_awards[i]['statusDetails'] == "lotCancelled"
        assert unsuccessful_awards[i]['relatedLots'][0] == lot_ids[i]


@pytestrail.case("C16415")
def test_createUnsuccessfulAwards_param_lotIds_as_empty_array(port, host, payload_createUnsuccessfulAwards, response):
    payload = payload_createUnsuccessfulAwards()
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    response.error['result'] = [{'code': 'DR-10/7',
                                 'description': "Attribute 'lotIds' is an empty array.",
                                 'details': [{'name': 'lotIds'}]}]

    assert actualresult == response.error


@pytestrail.case("C16414")
def test_createUnsuccessfulAwards_data_format_mismatch_of_attribute_lotId(port, host, payload_createUnsuccessfulAwards,
                                                                          response):
    lot_id = ""
    payload = payload_createUnsuccessfulAwards(
        lot_id
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    response.error['result'] = [{'code': 'DR-4/7',
                                 'description': "Data format mismatch of attribute 'lotIds'."
                                                " Expected data format: 'uuid', actual value: ''.",
                                 'details': [{'name': 'lotIds'}]}]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param('cpid', marks=pytestrail.case('C16896')),
                             pytest.param('ocid', marks=pytestrail.case('C16897')),
                             pytest.param('lotIds', marks=pytestrail.case('C16898')),
                             pytest.param('date', marks=pytestrail.case('C16899')),
                             pytest.param('owner', marks=pytestrail.case('C16900'))
                         ])
def test_createUnsuccessfulAwards_request_does_not_contain_param(port, host, param, payload_createUnsuccessfulAwards,
                                                                 response):
    payload = payload_createUnsuccessfulAwards()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    response.error['result'] = [{'code': 'RQ-1/7',
                                 'description': "Error parsing 'params'"}]

    assert actualresult == response.error
