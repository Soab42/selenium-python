from selenium import webdriver
from selenium.webdriver.common.by import By
from rpreport.credentials import usernames, passwords
from bs4 import BeautifulSoup
import time
import json
# import os
# os.environ["PATH"] += r"H:\chromedriver"
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
# Initialize Chrome WebDriver


# for username, password in zip(usernames, passwords):
# Navigate to the login page
# Set the desired IP address as the Host header
ip_address = "103.139.165.110:8080"
headers = {"Host": ip_address}

# Navigate to the IP address with the custom headers
driver.get("http://" + ip_address)
driver.maximize_window()

all_data = {}

for username, password in zip(usernames, passwords):
    # Fill in login form
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    print(username)
    print(password)
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    # Navigate to the data page
    driver.get(
        "http://103.139.165.110:8080/accounts/rec_pay.php?from=2023-07-01&to=2023-07-31&but_search=Search")
    # Find the table element
    table_element = driver.find_element(
        By.CSS_SELECTOR, '.table.table-striped.table-bordered')

    # Get the HTML content of the table
    table_html = table_element.get_attribute('outerHTML')

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(table_html, 'html.parser')

    # Find all rows in the table body
    rows = soup.find_all('tbody')[0].find_all('tr')

    # Loop through the rows and extract data
    for row in rows:
        cells = row.find_all('td')
        row_data = {
            'SL No': cells[0].text.strip(),
            'Description': cells[1].text.strip(),
            'This Month': cells[2].text.strip(),
            # 'This Year': cells[3].text.strip(),
            # 'Cumulative': cells[4].text.strip()
        }

        # Save data to JSON file
        data_dict = {"username": username, "scraped_data": scraped_data}
        with open(f"{username}.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)

        time.sleep(2)  # Add a delay before moving to the next user

        # Store data in the dictionary
        all_data[username] = {"scraped_data": row_data}
        time.sleep(2)
        # Close the browser window when you're done
driver.quit()
