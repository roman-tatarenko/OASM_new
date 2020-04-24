import pytest
from uuid import uuid4


@pytest.fixture(scope='function')
def payload_validateRequirementResponse(request_template, prepared_cpid, prepared_entity_id):
    payload = request_template(action='validateRequirementResponse')

    def _payload_validateRequirementResponse(requirement_id=str(uuid4()), cpid=prepared_cpid, value=True):
        payload['params'] = {
            "cpid": cpid,
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
