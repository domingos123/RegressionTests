from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_page(driver, navbar_buttons):
    """
    Navigate through navbar buttons to the desired page.
    :param driver: WebDriver instance
    :param navbar_buttons: List of buttons to click in order (e.g., ["Gest\u00e3o de Energia", "Tarifas"])
    """
    for button in navbar_buttons:
        # Check for and remove any potential overlay blocking clicks
        try:
            # Wait for the overlay to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'introjs-overlay'))
            )
            # Remove the overlay
            driver.execute_script("document.querySelector('.introjs-overlay')?.remove();")
            # print("Overlay removed.")
        except Exception as overlay_exception:
             print("No overlay detected or failed to remove overlay.")
        
        # Ensure the button is clickable before clicking
        try:
            button_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(., '{button}')]"))
            )
            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            # Click the button
            button_element.click()
            # print(f"Clicked on: {button}")
        except Exception as click_exception:
            print(f"Failed to click on {button}: {click_exception}")
