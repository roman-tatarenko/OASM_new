import pytest


@pytest.fixture(scope='function')
def payload_findCANIds(request_template, prepared_cpid, prepared_ev_ocid):
    payload = request_template(action='findCANIds')

    def _payload_findCANIds(*args, cpid=prepared_cpid, ocid=prepared_ev_ocid, **kwargs):
        payload['params'] = {
            "cpid": cpid,
            "ocid": ocid,
            "states": [kwargs],
            "lotIds": args
        }
        if not kwargs:
            del payload['params']['states']

        if not args:
            del payload['params']['lotIds']

        return payload

    return _payload_findCANIds
