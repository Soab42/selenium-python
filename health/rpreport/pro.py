from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from rpreport.credentials import usernames, passwords
import time
import json
import multiprocessing


def scrape_data(username, password):
    # Initialize Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=option)

    # Set the desired IP address as the Host header
    ip_address = "103.139.165.110:8080"
    headers = {"Host": ip_address}

    # Navigate to the login page
    driver.get("http://" + ip_address)
    driver.maximize_window()

    # Fill in login form
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    # Wait for the user to be logged in (adjust the time as needed)
    time.sleep(3)

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

    user_data = []

    # Loop through the rows and extract data
    for row in rows:
        cells = row.find_all('td')
        row_data = {
            'SL No': cells[0].text.strip(),
            'Description': cells[1].text.strip(),
            'This Month': cells[2].text.strip(),
        }
        user_data.append(row_data)

    # Close the browser window when done
    driver.quit()

    return {username: user_data}


if __name__ == "__main__":
    # Create a list of processes for concurrent scraping
    processes = []
    for username, password in zip(usernames, passwords):
        process = multiprocessing.Process(
            target=scrape_data, args=(username, password))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Store all scraped data in a single dictionary
    all_data = []
    for process in processes:
        scraped_data = process.exitcode  # Get the returned data from the process
        all_data.update(scraped_data)

    # Save all_data to a single JSON file
    with open("all_data.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)
