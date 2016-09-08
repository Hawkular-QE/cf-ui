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


def _test_cfui_negative_navigate_select(web_session):
    try:
        NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'EditTags')
    except:
        print "Negative test - it works!"


def test_cfui_restore_tags(web_session):
    logger = web_session.logger
    tag_cat = 'Department'
    tag_add = 'Marketing'

    tags_5 = {
            'Department': ['Engineering'],
            'LifeCycle *': ['Fully retire VM and remove from Provider'],
            'Quota - Max Storage *': ['1TB'],
            'Auto Approve - Max VM *': ['5'],
            'Auto Approve - Max Memory *': ['8GB']
        }
    t = tags(web_session)

    nav = NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    web_session.logger.info("collect existent tags")
    #stored_tags = t.ui_tags()
    stored_tags = tags_5
    print "STORED TAGS == ", stored_tags
    #t.set_tag(tag_cat, tag_add)

    logger.info("drop all tags")
    t.drop_all_tags()

    logger.info("restoring saved tags")
    for tag_key in stored_tags.keys():
        for tag_value in stored_tags[tag_key]:
            print "Restore (", tag_key, " - ", tag_value, ")"
            nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
            t.set_tag(tag_key, tag_value)


def _test_cfui_drop_tag(web_session, tag_cat, tag_add):
    NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')\
        .drop_tag(tag_cat, tag_add)


def _test_cfui_drop_all_tags(web_session):
    NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    tags(web_session).drop_all_tags()


def _test_cfui_wrong_drop_tag(web_session):
    try:
        NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags').drop_tag('Department', 'Engiingghuheuiwh')
    except:
        print "Negative test (wrong drop of tag) - it works!"


def _test_cfui_number_of_tags(web_session):
    t = tags(web_session)
    NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

    web_session.logger.info("collect existent tags")
    stored_tags = t.ui_tags()
    print "SAVED TAGS == ", stored_tags
    # TODO: get tags info from db


def test_cfui_set_multi_tags(web_session):
    logger = web_session.logger
    logger.info("Begin set_few_tags test")

    tags_2 = {'Department': ['Engineering', 'Marketing']}
    tags_5 = {
        'Department': ['Engineering'],
        'LifeCycle *': ['Fully retire VM and remove from Provider'],
        'Quota - Max Storage *': ['1TB'],
        'Auto Approve - Max VM *': ['5'],
        'Auto Approve - Max Memory *': ['8GB']
    }

    tag_dict = tags_5
    t = tags(web_session)
    nav = NavigationTree(web_session).jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

    web_session.logger.info("collect existent tags")
    stored_tags = t.ui_tags()
    print "SAVED TAGS == ", stored_tags

    logger.info("Starting to set given tags")
    for tag_key in tag_dict.keys():
        for tag_value in tag_dict[tag_key]:
            web_session.logger.info( " - Set tag: ({} -> {})".format(tag_key, tag_value))
            nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
            t.set_tag(tag_key, tag_value)

    logger.info(" == drop all tags == ")
    nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
    t.drop_all_tags()

    logger.info("restoring saved tags")
    nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')

    print "TAGS TO BE RESTORED: ", stored_tags
    for tag_key in stored_tags.keys():
        for tag_value in stored_tags[tag_key]:
            print "Restore (", tag_key, " - ", tag_value, ")"
            nav.jump_to_middleware_servers_view().to_first_details().select_and_click('Policy', 'Edit Tags')
            t.set_tag(tag_key, tag_value)


