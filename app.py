from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class NeuroBlastBot():
    def __init__(self, chrome_driver : webdriver.Chrome, options = webdriver.ChromeOptions) -> None:
        self.driver = chrome_driver

    def get_base_url(self):
        url = "https://neuroblastomaorgau.altruisticidentity.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dplatform-identity-client%26nonce%3D6eebc1e729560900a3103db60cd668d7e624e7a65b153ffff31a6c0ebf663eaf%26platform%3Df0708f26-0dc0-493a-8842-1b823abd5a01%26redirect_uri%3Dhttps%253A%252F%252Fwww.neuroblastoma.org.au%252Fidp%252Flogin%252Fcallback%252FDefault.aspx%253FreturnUrl%253D%252F%26response_mode%3Dform_post%26response_type%3Dcode%2520id_token%26scope%3Dopenid%2520profile%2520email%2520platformapiaccess%2520offline_access"
        self.driver.get(url=url)
        
    def login(self):
        wait = WebDriverWait(self.driver, timeout=60)

        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")

        wait.until(
            EC.presence_of_element_located((By.ID, "email")),
        ).send_keys(email)

        next_btn = self.driver.find_element(by=By.ID, value="next")
        next_btn.click()

        password_el = wait.until(
            EC.presence_of_element_located((By.ID, "password")),
        )

        password_el.send_keys(password)
        password_el.send_keys("\n")
        
        self.driver.implicitly_wait(5)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/manager/']")),
        )
        self.driver.get("https://www.neuroblastoma.org.au/manager/reports/outputfiles.aspx")

    def scroll_through_options(self):
        wait = WebDriverWait(self.driver, 10)


        # Now interact with the select element

        element = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_ctl00_bodyContent_ContentPlaceHolder_ddlModule')))
        select = Select(element)
        options = [option.text for option in select.options]

        for option_text in options:
            
            # Re-fetching the select element since it goes stale every loop
            select_element = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_bodyContent_ContentPlaceHolder_ddlModule')))
            select = Select(select_element)

            # Selecting each value that the selectboc has availaible.
            select.select_by_visible_text(option_text)

            # This is where the download and processing options will sit
            print(f"Selected option: {option_text}")
            self.set_date_range()



            time.sleep(2)

    def set_date_range(self):
        start_date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        end_date = datetime.now().strftime("%d/%m/%Y")
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpStartDate_txtDate")
            )
        ).clear()
        self.driver.find_element(
            By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpStartDate_txtDate"
        ).send_keys(start_date)

        wait.until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpEndDate_txtDate")
            )
        ).clear()
        self.driver.find_element(
            By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpEndDate_txtDate"
        ).send_keys(end_date)

    def process_downloads(self, option_text):
        
        pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    chrome_driver = webdriver.Chrome()
    chrome_driver.implicitly_wait(60)
    bot = NeuroBlastBot(chrome_driver)
    bot.get_base_url()
    bot.login()
    bot.scroll_through_options()
