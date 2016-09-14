import pytest
from common.session import session
from common.download_report import download_report
from navigation.navigation import NavigationTree
import os
import glob
import fnmatch



@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    file = "{}{}".format(os.getenv("HOME"), '/Downloads/Middleware*')
    r = glob.glob(file)
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