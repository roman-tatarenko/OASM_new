import json

import pytest
from cassandra.query import UNSET_VALUE


@pytest.fixture(scope='function')
def execute_insert_into_revision_amendments(prepared_insert_revision_amendments, cassandra_session):
    def with_values(cpid, ocid, id, data):
        values = (
            f'{cpid}', f'{ocid}', id, f'{json.dumps(data)}'
        )
        cassandra_session.execute(prepared_insert_revision_amendments, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_notice_compiled_release(prepared_insert_notice_compiled_release, cassandra_session):
    def with_values(cp_id, oc_id, json_data, publish_date, release_date, release_id, stage, status):
        values = (
            f'{cp_id}', f'{oc_id}', f'{json.dumps(json_data)}', publish_date, release_date,
            f'{release_id}', stage, status
        )
        cassandra_session.execute(prepared_insert_notice_compiled_release, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_submission_bid(prepared_insert_submission_bid, cassandra_session):
    def with_values(cp_id, stage, bid_id, created_date, json_data, owner, pending_date, status, token_entity):
        values = (
            f'{cp_id}', stage, bid_id, created_date, f'{json.dumps(json_data)}',
            owner, pending_date, status, token_entity
        )
        cassandra_session.execute(prepared_insert_submission_bid, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_contracting_can(prepared_insert_contracting_can, cassandra_session):
    def with_values(cp_id, can_id, award_id, created_date, json_data, lot_id, owner, status, status_details,
                    token_entity, ac_id=UNSET_VALUE):
        values = (
            f'{cp_id}', can_id, ac_id, f'{award_id}', created_date, f'{json.dumps(json_data)}',
            f'{lot_id}', owner, status, status_details, token_entity
        )
        cassandra_session.execute(prepared_insert_contracting_can, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_dossier_tenders(prepared_insert_dossier_tenders, cassandra_session):
    def with_values(cp_id, json_data, owner):
        values = (
            f'{cp_id}', f'{json.dumps(json_data)}', owner
        )
        cassandra_session.execute(prepared_insert_dossier_tenders, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_evaluation_award(prepared_insert_evaluation_award, cassandra_session):
    def with_values(cp_id, stage, token_entity, json_data, owner, status, status_details):
        values = (
            f'{cp_id}', stage, token_entity, f'{json.dumps(json_data)}',
            owner, status, status_details
        )
        cassandra_session.execute(prepared_insert_evaluation_award, values)

    return with_values


@pytest.fixture(scope='function')
def execute_insert_into_access_tender(prepared_insert_access_tender, cassandra_session):
    def with_values(cp_id, stage, token_entity, created_date, json_data, owner):
        values = (
            f'{cp_id}', stage, token_entity, created_date, f'{json.dumps(json_data)}',
            owner
        )
        cassandra_session.execute(prepared_insert_access_tender, values)

    return with_values
