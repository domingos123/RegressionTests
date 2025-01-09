from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def assert_error_message(driver, expected_message, timeout=10):
    """
    Validates that the expected error message is displayed on the page.

    Parameters:
        driver: The Selenium WebDriver instance.
        expected_message (str): The expected error message to validate.
        timeout (int): Maximum time to wait for the error message to appear (default is 10 seconds).

    Raises:
        AssertionError: If the error message does not appear or does not match the expected message.
    """
    try:
        # Wait for the error message to be visible
        error_message_element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "ContentPlaceHolderMain_lblError"))
        )
        # Get the error message text
        actual_message = error_message_element.text

        # Assert that the actual message matches the expected message
        assert actual_message == expected_message, \
            f"Expected error message '{expected_message}', but got '{actual_message}'"
        print("Error message successfully validated.")
    except TimeoutException:
        raise AssertionError("Error message did not appear within the expected time.")