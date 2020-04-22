import pytest


@pytest.fixture(scope='function')
def payload_validateRequirementResponse(request_template, prepared_cpid, prepared_ev_ocid, prepared_entity_id):
    payload = request_template(action='validateRequirementResponse')

    def _payload_validateRequirementResponse(requirement_id=str(prepared_entity_id()), cpid=prepared_cpid,
                                             ocid=prepared_ev_ocid, value=True):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "requirementResponse": {
                "id": "string",
                "value": value,
                "requirement": {
                    "id": requirement_id
                }
            }
        }
        return payload

    return _payload_validateRequirementResponse
