import pytest


@pytest.fixture(scope='function')
def clear_dossier_tenders_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM tenders"
                              f" where cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_contracting_can_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM contracting_can"
                              f" where cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_evaluation_award_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM evaluation_award"
                              f" where cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_access_tender_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM access_tender"
                              f" WHERE cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_submission_bid_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM submission_bid"
                              f" WHERE cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_notice_compiled_release_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('ocds')
    cassandra_session.execute(f"DELETE FROM notice_compiled_release"
                              f" WHERE cp_id='{prepared_cpid}';")


@pytest.fixture(scope='function')
def clear_revision_amendments_by_cpid(cassandra_session, prepared_cpid):
    yield
    cassandra_session.set_keyspace('revision')
    cassandra_session.execute(f"DELETE FROM amendments"
                              f" WHERE cpid='{prepared_cpid}';")
