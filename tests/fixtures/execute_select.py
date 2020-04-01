import pytest


@pytest.fixture(scope='function')
def execute_select_revision_amendments_by_id(prepared_select_revision_amendments_by_id, cassandra_session):
    def with_values(cpid, ocid, id):
        return cassandra_session.execute(prepared_select_revision_amendments_by_id, [cpid, ocid, id])

    return with_values
