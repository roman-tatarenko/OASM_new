import json
from uuid import uuid4

import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C23060')
def test_checkAccessToQualification_check_on_service_return_success_in_response_without_result(port, host,
                                                                                               prepared_cpid,
                                                                                               prepared_token_entity,
                                                                                               prepared_owner, response,
                                                                                               data_tender,
                                                                                               payload_checkAccessToTender,
                                                                                               execute_insert_into_qualifications,
                                                                                               data_qualification,
                                                                                               prepared_tp_ocid,
                                                                                               payload_checkAccessToQualification):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )
    payload = payload_checkAccessToQualification(
        cpid=cpid,
        ocid=ocid,
        token=token,
        owner=owner,
        qualificationId=qualification_id
    )
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()

    print(json.dumps(data))
    print(json.dumps(payload))
    print(json.dumps(actualresult))
    assert actualresult == response.success


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("cpid", "ocds-t1s2t3-MD-1599999999999",
                                          marks=pytestrail.case('C23062'),
                                          id="cpid does not present into DB"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-1599999999999-TP-1599999999999",
                                          marks=pytestrail.case('C23063'),
                                          id="ocid does not present into DB"),

                             pytest.param("qualificationId", "810d47da-9999-9999-9999-9b774b1a0525",
                                          marks=pytestrail.case('C23061'),
                                          id="qualificationId does not present into DB")

                         ])
def test_checkAccessToQualification_check_on_service_return_error_in_response(prepared_cpid, prepared_tp_ocid,
                                                                              data_qualification,
                                                                              execute_insert_into_qualifications,
                                                                              payload_checkAccessToQualification,
                                                                              param, value, host, port, response):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )

    payload = payload_checkAccessToQualification(
        cpid=cpid,
        ocid=ocid,
        token=token,
        owner=owner,
        qualificationId=qualification_id
    )

    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['cpid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.14.3/22",
            "description": f"Qualification not found by cpid='ocds-t1s2t3-MD-1599999999999' and"
                           f" ocid='{ocid}' and "
                           f"id='{qualification_id}'."

        }]

    elif payload['params']['ocid'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.14.3/22",
            "description": f"Qualification not found by cpid='{cpid}' and"
                           f" ocid='ocds-t1s2t3-MD-1599999999999-TP-1599999999999' and "
                           f"id='{qualification_id}'."

        }]
    elif payload['params']['qualificationId'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.14.3/22",
            "description": f"Qualification not found by cpid='{cpid}' and"
                           f" ocid='{ocid}' and "
                           f"id='810d47da-9999-9999-9999-9b774b1a0525'."

        }]

    print(json.dumps(actualresult))
    print(json.dumps(response.error))

    assert actualresult == response.error


@pytest.mark.parametrize("param, value",
                         [
                             pytest.param("token", "810d47da-9999-9999-9999-9b774b1a0525",
                                          marks=pytestrail.case('C23064'),
                                          id="token does not present into DB"),

                             pytest.param("owner", "810d47da-9999-9999-9999-9b774b1a0525",
                                          marks=pytestrail.case('C23065'),
                                          id="owner does not present into DB")
                         ])
def test_checkAccessToQualification_service_return_error_in_response_token_owner(execute_insert_into_qualifications,
                                                                                 prepared_cpid, prepared_tp_ocid,
                                                                                 data_qualification,
                                                                                 payload_checkAccessToQualification,
                                                                                 param,
                                                                                 value, host, port, response):
    qualification_id = str(uuid4())
    cpid = prepared_cpid
    ocid = prepared_tp_ocid
    token = str(uuid4())
    owner = str(uuid4())
    data = data_qualification
    data['id'] = qualification_id
    data['token'] = token
    data['owner'] = owner
    execute_insert_into_qualifications(
        cpid=cpid,
        ocid=ocid,
        id=qualification_id,
        json_data=data
    )

    payload = payload_checkAccessToQualification(
        cpid=cpid,
        ocid=ocid,
        token=token,
        owner=owner,
        qualificationId=qualification_id
    )
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['token'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.14.1/22",
            "description": f"Invalid token '{value}' by cpid '{cpid}'."
        }]
        print(json.dumps(response.error))
    elif payload['params']['owner'] == value:
        response.error['result'] = [{
            "code": "VR.COM-7.14.2/22",
            "description": f"Invalid owner '{value}' by cpid '{cpid}'."
        }]
        print(json.dumps(response.error))

    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C23080'),
                                          id="without cpid in params object"),

                             pytest.param("ocid",
                                          marks=pytestrail.case('C23081'),
                                          id="without ocid in params object"),

                             pytest.param("token",
                                          marks=pytestrail.case('C23082'),
                                          id="without token in params object"),

                             pytest.param("owner",
                                          marks=pytestrail.case('C23083'),
                                          id="without owner in params object"),

                             pytest.param("qualificationId",
                                          marks=pytestrail.case('C23084'),
                                          id="without qualificatinId in params object")
                         ])
