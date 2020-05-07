from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from configparser import ConfigParser

# read Config
configur = ConfigParser()
configur.read('../config.ini')
BASE_URL = str(configur.get('config', 'BASE_URL'))
driver = webdriver.Chrome()
driver.get(BASE_URL)

# login
time.sleep(1)
driver.find_element_by_id("lid").send_keys(
    configur.get('credentials', 'email'))
driver.find_element_by_id("pwd").send_keys(configur.get('credentials', 'pwd'))
driver.find_element_by_id("signin_submit").send_keys(Keys.ENTER)

# HomePage - pop up close // wait for popup to show
loadCheck = WebDriverWait(driver, 200).until(
    EC.visibility_of_element_located((By.ID, 'NEW_DIALOG_CLOSE_MARK'))
)
if loadCheck:
    time.sleep(1)
    loadCheck.click()
    # click pateint
    driver.find_element_by_css_selector(
        ".physician-home-menus > li:nth-child(1)").click()
time.sleep(4)
