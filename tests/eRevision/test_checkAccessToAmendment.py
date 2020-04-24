import pytest
from pytest_testrail.plugin import pytestrail
import requests
import uuid


@pytestrail.case("C15031")
def test_checkAccessToAmendment_check_access_to_amendment_of_tender(host, port, execute_insert_into_revision_amendments,
                                                                    prepared_create_amendment, prepared_cpid,
                                                                    prepared_ev_ocid, prepared_entity_id,
                                                                    payload_checkAccessToAmendment,
                                                                    prepared_token_entity,
                                                                    prepared_owner,
                                                                    response):
    amendment_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = "tender"
    data['relatedItem'] = prepared_ev_ocid
    data['token'] = str(prepared_token_entity())
    data['owner'] = prepared_owner
    execute_insert_into_revision_amendments(
        cpid=prepared_cpid,
        ocid=prepared_ev_ocid,
        id=amendment_id,
        data=data
    )

    payload = payload_checkAccessToAmendment(
        amendmentId=str(amendment_id),
        token=data['token'],
        owner=data['owner']
    )

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytestrail.case("C15035")
def test_checkAccessToAmendment_check_access_to_amendment_of_second_lot(host, port,
                                                                        execute_insert_into_revision_amendments,
                                                                        prepared_create_amendment, prepared_cpid,
                                                                        prepared_ev_ocid, prepared_entity_id,
                                                                        payload_checkAccessToAmendment,
                                                                        prepared_token_entity, prepared_owner,
                                                                        response):
    cpid = prepared_cpid
    ocid = prepared_ev_ocid
    amendment_id = prepared_entity_id()
    lot_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = "lot"
    data['relatedItem'] = str(lot_id)
    data['token'] = str(prepared_token_entity)
    data['owner'] = str(prepared_owner)
    execute_insert_into_revision_amendments(
        cpid=cpid,
        ocid=ocid,
        id=amendment_id,
        data=data
    )

    amendment_id_2 = prepared_entity_id()
    lot_id_2 = prepared_entity_id()
    data_2 = prepared_create_amendment
    data_2['id'] = str(amendment_id_2)
    data_2['relatesTo'] = 'lot'
    data_2['relatedItem'] = str(lot_id_2)
    data_2['token'] = data['token']
    data_2['owner'] = data['owner']
    execute_insert_into_revision_amendments(
        cpid=cpid,
        ocid=ocid,
        id=amendment_id_2,
        data=data_2
    )

    payload = payload_checkAccessToAmendment(
        cpid=cpid,
        ocid=ocid,
        token=data_2['token'],
        owner=data_2['owner'],
        amendmentId=str(amendment_id_2)
    )

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("cpid", "", "DR-5/21",
                                          "Data mismatch of attribute 'cpid'"
                                          " to the pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case("C15040"),
                                          id="cpid as emptyString"),

                             pytest.param("cpid", 22.9, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: '22.9'.",
                                          marks=pytestrail.case("C15041"),
                                          id="cpid as number"),

                             pytest.param("cpid", True, "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                          " Actual value: 'true'.",
                                          marks=pytestrail.case("C15042"),
                                          id="cpid as boolean"),

                             pytest.param("cpid", "ocdst1s2t3MD-1589999909002", "DR-5/21",
                                          "Data mismatch of attribute 'cpid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: 'ocdst1s2t3MD-1589999909002'.",
                                          marks=pytestrail.case("C15043"),
                                          id="cpid mismatch")
                         ])
