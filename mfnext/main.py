from selenium import webdriver
from selenium.webdriver.common.by import By
from credentials import usernames, passwords
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

# import os
# os.environ["PATH"] += r"H:\chromedriver"
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
# Initialize Chrome WebDriver

driver.get("https://mfnext.microfin360.com/pmk/#/login")
# driver.maximize_window()

# Fill in login form
username_input = driver.find_element(By.ID, "__BVID__12")
password_input = driver.find_element(By.ID, "__BVID__13")

username_input.send_keys("sabuzbag")
password_input.send_keys("sabuzbag")

login_button = driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(3)")
login_button.click()

# Wait for the user to be logged in (adjust the time as needed)
time.sleep(3)

driver.get("https://mfnext.microfin360.com/pmk/#/members/members/index")
search_input = driver.find_element(By.NAME, "txt_name")
# search_input.send_keys(input('type member id'))
search_input.send_keys("026107225")

search_button = driver.find_element(By.ID, "custom-search-btn")
search_button.click()
time.sleep(1)
member_id = driver.find_element(By.XPATH, "//*[@id='__BVID__97']/tbody/tr/td[2]/div/div[1]/span/a")
href = member_id.get_attribute("href")

driver.get(href)

time.sleep(3)

# member_id.click()
# print(href)
loan_button = driver.find_element(By.XPATH, "//*[@id='__BVID__101__BV_tab_controls_']/li[3]")
loan_button.click()
time.sleep(1)
# loan_details = driver.find_element(By.ID, '__BVID__218')
loan_details_view_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'View transaction')]")
last_button = loan_details_view_button[-1]
last_button.click()
time.sleep(3)
# Find the table element
# table = driver.find_element(By.ID, "__BVID__107")
modal_table_header = driver.find_element(By.TAG_NAME, "caption")

# Get the next sibling element
rows = modal_table_header.find_element(By.XPATH, "following-sibling::*[1]")

# print(next_sibling.text)
# Initialize a list to store the extracted data
data = []

# Loop through each row and extract the data from columns
for row in rows:
    cells = rows.find_elements(By.TAG_NAME, 'td')
    print(
     cells[0].text,
     cells[1].text,
    )
    # row_data = {
    #             'SL No': cells[0].text.strip(),
    #             'Transaction Date': cells[6].text.strip(),
    #             'Actual Payment': cells[7].text.strip(),
    #         }
    # data.append(row_data)

# Close the browser session
driver.quit()

# Print the extracted data

# print(data)

# 026107225

# driver.quit()
