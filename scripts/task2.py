from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
from configparser import ConfigParser

# read Config
configur = ConfigParser()
configur.read('../config.ini')
BASE_URL = str(configur.get('config', 'BASE_URL'))
# read data from file
try:
    with open("../data.json") as f:
        data = json.load(f)
except:
    print("No Data Found")

driver = webdriver.Chrome()
driver.get(BASE_URL)
driver.maximize_window()
driver.implicitly_wait(35)
# SIGN IN
driver.find_element_by_id("lid").send_keys(
    configur.get('credentials', 'email'))
driver.find_element_by_id("pwd").send_keys(configur.get('credentials', 'pwd'))
driver.find_element_by_id("signin_submit").send_keys(Keys.ENTER)
# VERification


# HomePage - pop up close // wait for popup to show
loadCheck = WebDriverWait(driver, 200).until(
    EC.visibility_of_element_located((By.ID, 'NEW_DIALOG_CLOSE_MARK'))
)
if loadCheck:
    time.sleep(1)
    loadCheck.click()
    # click chart notes
    driver.find_element_by_css_selector(
        ".physician-home-menus > li:nth-child(3)").click()
time.sleep(2)

# click encouter / create patient
loadCheck = WebDriverWait(driver, 200).until(
    EC.invisibility_of_element((By.ID, 'mainLoading'))
)
if loadCheck:
    driver.find_element_by_id("newEncButDiv").click()
    time.sleep(2)
    driver.find_element_by_id(
        "SEARCH_PATIENT_FOR_ENCOUNTER").send_keys(data["name"])
    time.sleep(2)
    driver.find_element_by_id(
        "SEARCH_PATIENT_FOR_ENCOUNTER").send_keys(Keys.ENTER)
time.sleep(1)
driver.find_element_by_css_selector("button.v1-pmy-btn:nth-child(3)").click()
time.sleep(6)


# click history
driver.find_element_by_id("encounterTab_2").click()
time.sleep(2)
WebDriverWait(driver, 300).until(EC.frame_to_be_available_and_switch_to_it(
    (By.CLASS_NAME, 'ze_area')))
driver.find_element_by_css_selector(".ze_body > div").send_keys(
    data["History of Present Illness"])
driver.switch_to.default_content()


# physical examination
driver.find_element_by_id("encounterTab_3").click()
time.sleep(2)
driver.find_element_by_css_selector(
    "#PE_VIEW > div > table > tbody > tr > td > div.v1-chartnote-link > div:nth-child(1)").click()
time.sleep(3)
# select Template
try:
    driver.find_element_by_xpath(
        "//*[@id='lftContainer']/ul/ul[1]/li[contains(.,'{}')]".format(data["Physical Examination"]["Template"])).click()
except:
    driver.find_element_by_xpath(
        "//*[@id='lftContainer']/ul/ul[2]/li[contains(.,'{}')]".format(data["Physical Examination"]["Template"])).click()
# checkboxes
time.sleep(1)
for c in data["Physical Examination"]["Checkboxes"]:
    for i, ac in enumerate(c):
        driver.find_element_by_css_selector(
            "input[type='checkbox'][value='{}']".format(">>"*i + ac)).click()
        time.sleep(1)
# values
if data["Physical Examination"]["Values"]:
    tempData = data["Physical Examination"]["Values"]
    for key in tempData:
        driver.find_element_by_xpath(
            "//*[@id='ENTRY_NAME'][contains(.,'{}')]/../div[2]/input".format(key)).send_keys(tempData[key])
    time.sleep(1)
# Close
driver.find_element_by_css_selector(
    '#tDialogContent > div > div.ButtComDiv > button.v2-pmy-btn').click()
time.sleep(1)

#
# diagonisis
driver.find_element_by_id("encounterTab_6").click()
time.sleep(1)
driver.find_element_by_css_selector(
    '#encounterPart_6 > div > table > tbody > tr > td > div.cmflt > div.v1-chartnote-link > div:nth-child(3)').click()
time.sleep(1)
for index, dg in enumerate(data["Diagnoses"]):
    if(index+1 > 3):
        driver.find_element_by_css_selector(
            "#_DIALOG_CONTENT > div > div.wdfl.pt > div").click()
        time.sleep(1)
    driver.find_element_by_xpath(
        "//*[@id='itemListDiv']/div[{}]/div/div[1]/input".format(index+1)).send_keys(dg["Diagnosis"])
    time.sleep(3)
    driver.find_element_by_xpath(
        "//*[@id='itemListDiv']/div[{}]/div/div[1]/input".format(index+1)).send_keys(Keys.ENTER)
    time.sleep(1)
driver.find_element_by_css_selector(
    "#_DIALOG_CONTENT > div > div.wdfl.pt > .v2-pmy-btn").click()

# Return and Repeat
time.sleep(2)
driver.find_element_by_id("saveContentDiv").click()
time.sleep(2)
driver.find_element_by_id("MEMBER_TAB_ID_2").click()
time.sleep(3)
