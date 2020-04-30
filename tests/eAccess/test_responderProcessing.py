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
def test_responderProcessing_changes_in_persones_persones_update(host, port, prepared_cpid, prepare_data,
                                                                 execute_insert_into_access_tender,
                                                                 prepared_token_entity, prepared_owner,
                                                                 payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['title'] = "tat1"
    responder['name'] = "tat2"
    responder['identifier']['uri'] = "tat_uri"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C13319")
def test_responderProcessing_new_persones_information_add_persones(host, port, prepared_cpid, prepare_data,
                                                                   execute_insert_into_access_tender,
                                                                   prepared_token_entity, prepared_owner,
                                                                   payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = prepare_data(schema=schema_identifier)

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C13320")
def test_responderProcessing_persones_business_function_update(host, port, prepared_cpid, prepare_data,
                                                               execute_insert_into_access_tender,
                                                               prepared_token_entity, prepared_owner,
                                                               payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    busFuncVal = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = busFuncVal

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['businessFunctions'][0] = busFuncVal
    responder['businessFunctions'][0]['type'] = "technicalOpener"
    responder['businessFunctions'][0]['jobTitle'] = "tat_4to-4to"
    responder['businessFunctions'][0]['period']['startDate'] = "2020-04-29T11:07:00Z"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C13321")
def test_responderProcessing_new_business_function_information_in_persones(host, port, prepared_cpid, prepare_data,
                                                                           execute_insert_into_access_tender,
                                                                           prepared_token_entity, prepared_owner,
                                                                           payload_responderProcessing, response,
                                                                           prepared_entity_id):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    busFuncVal = prepare_data(schema=schema_businessFunction)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = busFuncVal

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['businessFunctions'][0] = busFuncVal
    responder['businessFunctions'][0]['id'] = str(prepared_entity_id())

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C13322")
def test_responderProcessing_changes_of_persones_documents_documents_update(host, port, prepared_cpid, prepare_data,
                                                                            execute_insert_into_access_tender,
                                                                            prepared_token_entity, prepared_owner,
                                                                            payload_responderProcessing, response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    busFuncVal = prepare_data(schema=schema_businessFunction)
    documentVal = prepare_data(schema=schema_document)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = busFuncVal
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documentVal

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['businessFunctions'][0] = busFuncVal
    responder['businessFunctions'][0]['documents'][0] = documentVal
    responder['businessFunctions'][0]['documents'][0]['title'] = "tat_doc_title"
    responder['businessFunctions'][0]['documents'][0]['description'] = "tat_doc_description"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C13323")
def test_responderProcessing_new_persones_documents_add_new_documents(host, port, prepared_cpid, prepare_data,
                                                                      execute_insert_into_access_tender,
                                                                      prepared_token_entity, prepared_owner,
                                                                      payload_responderProcessing, response,
                                                                      prepared_entity_id):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    busFuncVal = prepare_data(schema=schema_businessFunction)
    documentVal = prepare_data(schema=schema_document)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = busFuncVal
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documentVal

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['businessFunctions'][0] = busFuncVal
    responder['businessFunctions'][0]['documents'][0] = documentVal
    responder['businessFunctions'][0]['documents'][0]['id'] = str(prepared_entity_id())

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C14098")
def test_responderProcessing_without_responder_identifier_uri_persones_present_into_DB(host, port,
                                                                                       prepared_cpid,
                                                                                       prepare_data,
                                                                                       execute_insert_into_access_tender,
                                                                                       prepared_token_entity,
                                                                                       prepared_owner,
                                                                                       payload_responderProcessing,
                                                                                       response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)
    data['tender']['procuringEntity']['persones'][0]['identifier'] = val

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    del responder['identifier']['uri']
    responder['title'] = "for compare title"

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C16889")
def test_responderProcessing_without_responder_identifier_uri_persones_does_not_present_into_DB(host, port,
                                                                                                prepared_cpid,
                                                                                                prepare_data,
                                                                                                execute_insert_into_access_tender,
                                                                                                prepared_token_entity,
                                                                                                prepared_owner,
                                                                                                payload_responderProcessing,
                                                                                                response):
    cpid = prepared_cpid

    data = prepare_data(schema=schema_tender)
    name=data.copy()

    del name['tender']['procuringEntity']['persones']



    responder = prepare_data(schema=schema_responder)

    # responder['identifier'] = prepare_data(schema=schema_identifier)
    del responder['identifier']['uri']


    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C16890")
def test_responderProcessing_without_responder_businessFunction_documents_object_0(host, port,
                                                                                 prepared_cpid,
                                                                                 prepare_data,
                                                                                 execute_insert_into_access_tender,
                                                                                 prepared_token_entity,
                                                                                 prepared_owner,
                                                                                 payload_responderProcessing,
                                                                                 response):
    cpid = prepared_cpid

    data = prepare_data(schema=schema_tender)

    val = prepare_data(schema=schema_identifier)
    busFuncVal = prepare_data(schema=schema_businessFunction)
    documentVal = prepare_data(schema=schema_document)

    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0] = busFuncVal
    data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0] = documentVal

    responder = prepare_data(schema=schema_responder)
    responder['title'] = "Title for drop documents[]"
    responder['identifier'] = val
    responder['businessFunctions'][0] = busFuncVal
    del responder['businessFunctions'][0]['documents']

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success


@pytestrail.case("C16891")
def test_responderProcessing_without_responder_businessFunction_documents_objec_does_not_presentDB_1(host, port,
                                                                                                   prepared_cpid,
                                                                                                   prepare_data,
                                                                                                   execute_insert_into_access_tender,
                                                                                                   prepared_token_entity,
                                                                                                   prepared_owner,
                                                                                                   payload_responderProcessing,
                                                                                                   response):
    cpid = prepared_cpid
    data = prepare_data(schema=schema_tender)
    val = prepare_data(schema=schema_identifier)

    data['tender']['procuringEntity']['persones'][0]['identifier'] = val
    id_busFunc = data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['id']
    del data['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents']

    responder = prepare_data(schema=schema_responder)
    responder['identifier'] = val
    responder['businessFunctions'][0] = prepare_data(schema=schema_businessFunction)
    responder['businessFunctions'][0]['id'] = id_busFunc
    responder['businessFunctions'][0]['documents'][0] = prepare_data(schema=schema_document)

    execute_insert_into_access_tender(
        cp_id=cpid,
        stage="EV",
        token_entity=prepared_token_entity,
        created_date=datetime.now(),
        json_data=data,
        owner=prepared_owner
    )

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
    print(cpid)
    assert actualresult == response.success
