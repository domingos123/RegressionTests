from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config  # Import the config.py file

def login(driver):
    # Navigate to the login page
    driver.get(config.login_url)
    
    # Wait for the login fields to load and fill them in
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtUserName")))

    # Fill out the login form
    driver.find_element(By.ID, "txtUserName").send_keys(config.username)
    driver.find_element(By.ID, "txtPassword").send_keys(config.password)
    driver.find_element(By.ID, "txtPassword").send_keys(Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(driver, 10).until(EC.url_contains("dev.nextbitt.net"))
    print("Login successful.")
    sleep(20)
