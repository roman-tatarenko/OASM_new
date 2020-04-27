import pytest


@pytest.fixture(scope='function')
def execute_select_revision_amendments_by_id(prepared_select_revision_amendments_by_id, cassandra_session):
    def with_values(cpid, ocid, id):
        return cassandra_session.execute(prepared_select_revision_amendments_by_id, [cpid, ocid, id])

    return with_values


@pytest.fixture(scope='function')
def execute_select_notice_compiled_release(prepared_select_notice_compiled_release, cassandra_session):
    def with_values(cpid, ocid):
        return cassandra_session.execute(prepared_select_notice_compiled_release, [cpid, ocid])

    return with_values


@pytest.fixture(scope='function')
def execute_select_evaluation_award_by_token_entity(prepared_select_evaluation_award_by_token_entity,
                                                    cassandra_session):
    def with_values(cp_id, stage, token_entity):
        return cassandra_session.execute(prepared_select_evaluation_award_by_token_entity, [cp_id, stage, token_entity])

    return with_values
