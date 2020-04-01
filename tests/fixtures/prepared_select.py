import pytest


@pytest.fixture(scope='session')
def prepared_select_revision_amendments_by_id(cassandra_session):
    cassandra_session.set_keyspace('revision')
    query = 'SELECT * FROM amendments WHERE cpid=? AND ocid=? AND id=?'
    prepared = cassandra_session.prepare(query)
    return prepared
