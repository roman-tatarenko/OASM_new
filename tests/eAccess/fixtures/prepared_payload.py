import pytest


@pytest.fixture(scope='function')
def payload_getLotStateByIds(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='getLotStateByIds')

    def _payload_getLotStateByIds(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "lotIds": list(args),
            "cpid": cpid,
            "ocid": ocid
        }
        return payload

    return _payload_getLotStateByIds


@pytest.fixture(scope='function')
def payload_findLotIds(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='findLotIds')

    def _payload_findLotIds(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "states": list(args),
            "cpid": cpid,
            "ocid": ocid
        }
        return payload

    return _payload_findLotIds


@pytest.fixture(scope='function')
def payload_checkAccessToTender(request_template, prepared_cpid, prepared_ev_ocid, prepared_owner,
                                prepared_token_entity):
    payload = request_template(action='checkAccessToTender')

    def _payload_checkAccessToTender(cpid=prepared_cpid, ocid=prepared_ev_ocid, token=str(prepared_token_entity),
                                     owner=prepared_owner):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "token": token,
            "owner": owner
        }
        return payload

    return _payload_checkAccessToTender


@pytest.fixture(scope='function')
def payload_checkPersonesStructure(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='checkPersonesStructure')

    def _payload_checkPersonesStructure(*args, locationOfPersones, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "persones": list(args),
            "cpid": cpid,
            "ocid": ocid,
            "locationOfPersones": locationOfPersones
        }
        return payload

    return _payload_checkPersonesStructure


@pytest.fixture(scope='function')
def payload_getTenderState(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='getTenderState')

    def _payload_getTenderState(cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid
        }
        return payload

    return _payload_getTenderState
