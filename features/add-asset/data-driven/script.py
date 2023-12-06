import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from rich.panel import Panel
from rich import print

import unittest
import sys
import os
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "http://localhost:3000/login"
FEATURE_URL = "http://localhost:3000/view-asset"
USERNAME = "ngocngo"
PASSWORD = "ngocngo"
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


class Helper():
    @staticmethod
    def AddAsset(ctx, aname: str, adepartment: str, atype: str, astatus: str, adescription: str, anote: str, expected):
        driver = ctx.driver
        
        select_department = driver.find_element(By.ID, "department-select")
        
        driver.find_element(By.ID, "btn-add-asset").click()
        
        # ActionChains(driver).move_to_element(select_department).click()
        # time.sleep(10000)
        
        # ActionChains(driver).move_to_element(department_select).click()
        
        name = driver.find_element(By.ID, "control-ref_name")
        name.send_keys(aname)
        
        department = driver.find_element(By.ID, "control-ref_department_id")
        department.click()
        time.sleep(1)
        department.send_keys(Keys.ENTER)
        
        type = driver.find_element(By.ID, "control-ref_type")
        type.send_keys(atype)
        
        status = driver.find_element(By.ID, "control-ref_status")
        status.send_keys(astatus)
        
        description = driver.find_element(By.ID, "control-ref_description")
        description.send_keys(adescription)
        
        note = driver.find_element(By.ID, "control-ref_status_note")
        note.send_keys(anote)
        
        driver.find_element(By.ID, "submit-add-asset").click()
        
        time.sleep(1)
        
        
class TestDrive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """setUpClass runs once per class.
        This is where you set up the driver and log in
        """
        # Set up the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(10)

        cls.driver = driver
        cls.logger = logger
        
        # Login
        driver.get(LOGIN_URL)
        
        username = driver.find_element(By.ID, "basic_username")
        password = driver.find_element(By.ID, "basic_password")
        login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        ActionChains(driver).move_to_element(username).click().send_keys(
            USERNAME
        ).move_to_element(password).click().send_keys(PASSWORD).move_to_element(
            login
        ).click().perform()
        time.sleep(1)
        
        driver.get(FEATURE_URL)
        # if login failed, exit
        if "Department Name" not in driver.page_source:
            driver.quit()
            LOGIN_ERR = Panel(
                f"""
            Login failed. Please check your credentials and try again.
            - username: {USERNAME}
            - password: {PASSWORD}
            """,
                title="Login Error",
                title_align="left",
                expand=True,
                style="red",
            )
            print(LOGIN_ERR)
            sys.exit(1)

    def setUp(self):
        """setUp runs before each test case run.
        This is where you set up any data needed for the tests.
        """
        pass
        

    # TEST CASES
    def test_drive(self):
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    Helper.AddAsset(self, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    print("called helper")
                except:
                    print("there're some errors")
                finally: continue


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)