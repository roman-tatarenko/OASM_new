import pytest

from credentials import hosts, cacluster, bootstrap_servers


def pytest_addoption(parser):
    """Method for adding custom console parameters"""
    parser.addoption('--host',
                     default='dev',
                     help='host options: "dev", "sandbox", or your own host for local testing')


@pytest.fixture(scope='session')
def host(request):
    """Return the target host
    :param request:
    :return:
    """
    # get host value
    cli_value = request.config.getoption('--host')

    if cli_value == '' or cli_value == 'dev':
        domain = hosts['dev']
    elif cli_value == 'sandbox':
        domain = hosts['sandbox']
    else:
        domain = cli_value
    return domain


@pytest.fixture(scope='session')
def cluster(request):
    from cassandra.auth import PlainTextAuthProvider
    from cassandra.cluster import Cluster

    # get host value
    cli_value = request.config.getoption('--host')

    if cli_value == '' or cli_value == 'dev':
        auth_provider = PlainTextAuthProvider(username=cacluster['dev']['username'],
                                              password=cacluster['dev']['password'])
        cluster = Cluster(cacluster['dev']['cluster'], auth_provider=auth_provider, port=9042)

    elif cli_value == 'sandbox':
        auth_provider = PlainTextAuthProvider(username=cacluster['sandbox']['username'],
                                              password=cacluster['sandbox']['password'])
        cluster = Cluster(cacluster['sandbox']['cluster'], auth_provider=auth_provider, port=9042)

    return cluster


@pytest.fixture(scope='session')
def kafka_bootstrap_servers(request):
    cli_value = request.config.getoption('--host')
    if cli_value == '' or cli_value == 'dev':
        bs = bootstrap_servers['dev']
    return bs


@pytest.fixture(scope='session')
def cassandra_session(cluster):
    session = cluster.connect()
    yield session
    session.shutdown()
