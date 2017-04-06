import pytest
from common.session import session
from views.server_group_deployment import server_group_deploymnt

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)
    web_session.logger.info("HAWKULARQE-37- Server Group Deployment")


    return web_session

def test_server_deployment(web_session):
    web_session.logger.info("Begin server group deployment test")
    assert server_group_deploymnt(web_session).add_deployment()