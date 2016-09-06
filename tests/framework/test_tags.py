import pytest
from common.session import session
from navigation.navigation import NavigationTree
from tags.tags import tags
from time import sleep

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=False)

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session


def _test_cfui_select(web_session):
    NavigationTree(web_session).jump_to_middleware_providers_view().to_first_details().select_and_click("Monitoring", "Timelines")
    sleep(1)


def _test_cfui_negative_navigate_select(web_session):
    try:
        NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'EditTags')
    except:
        print "Negative test - it works!"

def _test_cfui_set_tag(web_session):

    tag_cat = 'Department'
    tag_add = 'Marketing'

    t = tags(web_session)

    nav = NavigationTree(web_session).jump_to_middleware_servers_view()\
        .to_first_details()\
        .select_and_click('Policy', 'Edit Tags')\
        .hold_on(5)
    web_session.logger.info("collect existent tags")
    stored_tags = t.ui_tags()
    print "STORED TAGS == ", stored_tags

    t.set_tag(tag_cat, tag_add)
    t.drop_all_tags()

    # restoring saved tags
    web_session.logger.info("restoring saved tags")
    nav.jump_to_middleware_servers_view()\
        .to_first_details()\
        .select_and_click('Policy', 'Edit Tags')

    for tag_key in stored_tags.keys():
        for tag_value in stored_tags[tag_key]:
            print "Restore (", tag_key, " - ", tag_value, ")"
            t.set_tag(tag_key, tag_value)


def _test_cfui_drop_tag(web_session, tag_cat, tag_add):
    NavigationTree(web_session).jump_to_middleware_servers_view().\
        to_first_details()\
        .select_and_click('Policy', 'Edit Tags')\
        .hold_on(5)\
        .drop_tag(tag_cat, tag_add)
    #sleep(1)


def test_cfui_drop_all_tags(web_session):
    NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    tags(web_session).drop_all_tags()


def _test_cfui_wrong_drop_tag(web_session):
    try:
        NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags').hold_on(5).drop_tag('Department', 'Engiingghuheuiwh')
    except:
        print "Negative test (wrong drop of tag) - it works!"


def _test_cfui_set_few_tags(web_session):
    logger = web_session.logger
    logger.info("Begin set_few_tags test")

    tag_dict = {'Department': ['Engineering', 'Marketing']}
    t = tags(web_session)
    nav = NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

    web_session.logger.info("collect existent tags")
    stored_tags = t.ui_tags()
    print "STORED TAGS == ", stored_tags

    logger.info("Starting to set given tags")
    for tag_key in tag_dict.keys():
        for tag_value in tag_dict[tag_key]:
            web_session.logger.info( " - Set tag: ({} -> {})".format(tag_key, tag_value))
            t.set_tag(tag_key, tag_value)


    # removing all tags
    logger.info(" == drop all tags == ")
    t.drop_all_tags()

    # restoring saved tags
    logger.info("restoring saved tags")
    nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

    for tag_key in stored_tags.keys():
        for tag_value in stored_tags[tag_key]:
            print "Restore (", tag_key, " - ", tag_value, ")"
            t.set_tag(tag_key, tag_value)
