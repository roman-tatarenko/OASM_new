import pytest


@pytest.fixture(scope='function')
def prepared_payload_getLotStateByIds(prepared_request_id, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
                                      prepared_owner):
    def _prepared_payload_getLotStateByIds(lot_id=prepared_token_entity):
        return {
            "version": "2.0.0",
            "id": f"{prepared_request_id}",
            "action": "getLotStateByIds",
            "params": {
                "lotIds": [
                    f"{lot_id}"
                ],
                "cpid": f"{prepared_cpid}",
                "ocid": f"{prepared_ev_ocid}"
            }
        }

    return _prepared_payload_getLotStateByIds


@pytest.fixture(scope='function')
def prepared_payload_findLotIds(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(acton='findLotIds')

    def _prepared_payload_findLotIds(*states, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "states": list(states),
            "cpid": cpid,
            "ocid": ocid
        }
        return payload

    return _prepared_payload_findLotIds


@pytest.fixture(scope='function')
def prepared_payload_checkAccessToTender(prepared_request_id, prepared_cpid, prepared_ev_ocid, prepared_token_entity,
                                         prepared_owner):
    return {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "action": "checkAccessToTender",
        "params": {
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ev_ocid}",
            "token": f"{prepared_token_entity}",
            "owner": f"{prepared_owner}"
        }
    }


@pytest.fixture(scope='function')
def payload_checkPersonesStructure(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(acton='checkPersonesStructure')

    def _payload_checkPersonesStructure(persones, locationOfPersones, cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                        ):
        payload['params'] = {
            "persones": persones,
            "cpid": cpid,
            "ocid": ocid,
            "locationOfPersones": locationOfPersones
        }
        return payload

    return _payload_checkPersonesStructure
