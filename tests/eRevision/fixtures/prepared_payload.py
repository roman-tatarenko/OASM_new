import pytest

@pytest.fixture(scope='function')
def prepared_payload_findAmendmentIds(prepared_request_id, prepared_cpid, prepared_ev_ocid):
    def with_values(version="2.0.0", id=f"{prepared_request_id}", action="findAmendmentIds",
                    relatesTo="tender", status="pending", type="cancellation", cpid=prepared_cpid,
                    ocid=prepared_ev_ocid, relatedItems=prepared_ev_ocid):
        return {
            "version": version,
            "id": id,
            "action": action,
            "params": {
                "status": status,
                "type": type,
                "relatesTo": relatesTo,
                "relatedItems": [relatedItems],
                "cpid": cpid,
                "ocid": ocid
            }
        }

    return with_values


@pytest.fixture(scope='function')
def prepared_payload_dataValidation(prepared_request_id, prepared_entity_id, prepared_cpid, prepared_ev_ocid):
    def with_values(id=prepared_request_id, amendment_id=prepared_entity_id()):
        return {
            "version": "2.0.0",
            "id": f"{id}",
            "action": "dataValidation",
            "params": {
                "amendment": {
                    "rationale": "Some_string_1",
                    "description": "Some_string_2",
                    "documents": [
                        {
                            "documentType": "cancellationDetails",
                            "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                            "title": "string",
                            "description": "string"
                        }
                    ],
                    "id": f"{amendment_id}"
                },
                "cpid": f"{prepared_cpid}",
                "ocid": f"{prepared_ev_ocid}",
                "operationType": "tenderCancellation"
            }
        }

    return with_values


@pytest.fixture(scope='function')
def prepared_payload_createAmendment(prepared_request_id, prepared_cpid, prepared_ev_ocid, prepared_entity_id):
    def _prepared_payload_createAmendment(amendment_id=prepared_entity_id()):
        return {
            "version": "2.0.0",
            "id": f"{prepared_request_id}",
            "action": "createAmendment",
            "params": {
                "amendment": {
                    "rationale": "Some_string_1",
                    "description": "Some_string_2",
                    "documents": [{
                        "documentType": "cancellationDetails",
                        "id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                        "title": "amendments documents title",
                        "description": "amendments documents description"
                    }],
                    "id": f"{amendment_id}"
                },
                "relatedEntityId": f"{prepared_ev_ocid}",
                "operationType": "tenderCancellation",
                "date": "2020-02-28T16:14:54Z",
                "cpid": f"{prepared_cpid}",
                "ocid": f"{prepared_ev_ocid}",
                "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        }

    return _prepared_payload_createAmendment


@pytest.fixture(scope='function')
def payload_checkAccessToAmendment(request_template, prepared_cpid, prepared_ev_ocid, prepared_owner,
                                   prepared_entity_id, prepared_token_entity):
    payload = request_template(acton='checkAccessToAmendment')

    def _payload_checkAccessToAmendment(token=str(prepared_token_entity), amendmentId=str(prepared_entity_id()),
                                        owner=prepared_owner, cpid=prepared_cpid, ocid=prepared_ev_ocid,
                                        ):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "token": token,
            "owner": owner,
            "amendmentId": amendmentId
        }
        return payload

    return _payload_checkAccessToAmendment
