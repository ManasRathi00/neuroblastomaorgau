from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select


chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=chrome_options)
url = "https://neuroblastomaorgau.altruisticidentity.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dplatform-identity-client%26nonce%3D6eebc1e729560900a3103db60cd668d7e624e7a65b153ffff31a6c0ebf663eaf%26platform%3Df0708f26-0dc0-493a-8842-1b823abd5a01%26redirect_uri%3Dhttps%253A%252F%252Fwww.neuroblastoma.org.au%252Fidp%252Flogin%252Fcallback%252FDefault.aspx%253FreturnUrl%253D%252F%26response_mode%3Dform_post%26response_type%3Dcode%2520id_token%26scope%3Dopenid%2520profile%2520email%2520platformapiaccess%2520offline_access"
driver.get(url)
driver.implicitly_wait(60)

wait = WebDriverWait(driver, timeout=60)

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

wait.until(
    EC.presence_of_element_located((By.ID, "email")),
).send_keys(email)

next_btn = driver.find_element(by=By.ID, value="next")
next_btn.click()

password_el = wait.until(
    EC.presence_of_element_located((By.ID, "password")),
)

password_el.send_keys(password)
password_el.send_keys("\n")

driver.implicitly_wait(5)
wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='/manager/']")),
)

driver.get("https://www.neuroblastoma.org.au/manager/reports/outputfiles.aspx")
# time.sleep(60)
wait = WebDriverWait(driver, 10)


# Now interact with the select element

element = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_ctl00_bodyContent_ContentPlaceHolder_ddlModule')))
select = Select(element)
options = [option.text for option in select.options]

for option_text in options:
    
    # Re-fetch the select element and its options
    select_element = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_bodyContent_ContentPlaceHolder_ddlModule')))
    select = Select(select_element)

    # Select each option by its visible text
    select.select_by_visible_text(option_text)

    # Perform your actions here
    # For demonstration, we'll just print the selected option's text
    print(f"Selected option: {option_text}")

    # You might need to wait for the page to load or for some action to complete
    # Adjust the sleep time based on your application's behavior
    time.sleep(2)

# options = dropdown.find_elements(By.TAG_NAME, "option")
# for option in options:
#     print(option.get_attribute("value"))
#     option = options[0]
#     # option_value = option.get_attribute("value")

#     option.click()
#     time.sleep(10)
# # Set date range
start_date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
end_date = datetime.now().strftime("%d/%m/%Y")

wait.until(
    EC.presence_of_element_located(
        (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpStartDate_txtDate")
    )
).clear()
driver.find_element(
    By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpStartDate_txtDate"
).send_keys(start_date)

wait.until(
    EC.presence_of_element_located(
        (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpEndDate_txtDate")
    )
).clear()
driver.find_element(
    By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_dpEndDate_txtDate"
).send_keys(end_date)

# # Click on Export CSV button
    # wait.until(
    #     EC.presence_of_element_located(
    #         (By.ID, "ctl00_ctl00_bodyContent_ContentPlaceHolder_lnkbtnDownload")
    #     )
    # ).click()

# default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
# time_limit = 60
# time_spent = 0

# while time_spent < time_limit:
#     downloaded_files = os.listdir(default_download_dir)
#     csv_files = [f for f in downloaded_files if f.endswith(".csv")]
#     if csv_files:
#         source_file = os.path.join(default_download_dir, csv_files[0])
#         destination_file = os.path.join("csv_reports", csv_files[0])
#         os.makedirs(os.path.dirname(destination_file), exist_ok=True)
#         shutil.move(source_file, destination_file)
#         print(f"CSV file downloaded: {csv_files[0]}")
#         break
#     time.sleep(1)
#     time_spent += 1
# else:
#     print("File download failed.")

# driver.quit()

