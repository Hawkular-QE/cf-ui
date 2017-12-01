# CF-UI test framework

## Environment setup
```shell
git clone https://github.com/Hawkular-QE/cf-ui.git
cd cf-ui
sudo ./setup.sh
source .cf-ui/bin/activate
```
## Configuration
```shell
Edit the following property values in the conf/properties.properties file so that they represent the configuration under test:

    MIQ_<...>
    HAWKULAR_<...>
    OPENSHIFT_<...>
    SSH_<...>
    DB_<...>
```
## Validate the Setup / Configuration
```shell
The following test is expected to successful add the Middleware Manager Provider:

python -m pytest tests/framework/test_test.py::test_cfui_test
```
## Using Chrome web driver
Chrome driver is by default installed into .cf-ui directory and it is necessary to set PATH to it so Python Interpreter would know where to find the driver.
```shell
export PATH=$PATH:${PATH_TO_CF_UI}/.cf-ui
```
Click [here](https://sites.google.com/a/chromium.org/chromedriver/home) for Chrome driver official docs

For PyCharm add Environment Variables for test in Run/Debug Configuration. Setting PATH Environment Variable may be buggy for IDE so you can also set path to driver as method attribute in session.py

Example:
```python
driver = webdriver.Chrome("/path/to/.cf-ui/")
```
## Configuration
All configuration on which automation is relied upon should be stored in conf/properties.properties

Properties in conf/properties.properties are overwritten by env variables with same name as in conf/properties.properties or with prefix ```CFUI_```
So we can use framework testcases to prepare MIQ/CFME+HS for manual testcase if needed without changing conf/properties.properties file.  

```
export KEEP_BROWSER_RUNNING=True
export MIQ_HOSTNAME=<your_MIQ_HOSTNAME>
export MIQ_PORT=80

export HAWKULAR_HOSTNAME=<your_HAWKULAR_HOSTNAME>
export HAWKULAR_PORT=80

source .cf-ui/bin/activate
```
