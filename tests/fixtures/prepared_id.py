import random
import time
from uuid import uuid4

import pytest


@pytest.fixture(scope='function')
def prepared_cpid():
    cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return cp_id


@pytest.fixture(scope='function')
def prepared_ocid():
    oc_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return oc_id


@pytest.fixture(scope='function')
def prepared_ev_ocid(prepared_cpid):
    oc_id = f"{prepared_cpid}-EV-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return oc_id


@pytest.fixture(scope='function')
def prepared_ac_ocid(prepared_cpid):
    oc_id = f"{prepared_cpid}-AC-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return oc_id


@pytest.fixture(scope='function')
def prepared_ac_id(prepared_ac_ocid):
    ac_id = prepared_ac_ocid + str(int(time.time()) * 1000 + random.randint(1, 100))
    return ac_id


@pytest.fixture(scope='function')
def prepared_ev_id(prepared_ev_ocid):
    ev_id = prepared_ev_ocid + str(int(time.time()) * 1000 + random.randint(1, 100))
    return ev_id


@pytest.fixture(scope='function')
def prepared_release_id(prepared_ocid):
    release_id = f"{prepared_ocid}+{int(time.time()) * 1000 + random.randint(1, 100)}"
    return release_id


@pytest.fixture(scope='function')
def prepared_request_id():
    return uuid4()


@pytest.fixture(scope='function')
def prepared_operation_id():
    return uuid4()


@pytest.fixture(scope='function')
def prepared_token_entity():
    return uuid4()


@pytest.fixture(scope='function')
def prepared_entity_id():
    def _prepared_entity_id():
        return uuid4()

    return _prepared_entity_id


@pytest.fixture(scope='function')
def prepared_owner():
    return '3fa85f64-5717-4562-b3fc-2c963f66afa6'
