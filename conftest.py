import pytest
import toml
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

config = toml.load('config.toml')


def pytest_addoption(parser):
    """Method for adding custom console parameters"""
    parser.addoption(
        '--env',
        default='dev',
        help='environment options: "dev", "sandbox",'
             ' or your own host for testing'
    )


@pytest.fixture(scope='session')
def host(request):
    """Return the target host"""
    cli_value = request.config.getoption('--env')

    if cli_value == 'dev':
        domain = config['development']['host']
    elif cli_value == 'sandbox':
        domain = config['sandbox']['host']
    else:
        domain = cli_value
    return domain


@pytest.fixture(scope='session')
def cluster(request):
    cli_value = request.config.getoption('--env')

    if cli_value == 'dev':
        auth_provider = PlainTextAuthProvider(
            username=config['development']['cassandra']['username'],
            password=config['development']['cassandra']['password']
        )
        cluster = Cluster(
            config['development']['cassandra']['cluster'],
            auth_provider=auth_provider,
            port=9042
        )

    elif cli_value == 'sandbox':
        auth_provider = PlainTextAuthProvider(
            username=config['sandbox']['cassandra']['username'],
            password=config['sandbox']['cassandra']['password']
        )
        cluster = Cluster(
            config['sandbox']['cassandra']['cluster'],
            auth_provider=auth_provider,
            port=9042
        )

    return cluster


@pytest.fixture(scope='session')
def kafka_bootstrap_servers(request):
    cli_value = request.config.getoption('--env')
    if cli_value == '' or cli_value == 'dev':
        bs = config['development']['botstrap_servers']
    return bs


@pytest.yield_fixture(scope='session')
def cassandra_session(cluster):
    session = cluster.connect()
    yield session
    session.shutdown()
