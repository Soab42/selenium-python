from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from health.credentials import usernames, passwords
import time
import json
import multiprocessing
from multiprocessing import Process, Queue

# Define the number of concurrent processes
MAX_CONCURRENT_PROCESSES = 1


def scrape_data(queue, result_queue):

    while True:
        try:
            username, password = queue.get_nowait()
        except multiprocessing.Queue.empty():
            break

        # Initialize Chrome WebDriver and scraping code
        # ... (same as your original scrape_data function)
        # Initialize Chrome WebDriver
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=option)

        # Navigate to the login page
        driver.get("https://mfnext.microfin360.com/pmk/#/login")
        driver.maximize_window()

        # Fill in login form
        username_input = driver.find_element(By.ID, "__BVID__12")
        password_input = driver.find_element(By.ID, "__BVID__13")

        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(3)")
        login_button.click()

        # Wait for the user to be logged in (adjust the time as needed)
        time.sleep(3)

        # Navigate to the data page
        driver.get(
            "http://103.139.165.110:8080/accounts/rec_pay.php?from=2023-07-01&to=2023-07-31&but_search=Search")

        # Find the table element
        table_element = driver.find_element(By.CSS_SELECTOR, '.table.table-striped.table-bordered')

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
            user_data = {
                'SL No': cells[0].text.strip(),
                'Description': cells[1].text.strip(),
                'This Month': cells[2].text.strip(),
            }
    # Append scraped data to a shared result dictionary
    scraped_data = {username: user_data}  # Modify this according to your data
    result_queue.put(scraped_data)
    # Close the browser window when done
    driver.quit()


def main():
    # Create a task queue
    task_queue = Queue()

    # Enqueue all tasks (username, password pairs) into the queue
    for username, password in zip(usernames, passwords):
        task_queue.put((username, password))

    # Create a result queue to store scraped data from processes
    result_queue = Queue()

    # Create and start concurrent processes
    processes = []
    for _ in range(MAX_CONCURRENT_PROCESSES):
        process = Process(target=scrape_data, args=(task_queue, result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Gather and process the scraped data from all processes
    all_data = {}
    while not result_queue.empty():
        scraped_data = result_queue.get()
        all_data.update(scraped_data)

    # Save all_data to a single JSON file
    with open("all_data.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)


if __name__ == "__main__":
    main()
