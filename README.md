# CF-UI test framework

## Environment setup
```shell
git clone https://github.com/Hawkular-QE/cf-ui.git
cd cf-ui
./setup.sh
```
### Using Chrome web driver
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

```

