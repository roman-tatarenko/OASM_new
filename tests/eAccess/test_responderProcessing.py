import json
from datetime import datetime

import pytest
from pytest_testrail.plugin import pytestrail
import requests
from uuid import uuid4

from resources.domain.businessFunction import schema_businessFunction
from resources.domain.document import schema_document
from resources.domain.identifier import schema_identifier
from resources.domain.period import schema_period_start_date
from resources.domain.responder import schema_responder
from resources.domain.tender import schema_tender


@pytestrail.case("C13318")
def test_responderProcessing_update_person_object(host, port, prepared_cpid, prepare_data,
                                                  execute_insert_into_access_tender,
                                                  prepared_token_entity, prepared_owner,
                                                  payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['title'] = "tat1"
    responder['name'] = "tat2"
    responder['identifier']['uri'] = "tat_uri"

    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C13319")
def test_responderProcessing_new_persones_object(host, port, prepared_cpid, prepare_data,
                                                 execute_insert_into_access_tender,
                                                 prepared_entity_id,
                                                 prepared_token_entity, prepared_owner,
                                                 payload_responderProcessing, response):
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

    responder = prepare_data(schema=schema_responder)
    responder['identifier']['id'] = str(prepared_entity_id())
    responder['identifier']['scheme'] = "UA-NEDNO"

    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C13320")
def test_responderProcessing_update_businessFunction(host, port, prepared_cpid, prepare_data,
                                                     execute_insert_into_access_tender,
                                                     prepared_token_entity, prepared_owner,
                                                     payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    business_function = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['type'] = "technicalOpener"
    responder['businessFunctions'][0]['jobTitle'] = "tat_4to-4to"
    responder['businessFunctions'][0]['period']['startDate'] = "2020-04-29T11:07:00Z"

    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C13321")
def test_responderProcessing_add_new_business_function_object(host, port, prepared_cpid, prepare_data,
                                                              execute_insert_into_access_tender,
                                                              prepared_token_entity, prepared_owner,
                                                              payload_responderProcessing, response,
                                                              prepared_entity_id):
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

    responder = prepare_data(schema=schema_responder)
    responder['businessFunctions'][0]['id'] = str(prepared_entity_id())
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C13322")
def test_responderProcessing_update_documents_object(host, port, prepared_cpid, prepare_data,
                                                     execute_insert_into_access_tender,
                                                     prepared_token_entity, prepared_owner,
                                                     payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    business_function = prepare_data(schema=schema_businessFunction)
    documents = prepare_data(schema=schema_document)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documents

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['documents'][0] = documents
    responder['businessFunctions'][0]['documents'][0]['title'] = "tat_doc_title"
    responder['businessFunctions'][0]['documents'][0]['description'] = "tat_doc_description"
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C13323")
def test_responderProcessing_add_new_documents_object(host, port, prepared_cpid, prepare_data,
                                                      execute_insert_into_access_tender,
                                                      prepared_token_entity, prepared_owner,
                                                      payload_responderProcessing, response,
                                                      prepared_entity_id):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    business_function = prepare_data(schema=schema_businessFunction)
    documents = prepare_data(schema=schema_document)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documents

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['documents'][0] = documents
    responder['businessFunctions'][0]['documents'][0]['id'] = str(prepared_entity_id())
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C14098")
def test_responderProcessing_without_identifier_uri_if_persones_present_into_DB(host, port, prepare_data,
                                                                                prepared_cpid, prepared_owner,
                                                                                execute_insert_into_access_tender,
                                                                                prepared_token_entity, response,
                                                                                payload_responderProcessing):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    del responder['identifier']['uri']
    responder['title'] = "for compare title"
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16889")
def test_responderProcessing_without_identifier_uri_if_persones_does_not_present_into_DB(host, port, prepared_owner,
                                                                                         prepared_cpid, prepare_data,
                                                                                         execute_insert_into_access_tender,
                                                                                         prepared_token_entity,
                                                                                         payload_responderProcessing,
                                                                                         response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    del data['tender']['procuringEntity']['persones']

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    del responder['identifier']['uri']

    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16890")
def test_responderProcessing_without_documents_if_documents_present_in_DB(host, port, prepared_cpid, prepare_data,
                                                                          execute_insert_into_access_tender,
                                                                          prepared_token_entity, prepared_owner,
                                                                          payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    business_function = prepare_data(schema=schema_businessFunction)
    documents = prepare_data(schema=schema_document)

    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documents

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['title'] = "Title for drop documents[]"
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function.copy()
    del responder['businessFunctions'][0]['documents']
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16891")
def test_responderProcessing_without_documents_if_documents_does_not_present_in_DB(host, port, prepared_cpid, response,
                                                                                   prepare_data, prepared_owner,
                                                                                   execute_insert_into_access_tender,
                                                                                   prepared_token_entity,
                                                                                   payload_responderProcessing):
    cpid = prepared_cpid
    identifier = prepare_data(schema=schema_identifier)
    data = prepare_data(schema=schema_tender)
    business_function = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function

    del business_function['documents']
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C14099")
def test_responderProcessing_without_documents_description_if_persones_present_in_DB(host, port, prepared_cpid,
                                                                                     prepare_data, response,
                                                                                     execute_insert_into_access_tender,
                                                                                     prepared_token_entity,
                                                                                     prepared_owner,
                                                                                     payload_responderProcessing):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    identifier = prepare_data(schema=schema_identifier)
    business_function = prepare_data(schema=schema_businessFunction)
    documents = prepare_data(schema=schema_document)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documents

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['documents'][0] = documents
    responder['businessFunctions'][0]['documents'][0]['title'] = "title88"
    del responder['businessFunctions'][0]['documents'][0]['description']
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16892")
def test_responderProcessing_without_documents_description_if_persones_does_not_present_in_DB(host, port, prepared_cpid,
                                                                                              prepare_data,
                                                                                              execute_insert_into_access_tender,
                                                                                              prepared_token_entity,
                                                                                              prepared_owner, response,
                                                                                              payload_responderProcessing
                                                                                              ):
    cpid = prepared_cpid
    identifier = prepare_data(schema=schema_identifier)
    data = prepare_data(schema=schema_tender)
    business_function = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function

    del business_function['documents']
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = prepare_data(schema=schema_businessFunction)
    del responder['businessFunctions'][0]['documents'][0]['description']
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16893")
def test_responderProcessing_correct_change_businessFunctions_type(host, port, prepared_cpid, prepare_data,
                                                                   execute_insert_into_access_tender,
                                                                   prepared_token_entity, prepared_owner, response,
                                                                   payload_responderProcessing):
    cpid = prepared_cpid
    identifier = prepare_data(schema=schema_identifier)
    data = prepare_data(schema=schema_tender)
    business_function = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['type'] = "technicalOpener"
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16880")
def test_responderProcessing_return_the_created_responder_object_in_the_response(host, port, prepared_cpid,
                                                                                 prepare_data, prepared_token_entity,
                                                                                 execute_insert_into_access_tender,
                                                                                 prepared_owner, response,
                                                                                 payload_responderProcessing):
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

    responder = prepare_data(schema=schema_responder)

    name = responder['name']
    identifier_id = responder['identifier']['id']
    identifier_scheme = responder['identifier']['scheme']
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult['version'] == "2.0.0"
    assert actualresult['status'] == "success"
    assert actualresult['result']['name'] == name
    assert actualresult['result']['identifier']['id'] == identifier_id
    assert actualresult['result']['identifier']['scheme'] == identifier_scheme


@pytestrail.case("C16922")
def test_responderProcessing_add_new_persones_object_if_schema_does_not_coincides(host, port, prepared_cpid,
                                                                                  prepare_data, prepared_token_entity,
                                                                                  execute_insert_into_access_tender,
                                                                                  prepared_owner, response,
                                                                                  payload_responderProcessing):
    cpid = prepared_cpid
    identifier = prepare_data(schema=schema_identifier)
    data = prepare_data(schema=schema_tender)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['identifier']['scheme'] = "TEST SCHEMA"
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"

    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


@pytestrail.case("C16894")
def test_responderProcessing_businessFunctions_type_as_authority_which_presents_in_DB(host, port, prepared_cpid,
                                                                                      prepare_data, prepared_owner,
                                                                                      execute_insert_into_access_tender,
                                                                                      prepared_token_entity, response,
                                                                                      payload_responderProcessing):
    cpid = prepared_cpid
    identifier = prepare_data(schema=schema_identifier)
    data = prepare_data(schema=schema_tender)
    business_function = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = identifier
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = business_function
    business_function['type'] = "authority"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = identifier
    responder['businessFunctions'][0] = business_function
    responder['businessFunctions'][0]['type'] = "technicalOpener"
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.success['result'] = {
        "name": responder['name'],
        "identifier": {
            "id": responder['identifier']['id'],
            "scheme": responder['identifier']['scheme']
        }
    }

    assert actualresult == response.success


# ok -> this test will be failed This is bug
@pytestrail.case("C14095")
def test_responderProcessing_cpid_does_not_present_in_the_DB(host, port, prepared_cpid, prepare_data, response,
                                                             payload_responderProcessing):
    cpid = prepared_cpid
    responder = prepare_data(schema=schema_responder)
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "VR-10.1.4.1",
            "description": "Entity 'TenderProcessEntity' not found by cpid = '" + cpid + "' and stage = 'EV'",
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("authority",
                                          marks=pytestrail.case('C16895'),
                                          id="if businessFunctions.type as authority"),

                             pytest.param("",
                                          marks=pytestrail.case('C16874'),
                                          id="if businessFunctions.type as empty string"),

                         ])
def test_responderProcessing_mismatch_with_one_of_enum_expected_values(port, host, param, response, prepared_cpid,
                                                                       prepared_token_entity, prepared_owner,
                                                                       payload_responderProcessing, prepare_data,
                                                                       execute_insert_into_access_tender):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)

    del data['tender']['procuringEntity']['persones']
    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

    responder = prepare_data(schema=schema_responder)
    responder['businessFunctions'][0]['type'] = param
    payload = payload_responderProcessing(
        cpid=cpid,
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "DR-3/3",
            "description": "Attribute value mismatch with one of enum expected values. "
                           "Expected values: 'chairman, procurementOfficer, contactPoint, "
                           "technicalEvaluator, technicalOpener, priceOpener, priceEvaluator', "
                           "actual value: '" + param + "'.",
            "details": [{"name": "businessFunction.type"}]
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param, value,description",
                         [
                             pytest.param("cpid", "ocds-t1s2t3MD-158581611", "Data mismatch to pattern: "
                                                                             "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'"
                                                                             ". Actual value: 'ocds-t1s2t3MD-158581611'.",
                                          marks=pytestrail.case('C14096'),
                                          id="data of cpid mismatch to the pattern"),

                             pytest.param("ocid", "ocds-t1s2t3-MD15858167-EV-1585", "Data mismatch to pattern: "
                                                                                    "'^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                                                                    " Actual value: 'ocds-t1s2t3-MD15858167-EV-1585'.",
                                          marks=pytestrail.case('C14097'),
                                          id="data of ocid mismatch to the pattern"),

                         ])
def test_responderProcessing_if_data_of_ocid_ocid_mismatch_to_the_pattern(port, host, param, response, description,
                                                                          payload_responderProcessing, prepare_data,
                                                                          prepared_cpid, value):
    responder = prepare_data(schema=schema_responder)
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
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
                                          marks=pytestrail.case('C16842'),
                                          id="without cpid attribute"),

                             pytest.param("responder",
                                          marks=pytestrail.case('C16843'),
                                          id="without  responder object "),

                             pytest.param("date",
                                          marks=pytestrail.case('C16858'),
                                          id="without date attribute")

                         ])
