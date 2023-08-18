# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By  # Import the By class
# import time
# from selenium.webdriver.common.keys import Keys
# os.environ["PATH"] += r"H:\chromedriver"
# option=webdriver.ChromeOptions()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("http://demo.seleniumeasy.com/basic-first-form-demo.html")
# driver.implicitly_wait(8)
# # time.sleep(30)
# sum1 = driver.find_element(
#     By.NAME, "sum1")  # Use the By.ID constant
# sum2 = driver.find_element(
#     By.NAME, "sum2")  # Use the By.ID constant
#
# sum1.send_keys(Keys.NUMPAD1, Keys.NUMPAD8)
# sum2.send_keys(10)
#
# button = driver.find_element(By.CSS_SELECTOR, "button[onclick='return total()']")
# button.click()