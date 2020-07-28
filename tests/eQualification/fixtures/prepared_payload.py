from uuid import uuid4
from resources.domain._ import _

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


@pytest.fixture(scope='function')
def payload_checkQualificationState(request_template, prepared_cpid, prepared_tp_ocid, prepared_entity_id):
    payload = request_template(action='checkQualificationState')

    def _payload_checkQualificationState(cpid=prepared_cpid, ocid=prepared_tp_ocid, operationType=None,
                                         qualificationId=str(uuid4())):
        pmd = ("GPA", "TEST_GPA",)
        country = ("MD",)
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "country": _("random.schoice", seq=country, end=1),
            "pmd": _("random.schoice", seq=pmd, end=1),
            "operationType": operationType,
            "qualificationId": qualificationId
        }
        return payload

    return _payload_checkQualificationState


@pytest.fixture(scope='function')
def payload_doConsideration(request_template, prepared_cpid, prepared_tp_ocid, prepared_entity_id):
    payload = request_template(action='doConsideration')

    def _payload_doConsideration(cpid=prepared_cpid, ocid=prepared_tp_ocid, id=uuid4()):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "qualifications": [{
                "id": id
            }]
        }
        return payload

    return _payload_doConsideration