def test_checkAccessToAmendment_if_cpid_of_param_mismatch_to_the_pattern(port, host, param, value, code, description,
                                                                         payload_checkAccessToAmendment, response):
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("ocid", '', "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: ''.",
                                          marks=pytestrail.case("C15045"),
                                          id="ocid as emptyString"),

                             pytest.param("ocid", 22.9, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: '22.9'.",
                                          marks=pytestrail.case("CC15047"),
                                          id="ocid as number"),

                             pytest.param("ocid", True, "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'true'.",
                                          marks=pytestrail.case("C15046"),
                                          id="ocid as boolean"),

                             pytest.param("ocid", "ocdst1s2t3MD1589999909002EV1586476001000", "DR-5/21",
                                          "Data mismatch of attribute 'ocid' to the pattern: "
                                          "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'. "
                                          "Actual value: 'ocdst1s2t3MD1589999909002EV1586476001000'.",
                                          marks=pytestrail.case("C15048"),
                                          id="ocid mismatch")
                         ])
def test_checkAccessToAmendment_if_ocid_of_param_mismatch_to_the_pattern(port, host, param, value, code, description,
                                                                         payload_checkAccessToAmendment, response):
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-9999999999999",
                                          marks=pytestrail.case("C15036"),
                                          id="cpid does not present in DB"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-9999999999999-EV-9999999999999",
                                          marks=pytestrail.case("C15044"),
                                          id="ocid does not present in DB"),

                             pytest.param("amendmentId", "9fa99f99-9999-9999-b9fc-9c999f99afa9",
                                          marks=pytestrail.case("C15059"),
                                          id="amendment does not present in DB")

                         ])
def test_checkAccessToAmendment_if_amendment_does_not_present_in_DB(port, host, param,
                                                                    value, payload_checkAccessToAmendment,
                                                                    response, prepared_cpid, prepared_ev_ocid,
                                                                    prepared_entity_id, prepared_create_amendment,
                                                                    prepared_token_entity, prepared_owner,
                                                                    execute_insert_into_revision_amendments):
    cpid = prepared_cpid
    ocid = prepared_ev_ocid
    amendment_id = prepared_entity_id()
    lot_id = prepared_entity_id()
    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = "lot"
    data['relatedItem'] = str(lot_id)
    data['token'] = str(prepared_token_entity)
    data['owner'] = str(prepared_owner)
    execute_insert_into_revision_amendments(
        cpid=cpid,
        ocid=ocid,
        id=amendment_id,
        data=data
    )
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.2.4.3/21",
            "description": "Amendment not found.",
            "details": [{"id": payload['params']['amendmentId']}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("token", "ed9e99b9-82c9-9bcc-ac99-999999afa999", "VR-10.2.4.1/21",
                                          "Request token doesn't match token from the database.",
                                          marks=pytestrail.case("C15049"),
                                          id="token does not present in DB"),

                             pytest.param("owner", "9fa99f99-9999-9999-b9fc-9c999f99afa9", "VR-10.2.4.2/21",
                                          "Request owner doesn't match owner from the database.",
                                          marks=pytestrail.case("C15054"),
                                          id="owner does not present in DB")

                         ])
def test_checkAccessToAmendment_does_not_access_to_amendment(port, host, param, prepared_create_amendment, value, code,
                                                             description, payload_checkAccessToAmendment, response,
                                                             execute_insert_into_revision_amendments):
    payload = payload_checkAccessToAmendment()
    cpid = payload['params']['cpid']
    ocid = payload['params']['ocid']
    amendment_id = uuid.UUID(payload['params']['amendmentId'])
    token = payload['params']['token']
    owner = payload['params']['owner']

    data = prepared_create_amendment
    data['id'] = str(amendment_id)
    data['relatesTo'] = 'tender'
    data['relatedItem'] = ocid
    data['token'] = token
    data['owner'] = owner

    execute_insert_into_revision_amendments(
        cpid=cpid,
        ocid=ocid,
        id=amendment_id,
        data=data
    )

    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description

        }
    ]
    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("token", "", "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C15050"),
                                          id="token as emptyString"),

                             pytest.param("token", 22.9, "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: '22.9'.",
                                          marks=pytestrail.case("C15051"),
                                          id="token as number"),

                             pytest.param("token", True, "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: 'true'.",
                                          marks=pytestrail.case("C15052"),
                                          id="token_as_boolean"),

                             pytest.param("token", "8f8d8f9c862048a99da6251a90285f42", "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: "
                                          "'8f8d8f9c862048a99da6251a90285f42'.",
                                          marks=pytestrail.case("C15053"),
                                          id="token_mismatch")
                         ])
