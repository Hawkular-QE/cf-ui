import pytest
from common.session import session
from navigation.navigation import NavigationTree
from tags.tags import tags
from common.db import db

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session


def test_cfui_select(web_session):
    NavigationTree(web_session).jump_to_middleware_providers_view().to_first_details().select_and_click("Monitoring", "Timelines")


def _test_cfui_wrong_tags_select(web_session):
    try:
        NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'EditTags')
    except Exception as e:
        print "Negative test - it works: ", e.message
        #assert "Page does not contain such pattern(s)" in e.message


def _test_cfui_restore_tags(web_session):
    tags(web_session).restore_tags()


def test_cfui_drop_all_tags(web_session):
    #NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    NavigationTree(web_session).jump_to_middleware_providers_view().to_first_details().select_and_click('Policy',
                                                                                                      'Edit Tags')
    tags(web_session).drop_all_tags()


def test_cfui_wrong_drop_tag(web_session):
    NavigationTree(web_session).jump_to_middleware_providers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    t = tags(web_session)
    assert t.drop_tag('Department', 'Engiingghuheuiwh') == "Nothing to delete."


def test_cfui_number_of_tags(web_session):
    t = tags(web_session)
    NavigationTree(web_session).jump_to_middleware_providers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    web_session.logger.info("collect existent tags")
    stored_tags = t.ui_tags()
    print "SAVED TAGS == ", stored_tags
    # TODO: get tags info from db


def _test_cfui_set_multi_tags(web_session):
    tags(web_session)
    #.set_multi_tags_a()


