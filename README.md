# CF-UI test framework

## Environment setup
```shell
git clone https://github.com/Hawkular-QE/cf-ui.git
cd cf-ui
virtualenv .cf-ui
source .cf-ui/bin/activate
pip install -r requirements.txt
```
### Using Chrome web driver
For using Chrome web driver you have to uncomment ```# chromedriver``` line in requirements.txt before its installation
or run ```pip install chromedriver``` afterwards (in Virtual Environment). This will install chrome driver default location is .cf-ui directory and it is necessary to set PATH to it so Python Interpreter would know where to find the driver.
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
All configuration on which automation should relied should be stored in conf/properties.properties

## Navigation:
Usage of Navigation Tree:
'''
tree = NavigationTree(<web_session instance>) 
Not WebDriver instance
web_session instance as fixture
'''