def test_responderProcessing_without_cpid_responder_date_in_params(port, host, param, response,
                                                                   payload_responderProcessing):
    payload = payload_responderProcessing(date="2020-04-24T11:07:00Z")
    del payload['params'][param]
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("title",
                                          marks=pytestrail.case('C16844'),
                                          id="without responder.title"),

                             pytest.param("name",
                                          marks=pytestrail.case('C16845'),
                                          id="without responder.name"),

                             pytest.param("identifier",
                                          marks=pytestrail.case('C16846'),
                                          id="without responder.identifier"),

                             pytest.param("businessFunctions",
                                          marks=pytestrail.case('C16849'),
                                          id="without responder.businessFunctions"),

                         ])
def test_responderProcessing_without_responder_title_name_identifier_businessFunctions(port, host, param,
                                                                                       response, prepare_data,
                                                                                       payload_responderProcessing):
    responder = prepare_data(schema=schema_responder)
    del responder[param]
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("scheme",
                                          marks=pytestrail.case('C16847'),
                                          id="without responder.identifier.scheme"),

                             pytest.param("id",
                                          marks=pytestrail.case('C16848'),
                                          id="without responder.identifier.id")

                         ])
def test_responderProcessing_without_responder_identifier_id(port, host, param, response, prepare_data,
                                                             payload_responderProcessing):
    responder = prepare_data(schema=schema_responder)
    del responder['identifier'][param]
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case('C16850'),
                                          id=" request without responder.businessFunctions.id attribute"),

                             pytest.param("type",
                                          marks=pytestrail.case('C16851'),
                                          id="request without responder.businessFunctions.type attribute"),

                             pytest.param("jobTitle",
                                          marks=pytestrail.case('C16852'),
                                          id="request without responder.businessFunctions.jobTitle attribute"),

                             pytest.param("period",
                                          marks=pytestrail.case('C16853'),
                                          id="request without responder.businessFunctions.period object"),

                         ])
