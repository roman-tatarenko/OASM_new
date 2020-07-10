from uuid import uuid4

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


@pytest.fixture(scope='function')
def payload_responderProcessing(request_template, prepared_cpid, prepared_ev_ocid, prepare_data):
    payload = request_template(action='responderProcessing')

    def _payload_responderProcessing(cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                     responder=None, date=None):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "responder": responder,
            "date": date
        }
        return payload

    return _payload_responderProcessing


@pytest.fixture(scope='function')
def payload_getOrganization(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='getOrganization')

    def _payload_getOrganization(cpid=prepared_cpid, ocid=prepared_ev_ocid, role=None):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "role": role,
        }
        return payload

    return _payload_getOrganization


@pytest.fixture(scope='function')
def payload_setStateForLots(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='setStateForLots')

    def _payload_setStateForLots(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "lots": list(args)

        }
        return payload

    return _payload_setStateForLots


