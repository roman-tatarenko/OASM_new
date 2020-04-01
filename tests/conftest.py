from dataclasses import dataclass

import pytest

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

    return Port
