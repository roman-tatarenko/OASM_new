import pytest


@pytest.fixture(scope='function')
def payload_checkRelatedTenderer(request_template, prepared_cpid, prepared_ev_ocid, prepared_entity_id):
    payload = request_template(acton='checkRelatedTenderer')

    def _payload_checkRelatedTenderer(awardId=str(prepared_entity_id()), requirementId=str(prepared_entity_id()),
                                      relatedTendererId="relatedTendererId", cpid=prepared_cpid,
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
    payload = request_template(acton='createRequirementResponse')

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
                    "responderer": {
                        "id": "respondererId",
                        "name": "respondererName"
                    }
                }
            }
        }
        return payload

    return _payload_addRequirementResponse
