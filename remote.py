from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=800,600")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Remote(
        command_executor='http://localhost:4444',
   desired_capabilities=DesiredCapabilities.CHROME,
   options=options)

driver.get("https://google.com")

