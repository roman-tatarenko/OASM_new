import hashlib
import os
from dataclasses import dataclass

import pytest
import requests

pytest_plugins = [
    "tests.fixtures.prepared_id",
    "tests.fixtures.prepared_data",
    "tests.fixtures.prepared_kafka",
    "tests.fixtures.clear_table_by_cpid",
    "tests.fixtures.execute_insert_into_table",
    "tests.fixtures.prepared_insert_into_table",
    "tests.fixtures.prepared_payload",
    "tests.fixtures.prepared_select",
    "tests.fixtures.execute_select"
]


@pytest.fixture(scope='session')
def port():
    @dataclass
    class Port:
        """Ports of Docker containers"""
        eQualification: int = 9251
        eEvaluation: int = 9081
        eMDM: int = 9161
        eContracting: int = 9151
        eAccess: int = 9031
        eSubmission: int = 9061
        eRevision: int = 9351
        iStorage: int = 9131
        eNotice: int = 9041

    return Port


@pytest.fixture(scope='session')
def md5():
    # def _md5(file_name):
    #     hash_md5 = hashlib.md5()
    #     with open(file_name, "rb") as f:
    #         for chunk in iter(lambda: f.read(4096), b""):
    #             hash_md5.update(chunk)
    #     return hash_md5.hexdigest()
    def _md5(file_path):
        return hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    return _md5


@pytest.fixture(scope='function')
def response_success(prepared_request_id):
    return {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "success"
    }


@pytest.fixture(scope='function')
def response_error(prepared_request_id):
    return {
        "version": "2.0.0",
        "id": f"{prepared_request_id}",
        "status": "error"
    }


@pytest.fixture(scope='session')
def registering_document(host, port, md5, payload_registered_document):
    def _registering_document(dir_path, file_name):
        file_path = dir_path + file_name
        file_size = os.stat(file_path).st_size
        file_hash = md5(file_path=file_path)
        payload = payload_registered_document(file_name=file_name, hash=file_hash, weight=file_size)
        return requests.post(f'{host}:{port.iStorage}/storage/registration', json=payload).json()

    return _registering_document


@pytest.fixture(scope='session')
def upload_document(host, port, payload_registered_document):
    def _upload_document(dir_path, file_name, doc_id):
        file = {'file': open(dir_path + file_name, 'rb')}
        return requests.post(f'{host}:{port.iStorage}/storage/upload/{doc_id}', files=file).json()

    return _upload_document
