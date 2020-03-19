import json
from dataclasses import dataclass

import pytest
from cassandra.query import UNSET_VALUE

pytest_plugins = [
    "tests.fixtures.prepared_id",
    "tests.fixtures.prepared_data",
    "tests.fixtures.prepared_kafka"
]


@pytest.fixture(scope='session')
def cassandra_session(cluster):
    session = cluster.connect()
    yield session
    session.shutdown()


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


@pytest.fixture(scope='session')
def port():
    @dataclass
    class Port:
        """Ports of Docker containers"""
        eQualification: int = 9251
        eEvaluation: int = 9081
        eMDM: int = 9161
        eContracting: int = 9151
        eAccess: int = 9031
        eSubmission: int = 9061
        eRevision: int = 9351

    return Port


@pytest.fixture(scope='function')
def responses(prepared_request_id):
    @dataclass()
    class Responses:
        version = '0.0.1'
        ok = {'id': f'{prepared_request_id}', 'data': {}, 'version': version}
        errors = {'id': f'{prepared_request_id}', 'errors': [], 'version': version}

    return Responses


@pytest.fixture(scope='function')
def payload_template(prepared_request_id):
    return {
        "id": "",
        "command": "",
        "context": {},
        "data": {},
        "version": "0.0.1"
    }


@pytest.fixture(scope='function')
def prepared_payload(payload_template, prepared_request_id, prepared_operation_id):
    def with_values(command, cpid=None, stage="EV", operationid=prepared_operation_id, id=None, token=None,
                    owner='445f6851-c908-407d-9b45-14b92f3e964b'):
        payload_template['id'] = f"{prepared_request_id}"
        payload_template['command'] = command
        payload_template['context'] = {
            "operationId": f"{operationid}",
            "requestId": "7eb32550-2335-11ea-7a78-e9a0e1c3d51d",
            "cpid": cpid,
            "ocid": "ocds-t1s2t3-MD-1576850865434-EV-1576850873109",
            "stage": stage,
            "prevStage": "EV",
            "processType": "startConsiderByAward",
            "operationType": "doAwardConsideration",
            "phase": "awarding",
            "owner": f"{owner}",
            "country": "MD",
            "language": "ro",
            "pmd": "TEST_OT",
            "token": f'{token}',
            "startDate": "2019-12-20T14:32:05Z",
            "id": f"{id}",
            "timeStamp": 1576852325413,
            "isAuction": False
        }
        return payload_template

    return with_values


@pytest.fixture(scope='function')
def prepared_payload_getAmendmentIds(prepared_request_id, prepared_cpid, prepared_ev_ocid):
    def with_values(version="2.0.0", id=f"{prepared_request_id}", action="getAmendmentIds",
                    relatesTo="tender", status="pending", type="cancellation"):
        return {
            "version": version,
            "id": id,
            "action": action,
            "params": {
                "status": status,
                "type": type,
                "relatesTo": relatesTo,
                "relatedItems": [f"{prepared_ev_ocid}"],
                "cpid": f"{prepared_cpid}",
                "ocid": f"{prepared_ev_ocid}"
            }
        }

    return with_values
