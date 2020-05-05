from datetime import datetime
import pytest
from pytest_testrail.plugin import pytestrail
import requests
from resources.domain.tender import schema_tender


@pytestrail.case("C17057")
def test_getOrganization_returns_the_full_role_model_of_the_organization(host, port, prepared_cpid, prepare_data,
                                                                         prepared_ev_ocid, payload_getOrganization,
                                                                         execute_insert_into_access_tender,
                                                                         response, prepared_token_entity,
                                                                         prepared_owner):
    cpid = prepared_cpid

    data = prepare_data(schema=schema_tender)

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_getOrganization(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        role="procuringEntity"

    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = data['tender']['procuringEntity']

    assert actualresult == response.success


@pytestrail.case("C17058")
def test_getOrganization_procuringEntity_objaect_does_not_present_into_DB(host, port, prepared_cpid, prepare_data,
                                                                          prepared_ev_ocid, prepared_token_entity,
                                                                          execute_insert_into_access_tender,
                                                                          payload_getOrganization, prepared_owner,
                                                                          clear_access_tender_by_cpid):
    cpid = prepared_cpid

    data = prepare_data(schema=schema_tender)
    del data['tender']['procuringEntity']

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    payload = payload_getOrganization(
        cpid=cpid,
        ocid=prepared_ev_ocid,
        role="procuringEntity"

    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult['status'] == "incident"


@pytestrail.case("C17084")
@pytest.mark.xfail(reason="Incorrect code  in result in error")
def test_getOrganization_tender_not_found_by_cpid(host, port, prepared_cpid, prepared_ev_ocid, payload_getOrganization,
                                                  response):
    cpid = prepared_cpid
    ocid = prepared_ev_ocid

    payload = payload_getOrganization(
        cpid=cpid,
        ocid=ocid,
        role="procuringEntity"

    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR.COM-1.9.1",
            "description": f"Tender not found by cpid '{cpid}' and ocid '{ocid}'."

        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value, description",

                         [
                             pytest.param("cpid", "ocds-t1s2t3MD9999999999999",
                                          "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'. "
                                          "Actual value: 'ocds-t1s2t3MD9999999999999'.",
                                          marks=pytestrail.case('C17085'),
                                          id="by cpid"),

                             pytest.param("ocid", "ocds-t1s2t3-MD-9999999999999EV0000000000999",
                                          "Data mismatch to pattern: '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                          " Actual value: 'ocds-t1s2t3-MD-9999999999999EV0000000000999'.",
                                          marks=pytestrail.case('C17092'),
                                          id="by ocid")
                         ])
def test_getOrganization_data_mismatch_to_the_pattern(host, port, response, param, value, payload_getOrganization,
                                                      description):
    payload = payload_getOrganization(
        role="procuringEntity"
    )
    payload['params'][param] = value

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-5/3",
            "description": description,
            "details": [{"name": param}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",

                         [
                             pytest.param("cpid",
                                          marks=pytestrail.case('C17086'),
                                          id="cpid"),

                             pytest.param("ocid",
                                          marks=pytestrail.case('C17091'),
                                          id="ocid"),

                             pytest.param("role",
                                          marks=pytestrail.case('C17093'),
                                          id="role")
                         ])
def test_getOrganization_request_does_not_contains_param(host, port, param, payload_getOrganization, response):
    payload = payload_getOrganization()

    del payload['params'][param]

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'.",
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C17094")
@pytest.mark.parametrize('value', ["fundator", "owner", ""])
def test_getOrganization_value_mismatch_with_one_of_enum_expected_values(host, port, value, payload_getOrganization,
                                                                         response):
    payload = payload_getOrganization(
        role=value
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-3/3",
            "description": "Attribute value mismatch with one of enum expected values. "
                           f"Expected values: 'procuringEntity', actual value: '{value}'.",
            "details": [{"name": "role"}]
        }
    ]

    assert actualresult == response.error
