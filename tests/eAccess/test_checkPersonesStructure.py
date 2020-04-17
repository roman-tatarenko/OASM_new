import pytest
import requests
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C13271')
def test_checkPersonesStructure_if_a_request_contains_valid_data(host, port, payload_checkPersonesStructure,
                                                                 response, data_person):
    payload = payload_checkPersonesStructure(persones=[data_person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13272')
def test_checkPersonesStructure_if_a_request_does_not_contain_identifier_uri(host, port, payload_checkPersonesStructure,
                                                                             response, data_person):
    del data_person['identifier']['uri']
    payload = payload_checkPersonesStructure(persones=[data_person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13273')
def test_checkPersonesStructure_if_a_request_does_not_contain_businessFunctions_documents(host, port, response,
                                                                                          data_person,
                                                                                          payload_checkPersonesStructure
                                                                                          ):
    person_1 = data_person
    del data_person['businessFunctions'][0]['documents']
    payload = payload_checkPersonesStructure(persones=[person_1], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13274')
def test_checkPersonesStructure_if_a_request_does_not_contain_documents_description(host, port, response,
                                                                                    data_person,
                                                                                    payload_checkPersonesStructure
                                                                                    ):
    person_1 = data_person
    del data_person['businessFunctions'][0]['documents'][0]['description']
    payload = payload_checkPersonesStructure(persones=[person_1], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13294')
def test_checkPersonesStructure_if_a_request_contains_more_than_one_persones_object(host, port, response,
                                                                                    data_person,
                                                                                    payload_checkPersonesStructure
                                                                                    ):
    person_1 = data_person
    person_2 = data_person
    payload = payload_checkPersonesStructure(persones=[person_1, person_2], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytest.mark.parametrize("param,value,code,description",
                         [
                             pytest.param('cpid', '', "DR-5/3", "Data mismatch to pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-[0-9]{13}$'."
                                                                " Actual value: ''.", id='cpid',
                                          marks=pytestrail.case('C13299')),
                             pytest.param('ocid', '', "DR-5/3", "Data mismatch to pattern:"
                                                                " '^[a-z]{4}-[a-z0-9]{6}-[A-Z]{2}-"
                                                                "[0-9]{13}-(AC|EI|EV|FS|NP|PN)-[0-9]{13}$'."
                                                                " Actual value: ''.", id='ocid',
                                          marks=pytestrail.case('C13300'))

                         ])
def test_checkPersonesStructure_if_data_of_attribute_mismatch_to_the_pattern(host, port, data_person, response,
                                                                             param, value, code, description,
                                                                             payload_checkPersonesStructure):
    person = data_person
    payload = payload_checkPersonesStructure(persones=[person], locationOfPersones='award')
    payload['params'][param] = value
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()
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


@pytestrail.case('C13295')
def test_checkPersonesStructure_a_request_contains_more_than_one_businessFunctions_object(host, port, data_person,
                                                                                          response,
                                                                                          data_businessFunction,
                                                                                          payload_checkPersonesStructure):
    person = data_person
    person['businessFunctions'].append(data_businessFunction)
    payload = payload_checkPersonesStructure(persones=[person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success


@pytestrail.case('C13277')
def test_checkPersonesStructure_a_request_contains_invalid_enum_for_businessFunctions_type(host, port, data_person,
                                                                                           payload_checkPersonesStructure,
                                                                                           response):
    person = data_person
    person['businessFunctions'][0]['type'] = 'authority'
    payload = payload_checkPersonesStructure(persones=[person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [
        {
            "code": "DR-3/3",
            "description": "Attribute value mismatch with one of enum expected values."
                           " Expected values: 'chairman, procurementOfficer, contactPoint,"
                           " technicalEvaluator, technicalOpener, priceOpener, priceEvaluator',"
                           " actual value: 'authority'.",
            "details": [
                {
                    "name": "businessFunction.type"
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C13276')
def test_checkPersonesStructure_a_request_contains_invalid_enum_for_documentType(host, port, data_person,
                                                                                 payload_checkPersonesStructure,
                                                                                 response):
    person = data_person
    person['businessFunctions'][0]['documents'][0]['documentType'] = 'x_eligibilityDocuments'
    payload = payload_checkPersonesStructure(persones=[person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    response.error['result'] = [
        {
            "code": "DR-3/3",
            "description": "Attribute value mismatch with one of enum expected values."
                           " Expected values: 'regulatoryDocument', actual value: 'x_eligibilityDocuments'.",
            "details": [
                {
                    "name": "documentType"
                }
            ]
        }
    ]

    assert actualresult == response.error


@pytestrail.case('C13275')
def test_checkPersonesStructure_a_request_contains_more_than_one_document_object(host, port, data_person,
                                                                                 data_document,
                                                                                 payload_checkPersonesStructure,
                                                                                 response):
    person = data_person
    person['businessFunctions'][0]['documents'].append(data_document)
    payload = payload_checkPersonesStructure(persones=[person], locationOfPersones='award')
    actualresult = requests.post(f'{host}:{port.eAccess}/command2', json=payload).json()

    assert actualresult == response.success
