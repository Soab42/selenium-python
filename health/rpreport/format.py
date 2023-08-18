from selenium import webdriver
import time
import json
from rpreport.credentials import usernames, passwords


# Initialize Chrome WebDriver
driver = webdriver.Chrome()

for username, password in zip(usernames, passwords):
    # Navigate to the login page
    driver.get("login_url")

    # Fill in login form
    username_input = driver.find_element_by_id("username_field_id")
    password_input = driver.find_element_by_id("password_field_id")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element_by_id("login_button_id")
    login_button.click()

    # Navigate to the data page
    driver.get("data_url")

    # Scrape data
    data_element = driver.find_element_by_id("data_element_id")
    scraped_data = data_element.text

    # Save data to JSON file
    data_dict = {"username": username, "scraped_data": scraped_data}
    with open(f"{username}.json", "w") as json_file:
        json.dump(data_dict, json_file, indent=4)

    time.sleep(2)  # Add a delay before moving to the next user

# Close WebDriver
driver.quit()