def test_checkAccessToAmendment_if_data_format_mismatch_of_attribute_token(port, host, param, value, code, description,
                                                                           payload_checkAccessToAmendment, response):
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("owner", "", "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C15055"),
                                          id="owner as emptyString"),

                             pytest.param("owner", 22.9, "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: '22.9'.",
                                          marks=pytestrail.case("C15056"),
                                          id="owner as number"),

                             pytest.param("owner", True, "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: 'true'.",
                                          marks=pytestrail.case("C15057"),
                                          id="owner as boolean"),

                             pytest.param("owner", "9fa99f9999999999b9fc9c999f99afa9", "DR-4/21",
                                          "Data format mismatch of attribute 'token'. "
                                          "Expected data format: 'uuid', actual value: "
                                          "'9fa99f9999999999b9fc9c999f99afa9'.",
                                          marks=pytestrail.case("C15058"),
                                          id="owner mismatch")
                         ])
def test_checkAccessToAmendment_if_data_format_mismatch_of_attribute_owner(port, host, param, value, code, description,
                                                                           payload_checkAccessToAmendment, response):
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param("amendmentId", "", "DR-4/21",
                                          "Data format mismatch of attribute 'amendmentId'. "
                                          "Expected data format: 'uuid', actual value: ''.",
                                          marks=pytestrail.case("C15060"),
                                          id="amendment as emptyString"),

                             pytest.param("amendmentId", 22.9, "DR-4/21",
                                          "Data format mismatch of attribute 'amendmentId'. "
                                          "Expected data format: 'uuid', actual value: '22.9'.",
                                          marks=pytestrail.case("C15061"),
                                          id="amendment as number"),

                             pytest.param("amendmentId", True, "DR-4/21",
                                          "Data format mismatch of attribute 'amendmentId'. "
                                          "Expected data format: 'uuid', actual value: 'true'.",
                                          marks=pytestrail.case("C15062"),
                                          id="amendment as boolean"),

                             pytest.param("amendmentId", "9fa99f9999999999b9fc9c999f99afa9", "DR-4/21",
                                          "Data format mismatch of attribute 'amendmentId'. "
                                          "Expected data format: 'uuid', "
                                          "actual value: '9fa99f9999999999b9fc9c999f99afa9'.",
                                          marks=pytestrail.case("C15063"),
                                          id="amendment mismatch")
                         ])
def test_checkAccessToAmendment_if_data_format_mismatch_of_attribute_amendment(port, host, param, value, code,
                                                                               payload_checkAccessToAmendment, response,
                                                                               description):
    payload = payload_checkAccessToAmendment()
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": code,
            "description": description,
            "details": [
                {
                    "name": param
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case("C15066"),
                                          id="without cpid attribute"),

                             pytest.param("ocid",
                                          marks=pytestrail.case("C15067"),
                                          id="without ocid attribute"),

                             pytest.param("token",
                                          marks=pytestrail.case("C15068"),
                                          id="without token attribute"),

                             pytest.param("owner",
                                          marks=pytestrail.case("C15069"),
                                          id="without owner attribute"),

                             pytest.param("amendmentId",
                                          marks=pytestrail.case("C15070"),
                                          id="without amendment attribute")

                         ])
def test_checkAccessToAmendment_without_param_in_params(port, host, param, payload_checkAccessToAmendment, response):
    payload = payload_checkAccessToAmendment()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eRevision}/command', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-1/21",
            "description": "Error parsing 'params'"

        }
    ]
    assert actualresult == response.error
