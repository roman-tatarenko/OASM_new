from datetime import datetime

import pytest
import requests
from pytest_testrail.plugin import pytestrail

from utils.ocds_date import ocds_datetime, ocds_date_to_datetime


@pytestrail.case('C13253')
def test_closeAwardPeriod_with_valid_params_and_awardPeriod_in_db(port, host, payload_closeAwardPeriod,
                                                                  execute_insert_into_evaluation_period,
                                                                  execute_select_evaluation_period_by_cpid,
                                                                  prepared_cpid, response):
    cp_id = prepared_cpid
    end_date = ocds_datetime()
    execute_insert_into_evaluation_period(
        cp_id=cp_id,
        stage='EV',
        start_date=datetime.now()
    )
    payload = payload_closeAwardPeriod(
        cpid=prepared_cpid,
        endDate=end_date
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.success['result'] = {
        'awardPeriod': {
            'endDate': end_date
        }
    }
    assert actualresult == response.success

    record = execute_select_evaluation_period(
        cp_id=prepared_cpid
    ).one()

    assert record.end_date == ocds_date_to_datetime(end_date)


@pytestrail.case('C16926')
def test_closeAwardPeriod_without_awardPeriod_in_db(port, host, payload_closeAwardPeriod,
                                                    execute_insert_into_evaluation_period,
                                                    prepared_cpid, response):
    end_date = ocds_datetime()
    execute_insert_into_evaluation_period(
        cp_id=prepared_cpid,
        stage='EV'
    )
    payload = payload_closeAwardPeriod(
        cpid=prepared_cpid,
        endDate=end_date
    )
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()
    response.error['result'] = [
        {
            'code': 'VR-10.4.6.1/7',
            'description': 'Period not found.'
        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param('cpid', marks=pytestrail.case('C16927')),
                             pytest.param('ocid', marks=pytestrail.case('C16928')),
                             pytest.param('endDate', marks=pytestrail.case('C16929'))
                         ])
def test_closeAwardPeriod_request_does_not_contain_param(port, host, param, payload_closeAwardPeriod,
                                                         response):
    payload = payload_closeAwardPeriod()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eEvaluation}/command2', json=payload).json()

    response.error['result'] = [{'code': 'RQ-1/7',
                                 'description': "Error parsing 'params'"}]

    assert actualresult == response.error