def test_responderProcessing_request_without_businessFunctions_id_type_jobTitle_period_object(port, host, param,
                                                                                              response, prepare_data,
                                                                                              payload_responderProcessing):
    responder = prepare_data(schema=schema_responder)
    del responder['businessFunctions'][0][param]
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytestrail.case("C16854")
def test_responderProcessing_without_businessFunctions_period_startDate_attribute(port, host, response, prepare_data,
                                                                                  payload_responderProcessing):
    responder = prepare_data(schema=schema_responder)
    del responder['businessFunctions'][0]['period']['startDate']
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error


@pytest.mark.parametrize("param",
                         [
                             pytest.param("id",
                                          marks=pytestrail.case("C16855"),
                                          id="without responder.businessFunctions.documents.id attribute"),

                             pytest.param("documentType",
                                          marks=pytestrail.case("C16856"),
                                          id="without responder.businessFunctions.documents.documentType "
                                             "attribute"),

                             pytest.param("title",
                                          marks=pytestrail.case('C16857'),
                                          id="without responder.businessFunctions.documents.title attribute")

                         ])
def test_responderProcessing_without_businessFunctions_documents_id_documentType_title(port, host, param, response,
                                                                                       payload_responderProcessing,
                                                                                       prepare_data):
    responder = prepare_data(schema=schema_responder)
    del responder['businessFunctions'][0]['documents'][0][param]
    payload = payload_responderProcessing(
        responder=responder,
        date="2020-04-24T11:07:00Z"
    )

    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
    response.error['result'] = [
        {
            "code": "RQ-02/3",
            "description": "Can not parse 'params'."
        }
    ]

    assert actualresult == response.error