def test_checkAccessTo_Qualification_without_attribute_in_params_object(payload_checkAccessToQualification,
                                                                        prepared_cpid, prepared_tp_ocid,
                                                                        prepared_token_entity, param, host, port,
                                                                        response):
    payload = payload_checkAccessToQualification()
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-1/22",
        "description": "Error parsing 'params'"
    }]

    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytest.mark.parametrize("param, value, code, description",
                         [
                             pytest.param("cpid", True, "DR-5/22", "Data mismatch of attribute 'cpid' to the pattern:"
                                                                   " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                                                   "Actual value: 'true'.",
                                          marks=pytestrail.case('C23085'),
                                          id="data type mismatch of cpid"),

                             pytest.param("ocid", True, "DR-5/22", "Data mismatch of attribute"
                                                                   " 'ocid' to the pattern: "
                                                                   "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-"
                                                                   "(AC|EI|EV|FS|NP|PN|TP)-[0-9]{13}$'. Actual value: "
                                                                   "'true'.",
                                          marks=pytestrail.case('C23086'),
                                          id="data type mismatch of ocid"),

                             pytest.param("token", True, "DR-4/22", "Data format mismatch of attribute 'token'. "
                                                                    "Expected data format: 'uuid', actual value: "
                                                                    "'true'.",
                                          marks=pytestrail.case('C23087'),
                                          id="data type mismatch of token"),

                             pytest.param("owner", True, "DR-4/22", "Data format mismatch of attribute 'owner'. "
                                                                    "Expected data format: 'uuid', actual value: "
                                                                    "'true'.",
                                          marks=pytestrail.case('C23088'),
                                          id="data type mismatch of owner"),

                             pytest.param("qualificationId", False, "DR-4/22",
                                          "Data format mismatch of attribute 'id'. "
                                          "Expected data format: "
                                          "'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                                          "[0-9a-f]{4}-[0-9a-f]{12}$', "
                                          "actual value: 'false'.",
                                          marks=pytestrail.case('C23089'),
                                          id="data type mismatch of qualificationId")
                         ])
def test_checkAccessTo_Qualification_data_type_mismatch_of_attribute(payload_checkAccessToQualification, param, value,
                                                                     host, port, response, code, description):
    payload = payload_checkAccessToQualification()
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    if payload['params']['qualificationId'] == value:
        response.error['result'] = [{
            "code": str(code),
            "description": str(description),
            "details": [{"name": "id"}]
        }]
    else:
        response.error['result'] = [{
            "code": str(code),
            "description": str(description),
            "details": [{"name": str(param)}]
        }]
    print(json.dumps(response.error))
    print(json.dumps(actualresult))
    assert actualresult == response.error


@pytestrail.case('C23118')
def test_checkAccessTo_Qualification_empty_params_object(payload_checkAccessToQualification, host, port, response):
    payload = payload_checkAccessToQualification()
    payload['params'] = {}

    actualresult = requests.post(f'{host}:{port.eQualification}/command2', json=payload).json()
    response.error['result'] = [{
        "code": "RQ-1/22",
        "description": "Error parsing 'params'"
    }]
    print(json.dumps(payload))
    print(json.dumps(actualresult))
    print(json.dumps(response.error))
    assert actualresult == response.error
