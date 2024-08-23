from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import glob
from airtable_helper.upsert import upsert_csv_to_airtable

class NeuroBlastBot():
    def __init__(self, chrome_driver : webdriver.Chrome, options = webdriver.ChromeOptions) -> None:
        self.download_dir = os.path.join(os.getcwd(), 'csv_reports')
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
        print("Total Options : ", len(options), "Options are : ", options)
        for option_text in options[1:]:
            select_element = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_bodyContent_ContentPlaceHolder_ddlModule')))
            select = Select(select_element)
            select.select_by_visible_text(option_text)
            print(f"Selected option: {option_text}")
            date_passed = self.set_date_range()
            if date_passed:
                print(f'{option_text} is a Date Passable element')

            self.process_downloads()
            self.handle_new_file(f"{option_text}.csv")
            time.sleep(2)

    def set_date_range(self):
        start_date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        end_date = datetime.now().strftime("%d/%m/%Y")
        try:
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

            head_element = self.driver.find_element(By.CSS_SELECTOR, "#managerContent > div.managerPage > h1")
            head_element.click()

            return True
        except TimeoutException:
            return False

    def process_downloads(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(
        EC.presence_of_element_located(
            (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_lnkbtnDownload")
        )
        ).click()
        pass

    def process_csv_files(self):
        # List to store CSV file paths
        csv_files = []
        csv_reports_directory = os.path.join(os.getcwd(), 'csv_reports')
        # Walk through the directory
        for root, dirs, files in os.walk(csv_reports_directory):
            for file in files:
                if file.endswith(".csv"):
                    # Get the full file path
                    file_path = os.path.join(root, file)
                    csv_files.append(file_path)
        
        # Loop over each CSV file and perform your processing
        for csv_file in csv_files:
            upsert_csv_to_airtable(csv_file_path=csv_file)
            # Call your function to process each CSV file
            # For example: upsert_csv_to_airtable(csv_file, airtable_base_id, api_key, primary_key)
        
        return csv_files
    
    def empty_csv_reports_directory(self):
        # Use glob to find all .csv files in the directory
        csv_reports_directory = os.path.join(os.getcwd(), 'csv_reports')
        csv_files = glob.glob(os.path.join(csv_reports_directory, "*.csv"))
        
        # Loop over each file and remove it
        for csv_file in csv_files:
            try:
                os.remove(csv_file)
                print(f"Deleted file: {csv_file}")
            except OSError as e:
                print(f"Error deleting file {csv_file}: {e}")
    def handle_new_file(self,new_filename):
        latest_file = None
        while latest_file is None:
            time.sleep(2)  
            list_of_files = glob.glob(os.path.join(self.download_dir, '*'))
            latest_file = max(list_of_files, key=os.path.getctime) if list_of_files else None

        # Perform the desired action with the new file
        

        # Rename the new file
        new_file_path = os.path.join(self.download_dir, new_filename)
        os.rename(latest_file, new_file_path)

        return new_file_path

if __name__ == "__main__":
    download_dir = os.path.join(os.getcwd(), 'csv_reports')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Set the default download directory
        "download.prompt_for_download": False,       # Disable download prompt
        "download.directory_upgrade": True,          # Allow directory upgrade
        "safebrowsing.enabled": True                 # Enable safe browsing
    })

    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.implicitly_wait(60)
    bot = NeuroBlastBot(chrome_driver)
    # bot.get_base_url()
    # bot.login()
    # bot.empty_csv_reports_directory()
    # bot.scroll_through_options()    
    bot.process_csv_files()
