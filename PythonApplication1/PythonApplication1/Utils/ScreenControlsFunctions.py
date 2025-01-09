from time import sleep
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def filter_column(driver, codigo, controlId, tableId):
    # Locate the filter textbox
    filter_textbox = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.ID, controlId))
    )
    filter_textbox.send_keys(codigo)
    filter_textbox.send_keys(Keys.RETURN)

    # Wait for the loading indicator to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'loading')]"))
    )
    sleep(10)
    
    # Use the tableId parameter in the XPath to find the filtered rows
    filtered_rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, f"//table[@id='{tableId}']//tbody/tr"))
    )

    # Ensure there are filtered rows
    assert len(filtered_rows) > 0, "No filtered rows found after applying filter"

    # Assume the first row is the target row
    target_row = filtered_rows[0]

    return target_row  # Return the target row

def fill_input_field(driver, field_id, value, wait_time=10):
    sleep(10)
    """Helper function to wait for an input field, clear it, and fill with a value."""
    input_field = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    input_field.clear()
    input_field.send_keys(value)

def select_dropdown_option(driver, dropdown_id, option_text, wait_time=10):
    """Helper function to open a dropdown and select an option."""
    dropdown_input = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.ID, dropdown_id))
    )
    dropdown_input.click()
    
    dropdown_option = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[text()='{option_text}']"))
    )
    dropdown_option.click()
    
def select_popup_row(driver, searchbuttonId, modal_id, table_id, filterControl_id, codigo,wait_time=10):
    """
    Opens a popup, waits for the popup's content to load, locates the table, and clicks the first row.

    :param driver: Selenium WebDriver instance
    :param searchbuttonId: ID of the button that opens the popup
    :param popup_div_id: ID of the div that loads after the popup opens
    :param table_id: ID of the table containing rows
    :param wait_time: Maximum wait time for the popup and table to load
    """
    try:
        # Step 1: Open the popup
        print("Opening the popup...")
        search_button = driver.find_element(By.ID, searchbuttonId)
        search_button.click()

        # Step 2: Wait for the popup's container div to appear
        print("Waiting for the popup container to load...")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.ID, modal_id))
        )

        # Step 3: Wait for the table inside the popup's div to load
        print("Waiting for the table to load inside the popup...")
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, table_id))
        )

        # Step 4: Locate and click the first row in the table
        print("Locating the first row in the table...")
        target_row = filter_column(driver, codigo, filterControl_id, table_id)

        # first_row = table.find_element(By.XPATH, ".//tr[4]")  # Select the first row dynamically

        # Scroll to the first row and click
        print("Clicking the first row...")
        driver.execute_script("arguments[0].scrollIntoView(true);", target_row)
        sleep(1)  # Allow time for scrolling animation
        target_row.click()
        print("First row clicked successfully.")
    
    except TimeoutException as e:
        print("Timeout: Popup content or table did not load within the specified wait time.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def select_first_popup_row(driver, searchbuttonId, modal_id, table_id,wait_time=10):
    """
    Opens a popup, waits for the popup's content to load, locates the table, and clicks the first row.

    :param driver: Selenium WebDriver instance
    :param searchbuttonId: ID of the button that opens the popup
    :param popup_div_id: ID of the div that loads after the popup opens
    :param table_id: ID of the table containing rows
    :param wait_time: Maximum wait time for the popup and table to load
    """
    try:
        # Step 1: Open the popup
        print("Opening the popup...")
        search_button = driver.find_element(By.ID, searchbuttonId)
        search_button.click()

        # Step 2: Wait for the popup's container div to appear
        print("Waiting for the popup container to load...")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.ID, modal_id))
        )

        # Step 3: Wait for the table inside the popup's div to load
        print("Waiting for the table to load inside the popup...")
        table = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, table_id))
        )

        # Step 4: Locate and click the first row in the table
        print("Locating the first row in the table...")
        first_row = table.find_element(By.XPATH, ".//tr[2]")  # Select the first row dynamically

        # Scroll to the first row and click
        print("Clicking the first row...")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_row)
        sleep(1)  # Allow time for scrolling animation
        first_row.click()
        print("First row clicked successfully.")
    
    except TimeoutException as e:
        print("Timeout: Popup content or table did not load within the specified wait time.")
    except Exception as e:
        print(f"An error occurred: {e}")
        

def set_checkbox_state(driver, checkbox_id, state, wait_time=10):
    """
    Set a checkbox's checked property based on the desired state.

    :param driver: Selenium WebDriver instance.
    :param checkbox_id: The ID of the checkbox element.
    :param state: Desired state for the checkbox (True for checked, False for unchecked).
    :param wait_time: Maximum wait time to locate the checkbox.
    """
    try:
        # Wait for the checkbox to be present and clickable
        checkbox = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.ID, checkbox_id))
        )

        # Check the current state of the checkbox
        is_checked = checkbox.is_selected()

        # Set the checkbox state only if it doesn't match the desired state
        if state and not is_checked:
            print(f"Checking the checkbox with ID '{checkbox_id}'.")
            checkbox.click()
        elif not state and is_checked:
            print(f"Unchecking the checkbox with ID '{checkbox_id}'.")
            checkbox.click()
        else:
            print(f"Checkbox with ID '{checkbox_id}' is already in the desired state.")

    except TimeoutException:
        print(f"Timeout: Checkbox with ID '{checkbox_id}' was not clickable within {wait_time} seconds.")
    except Exception as e:
        print(f"An error occurred while setting the checkbox state: {e}")


def change_tab(driver, tab_id, wait_time=10):
    """
    Changes to a tab by its ID (index) or text content.

    :param driver: Selenium WebDriver instance.
    :param tab_id: The tab's index (zero-based) or its text content.
    :param wait_time: Maximum wait time to locate the tab.
    """
    try:
        sleep(2)  # Allow animation to settle if applicable

        # Refined selector: Ensures valid, visible tabs only
        tabs = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "ul.rtsUL > li.rtsLI:not(.disabled) > a.rtsLink")
            )
        )

        # Debugging: Print all tabs located
        print("Tabs found:")
        for i, tab in enumerate(tabs):
            print(f"Index {i}: '{tab.text.strip()}'")

        if not tabs:
            print("Error: No tabs found on this screen.")
            return

        # Select tab by index
        if isinstance(tab_id, int):
            if 0 <= tab_id < len(tabs):
                print(f"Clicking tab at index {tab_id}...")
                target_tab = tabs[tab_id]
            else:
                print(f"Error: Tab index {tab_id} is out of range. Available tabs: {len(tabs)}")
                return
        # Select tab by text content
        else:
            print(f"Clicking tab with text '{tab_id}'...")
            target_tab = next(
                (tab for tab in tabs if tab_id.strip().lower() in tab.text.strip().lower()),
                None
            )
            if not target_tab:
                print(f"Error: No tab with text '{tab_id}' was found.")
                return

        # Scroll the tab into view and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", target_tab)
        sleep(1)  # Allow animation to settle if applicable
        target_tab.click()
        print("Tab clicked successfully.")

    except TimeoutException:
        print(f"Timeout: Unable to locate tabs within {wait_time} seconds.")
    except Exception as e:
        print(f"An error occurred while changing tabs: {e}")

