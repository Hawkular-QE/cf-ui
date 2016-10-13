import pytest
from common.session import session
from views.messagings import messagings

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
        request.addfinalizer(closeSession)

    return web_session

def _test_cfui_validate_messagings_view(web_session):
    web_session.logger.info("Begin validate Messagings View")
    assert messagings(web_session).validate_messagings_view()


def _test_cfui_message_details(web_session):
    web_session.logger.info("Begin validate Message Details")
    assert messagings(web_session).validate_messageing_details()

def test_cfui_validate_eap_jms_queues(web_session):
    web_session.logger.info("Begin validate EAP JMS Queues (INV-011a).")
    assert messagings(web_session).validate_eap_jms_queues()