import pytest


@pytest.fixture(scope='session')
def prepared_insert_evaluation_award(cassandra_session):
    cassandra_session.set_keyspace('ocds')
    query = 'INSERT INTO evaluation_award (cp_id,stage,token_entity,json_data,owner,status,status_details) ' \
            'VALUES (?,?,?,?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_access_tender(cassandra_session):
    cassandra_session.set_keyspace('ocds')
    query = 'INSERT INTO access_tender (cp_id,stage,token_entity,created_date,json_data,owner) ' \
            'VALUES (?,?,?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_dossier_tenders(cassandra_session):
    cassandra_session.set_keyspace('dossier')
    query = 'INSERT INTO tenders (cp_id,json_data,owner) ' \
            'VALUES (?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_contracting_can(cassandra_session):
    cassandra_session.set_keyspace('ocds')
    query = 'INSERT INTO contracting_can (cp_id,can_id,ac_id,award_id,created_date,json_data,lot_id,owner,status,' \
            'status_details,token_entity) ' \
            'VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_submission_bid(cassandra_session):
    cassandra_session.set_keyspace('ocds')
    query = 'INSERT INTO submission_bid (cp_id,stage,bid_id,created_date,json_data,' \
            'owner,pending_date,status,token_entity) VALUES (?,?,?,?,?,?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_notice_compiled_release(cassandra_session):
    cassandra_session.set_keyspace('ocds')
    query = 'INSERT INTO notice_compiled_release (cp_id,oc_id,json_data,publish_date,' \
            'release_date,release_id,stage,status) VALUES (?,?,?,?,?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared


@pytest.fixture(scope='session')
def prepared_insert_revision_amendments(cassandra_session):
    cassandra_session.set_keyspace('revision')
    query = 'INSERT INTO amendments (cpid,ocid,id,data) VALUES (?,?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared



@pytest.fixture(scope='session')
def prepared_insert_dossier_tenders(cassandra_session):
    cassandra_session.set_keyspace('dossier')
    query = 'INSERT INTO tenders (cp_id, json_data, owner) VALUES (?,?,?)'
    prepared = cassandra_session.prepare(query)
    return prepared
