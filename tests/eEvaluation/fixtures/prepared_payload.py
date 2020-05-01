import pytest


@pytest.fixture(scope='function')
def payload_checkRelatedTenderer(request_template, prepared_cpid, prepared_ev_ocid, prepared_entity_id,
                                 prepared_tenderer_id):
    payload = request_template(action='checkRelatedTenderer')

    def _payload_checkRelatedTenderer(awardId=str(prepared_entity_id()), requirementId=str(prepared_entity_id()),
                                      relatedTendererId=prepared_tenderer_id(), cpid=prepared_cpid,
                                      ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "awardId": awardId,
            "requirementId": requirementId,
            "relatedTendererId": relatedTendererId
        }
        return payload

    return _payload_checkRelatedTenderer


@pytest.fixture(scope='function')
def payload_addRequirementResponse(request_template, prepared_cpid, prepared_ev_ocid, prepared_entity_id):
    payload = request_template(action='addRequirementResponse')

    def _payload_addRequirementResponse(award_id, requirementResponse_id, relatedTenderer_id, requirement_id,
                                        cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "award": {
                "id": str(award_id),
                "requirementResponse": {
                    "id": str(requirementResponse_id),
                    "value": "true",
                    "relatedTenderer": {
                        "id": str(relatedTenderer_id)
                    },
                    "requirement": {
                        "id": str(requirement_id)

                    },
                    "responder": {
                        "name": "responderName",
                        "identifier": {
                            "id": "string",
                            "scheme": ""
                        }
                    }
                }
            }
        }
        return payload

    return _payload_addRequirementResponse


@pytest.fixture(scope='function')
def payload_getAwardStateByIds(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='getAwardStateByIds')

    def _payload_getAwardStateByIds(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "awardIds": list(args),

        }
        return payload

    return _payload_getAwardStateByIds


@pytest.fixture(scope='function')
def payload_checkAccessToAward(request_template, prepared_cpid, prepared_ev_ocid, prepared_owner,
                               prepared_token_entity):
    payload = request_template(action='checkAccessToAward')

    def _payload_checkAccessToAward(awardId=str(prepared_token_entity), token=str(prepared_token_entity),
                                    owner=prepared_owner, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "token": token,
            "owner": owner,
            "awardId": awardId
        }

        return payload

    return _payload_checkAccessToAward


@pytest.fixture(scope='function')
def payload_createUnsuccessfulAwards(request_template, prepared_cpid, prepared_ev_ocid, prepared_owner):
    payload = request_template(action='createUnsuccessfulAwards')

    def _payload_createUnsuccessfulAwards(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid, owner=prepared_owner,
                                          date="2020-04-28T14:12:32.055Z"):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "lotIds": list(args),
            "date": date,
            "owner": owner
        }

        return payload

    return _payload_createUnsuccessfulAwards


@pytest.fixture(scope='function')
def payload_closeAwardPeriod(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='closeAwardPeriod')

    def _payload_closeAwardPeriod(endDate=None, cpid=prepared_cpid, ocid=prepared_ev_ocid):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "endDate": endDate
        }

        return payload

    return _payload_closeAwardPeriod
