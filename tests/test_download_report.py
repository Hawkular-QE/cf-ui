import pytest
from common.session import session
from common.download_report import download_report
import os
import glob
import fnmatch
from common.ui_utils import ui_utils
from common.view import view

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    r = glob.glob("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware*'))
    r.extend(glob.glob("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers*')))

    for i in r:
        os.remove(i)

    request.addfinalizer(closeSession)

    return web_session

def test_cfui_providers_download_txt(web_session):
    web_session.web_driver.get("{}//ems_middleware/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download provider report as text test")
    assert download_report(web_session,"ems_middleware").text_format()

    web_session.logger.info("Begin download provider report as cvv test")
    assert download_report(web_session,"ems_middleware").csv_format()

    web_session.logger.info("Begin provider file assert")

    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Provider*')
    r = glob.glob(file)

    assert fnmatch.filter(r,'*.txt')
    assert fnmatch.filter(r,'*.csv')


def test_cfui_domain_download_txt(web_session):
    web_session.web_driver.get("{}/middleware_domain/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download domain report as text test")
    assert download_report(web_session,"middleware_domain").text_format()

    web_session.logger.info("Begin download domain report as cvv test")
    assert download_report(web_session,"middleware_domain").csv_format()

    web_session.logger.info("Begin provider file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Domain*')
    r = glob.glob(file)

    assert fnmatch.filter(r, '*.txt')
    assert fnmatch.filter(r, '*.csv')

def test_cfui_server_download_txt(web_session):
    web_session.web_driver.get("{}//middleware_server/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download server report as text test")
    assert download_report(web_session,"middleware_server").text_format()

    web_session.logger.info("Begin download server report as cvv test")
    assert download_report(web_session,"middleware_server").csv_format()

    web_session.logger.info("Begin server file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Servers*')
    r = glob.glob(file)
    assert fnmatch.filter(r, '*.txt')
    assert fnmatch.filter(r, '*.csv')


def test_cfui_datasource_download_txt(web_session):
    web_session.web_driver.get("{}/middleware_datasource/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download datasource report as text test")
    assert download_report(web_session,"middleware_datasource").text_format()

    web_session.logger.info("Begin download datasource report as cvv test")
    assert download_report(web_session,"middleware_datasource").csv_format()

    web_session.logger.info("Begin datasource file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Datasources*')
    r = glob.glob(file)
    assert fnmatch.filter(r, '*.txt')
    assert fnmatch.filter(r, '*.csv')


def test_cfui_deployment_download_txt(web_session):
    web_session.web_driver.get("{}/middleware_deployment/show_list".format(web_session.MIQ_URL))
    web_session.logger.info("Begin download deployment report as text test")
    assert download_report(web_session,"middleware_deployment").text_format()

    web_session.logger.info("Begin download deployment report as cvv test")
    assert download_report(web_session,"middleware_deployment").csv_format()

    web_session.logger.info("Begin deployment file assert")
    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Deployments*')
    r = glob.glob(file)
    assert fnmatch.filter(r, '*.txt')
    assert fnmatch.filter(r, '*.csv')

def test_cfui_provider_detail_pdf(web_session):
    web_session.logger.info("Begin download provider detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}//ems_middleware/show_list".format(web_session.MIQ_URL))
    view(web_session).list_View()
    utils.sleep(2)
    utils.click_on_row_containing_text(web_session.HAWKULAR_PROVIDER_NAME)
    utils.waitForTextOnPage('Status', 10)

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/ManageIQ-Providers-Hawkular-Middleware*'))

def test_cfui_domain_detail_download_pdf(web_session):
    web_session.logger.info("Begin download Domain detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_domain/show_list".format(web_session.MIQ_URL))
    domains = utils.get_list_table()
    utils.click_on_row_containing_text(domains[0].get('Feed'))

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Domain*'))

def test_cfui_server_detail_download_pdf(web_session):
    web_session.logger.info("Begin download Server detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_server/show_list".format(web_session.MIQ_URL))
    servers = utils.get_list_table()
    utils.click_on_row_containing_text(servers[0].get('Feed'))

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Server*'))

def test_cfui_deployment_detail_download_pdf(web_session):
    web_session.logger.info("Begin download Deployment detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_deployment/show_list".format(web_session.MIQ_URL))
    servers = utils.get_list_table()
    utils.click_on_row_containing_text(servers[0].get('Deployment Name'))

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Deployment*'))

def test_cfui_datasource_detail_download_pdf(web_session):
    web_session.logger.info("Begin download Datasource detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_datasource/show_list".format(web_session.MIQ_URL))
    servers = utils.get_list_table()
    utils.click_on_row_containing_text(servers[0].get('Datasource Name'))

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Datasource*'))

def test_cfui_messaging_detail_download_pdf(web_session):
    web_session.logger.info("Begin download Messaging detail PDF text")
    utils = ui_utils(web_session)
    web_session.web_driver.get("{}/middleware_messaging/show_list".format(web_session.MIQ_URL))
    servers = utils.get_list_table()
    utils.click_on_row_containing_text(servers[0].get('Messaging Name'))

    assert download_report(web_session, '').pdf_format()

    assert_pdf_download_exist("{}{}".format(os.getenv("HOME"), '/Downloads/Middleware Messaging*'))

def assert_pdf_download_exist(file):
    r = glob.glob(file)
    assert fnmatch.filter(r, '*.pdf')