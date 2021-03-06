import pytest
from common.session import session
from common.download_report import download_report
import os
import glob
import fnmatch
from common.view import view
from views.domains import domains
from common.timeout import timeout
import time
from common.navigate import navigate
from common.ui_utils import ui_utils
from common.db import db

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session

@pytest.fixture
def delete_files():
    r = glob.glob("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware*'))
    r.extend(glob.glob("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers*')))

    for i in r:
        os.remove(i)

    return

def test_cfui_providers_download_txt(web_session, delete_files):
    web_session.web_driver.get("{}/ems_middleware/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download provider report as text test")
    assert download_report(web_session,"ems_middleware").text_format()

    web_session.logger.info("Begin download provider report as cvv test")
    assert download_report(web_session,"ems_middleware").csv_format()

    web_session.logger.info("Begin provider file assert")

    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Provider*')
    assert_download_exist("{}.txt".format(file))
    assert_download_exist("{}.csv".format(file))

def test_cfui_domain_download_txt(web_session, delete_files):
    web_session.web_driver.get("{}/middleware_domain/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download domain report as text test")
    assert download_report(web_session,"middleware_domain").text_format()

    web_session.logger.info("Begin download domain report as cvv test")
    assert download_report(web_session,"middleware_domain").csv_format()

    web_session.logger.info("Begin provider file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Domain*')
    assert_download_exist("{}.txt".format(file))
    assert_download_exist("{}.csv".format(file))

def test_cfui_server_download_txt(web_session, delete_files):
    web_session.web_driver.get("{}//middleware_server/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download server report as text test")
    assert download_report(web_session,"middleware_server").text_format()

    web_session.logger.info("Begin download server report as cvv test")
    assert download_report(web_session,"middleware_server").csv_format()

    web_session.logger.info("Begin server file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Servers*')
    assert_download_exist("{}.txt".format(file))
    assert_download_exist("{}.csv".format(file))


def test_cfui_datasource_download_txt(web_session, delete_files):
    web_session.web_driver.get("{}/middleware_datasource/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download datasource report as text test")
    assert download_report(web_session,"middleware_datasource").text_format()

    web_session.logger.info("Begin download datasource report as cvv test")
    assert download_report(web_session,"middleware_datasource").csv_format()

    web_session.logger.info("Begin datasource file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Datasources*')
    assert_download_exist("{}.txt".format(file))
    assert_download_exist("{}.csv".format(file))


def test_cfui_deployment_download_txt(web_session, delete_files):
    web_session.web_driver.get("{}/middleware_deployment/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download deployment report as text test")
    assert download_report(web_session,"middleware_deployment").text_format()

    web_session.logger.info("Begin download deployment report as cvv test")
    assert download_report(web_session,"middleware_deployment").csv_format()

    web_session.logger.info("Begin deployment file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Deployments*')
    assert_download_exist("{}.txt".format(file))
    assert_download_exist("{}.csv".format(file))

def test_cfui_provider_detail_pdf(web_session, delete_files):
    if web_session.appliance_version == 'master':
        web_session.logger.debug("Download feature not supported for Provider Detail.")
        pytest.skip("Skip test - Download feature not supported for Provider Detail - version: master.")

    web_session.logger.info("Begin download provider detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}//ems_middleware/show_list".format(web_session.MIQ_URL))
    view(web_session).list_View()
    utils.sleep(2)
    utils.click_on_row_containing_text(web_session.HAWKULAR_PROVIDER_NAME)
    utils.waitForTextOnPage('Status', 10)

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware*.pdf'))

def test_cfui_domain_detail_download_pdf(web_session, delete_files):
    web_session.logger.info("Begin download Domain detail PDF text")
    utils = ui_utils(web_session)
    provider_name = web_session.HAWKULAR_PROVIDER_NAME
    navigate(web_session).get("{}/middleware_domain/show_list".format(web_session.MIQ_URL))
    utils.sleep(1)
    domains = db(web_session).get_domains()
    if not domains:
        web_session.logger.warning("No Domains found.")
        pytest.skip("Skip test - No Domains found.")
    assert utils.waitForTextOnPage(provider_name, 15)

    utils.click_on_row_containing_text(domains[0].get('feed'))
    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware Manager-Middleware Domain*.pdf'))

def test_cfui_server_detail_download_pdf(web_session, delete_files):
    if web_session.appliance_version == 'master':
        web_session.logger.debug("Download feature not supported for Server Detail.")
        pytest.skip("Skip test - Download feature not supported for Server Detail - version: master.")

    web_session.logger.info("Begin download Server detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_server/show_list".format(web_session.MIQ_URL))
    assert utils.waitForTextOnPage(web_session.HAWKULAR_PROVIDER_NAME, 10)
    servers = utils.get_list_table()
    utils.click_on_row_containing_text(servers[0].get('Feed'))

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Server*.pdf'))

def test_cfui_deployment_detail_download_pdf(web_session, delete_files):
    if web_session.appliance_version == 'master':
        web_session.logger.debug("Download feature not supported for Deloyment Detail.")
        pytest.skip("Skip test - Download feature not supported for Deloyment Detail - version: master.")

    web_session.logger.info("Begin download Deployment detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_deployment/show_list".format(web_session.MIQ_URL))
    assert utils.waitForTextOnPage("Deployment Name", 10)
    deployments = utils.get_list_table()
    utils.click_on_row_containing_text(deployments[0].get('Deployment Name'))

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware Manager-Middleware Deployment*.pdf'))

def test_cfui_datasource_detail_download_pdf(web_session, delete_files):
    if web_session.appliance_version == 'master':
        web_session.logger.debug("Download feature not supported for Datasource Detail.")
        pytest.skip("Skip test - Download feature not supported for Datasource Detail - version: master.")

    web_session.logger.info("Begin download Datasource detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_datasource/show_list".format(web_session.MIQ_URL))
    assert utils.waitForTextOnPage("Datasource Name", 10)
    datasources = utils.get_list_table()
    utils.click_on_row_containing_text(datasources[0].get('Datasource Name'))

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware Manager-Middleware Datasource_Datasource*.pdf'))

def test_cfui_messaging_detail_download_pdf(web_session, delete_files):
    if web_session.appliance_version == 'master':
        web_session.logger.debug("Download feature not supported for Messaging Detail.")
        pytest.skip("Skip test - Download feature not supported for Messaging Detail - version: master")

    web_session.logger.info("Begin download Messaging detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_messaging/show_list".format(web_session.MIQ_URL))
    assert utils.waitForTextOnPage("Messaging Name", 10)
    messagings = utils.get_list_table()
    utils.click_on_row_containing_text(messagings[0].get('Messaging Name'))

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware Manager-Middleware Messaging*.pdf'))

def test_cfui_server_groups(web_session, delete_files):
    web_session.logger.info("Begin download Server Groups PDF text")
    nav_to_server_groups(web_session)
    utils = ui_utils(web_session)
    utils.web_driver.find_element_by_xpath('.//*[@title="Download"]').click()
    el = web_session.web_driver.find_element_by_id("download_choice__download_pdf")
    assert utils.wait_until_element_displayed(el, 10)
    el.click()
    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Server Groups*.pdf'))

def test_cfui_server_groups_detail(web_session, delete_files):
    web_session.logger.info("Begin download Server Groups Detail PDF text")
    utils = ui_utils(web_session)

    nav_to_server_groups(web_session)
    servers = utils.get_list_table()

    utils.click_on_row_containing_text(servers[0].get('Server Group Name'))
    utils.waitForTextOnPage("Properties", 5)

    assert download_report(web_session, '').pdf_format()

    assert_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware Manager-Middleware Server Group*.pdf'))


def assert_download_exist(file, waitTime = 15):
    with timeout(waitTime, error_message="Timed out waiting for Download file: {}".format(file)):
        while True:
            r = glob.glob(file)
            if fnmatch.filter(r, file):
                break;

            time.sleep(1)

def nav_to_server_groups(web_session):
    utils = ui_utils(web_session)
    navigate(web_session).get("{}/middleware_domain/show_list".format(web_session.MIQ_URL), wait_for='Middleware Domains')
    utils.sleep(3)
    domains_ui = ui_utils(web_session).get_list_table()
    if not domains_ui:
        web_session.logger.warning("No Domains found.")
        pytest.skip("Skip test - No Domains found.")

    domains(web_session).nav_to_all_middleware_server_groups(domains_ui[0].get('Domain Name'))