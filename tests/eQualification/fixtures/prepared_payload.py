from uuid import uuid4

import pytest


@pytest.fixture(scope='function')
def payload_checkAccessToQualification(request_template, prepared_cpid, prepared_tp_ocid, prepared_owner,
                                       prepared_token_entity, prepared_entity_id):
    payload = request_template(action='checkAccessToQualification')

    def _payload_checkAccessToQualification(cpid=prepared_cpid, ocid=prepared_tp_ocid, token=str(prepared_token_entity),
                                            owner=prepared_owner, qualificationId=str(uuid4())):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "token": token,
            "owner": owner,
            "qualificationId": qualificationId
        }
        return payload

    return _payload_checkAccessToQualification
