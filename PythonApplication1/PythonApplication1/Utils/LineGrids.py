from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from Utils.ScreenControlsFunctions import filter_column

def alter_line(driver, data_line_matrix, row_index):
    """
    Function to alter a specific row in a dynamic table by clicking the 'pen' icon.

    Args:
        driver: Selenium WebDriver instance.
        data_line_matrix: Dictionary containing field IDs and values to alter.
        row_index: Index of the row to edit (0-based index).
    """
    try:
        # Step 1: Locate the target row
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")

        if row_index < 0 or row_index >= len(rows):
            print(f"Invalid row_index: {row_index}. Row does not exist.")
            return

        target_row = rows[row_index]
        print(f"Row {row_index} found.")

        # Step 2: Click the 'pen' icon to edit the row
        pen_icon = target_row.find_element(By.CLASS_NAME, "fa-pen")
        pen_icon.click()
        print("Edit button clicked. Waiting for inputs to become editable...")

        # Wait for the row to enter edit mode
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )

        # Step 3: Alter the fields based on data_line_matrix
        for field_id, value in data_line_matrix.items():
            if isinstance(value, bool):  # Handle checkboxes
                checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                if checkbox.is_selected() != value:
                    checkbox.click()
                print(f"Checkbox '{field_id}' set to {value}.")

            elif "RadComboBox" in field_id:  # Handle dropdowns
                dropdown_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, field_id + "_Input"))
                )
                dropdown_input.clear()  # Clear any previous value
                dropdown_input.click()
                sleep(1)

                dropdown_list = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, field_id + "_DropDown"))
                )
                options = dropdown_list.find_elements(By.CLASS_NAME, "rcbItem")
                for option in options:
                    if option.text.strip() == value:
                        option.click()
                        print(f"Selected '{value}' in dropdown '{field_id}'.")
                        break
                else:
                    print(f"Value '{value}' not found in dropdown '{field_id}'.")

            elif "DateTimePicker" in field_id:  # Handle date/time pickers
                datetime_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                datetime_input.clear()  # Clear old date
                datetime_input.send_keys(value)
                print(f"DateTime picker '{field_id}' set to '{value}'.")

            else:  # Default case: Text input
                text_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                text_input.clear()  # Clear existing value
                text_input.send_keys(value)
                print(f"Text input '{field_id}' set to '{value}'.")

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_btnSavelineEdit"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

        print("Save Line button clicked. Row updated successfully.")

    except Exception as e:
        print(f"An error occurred while altering the row: {e}")

def add_line(driver, data_line_matrix):
    try:
        # Step 1: Click the 'New Line' button
        sleep(3)
        new_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl00_btnNewLine"))
        )
        sleep(5)  # Wait for the page to load completely
        new_button.click()
        print("New Line button clicked.")

        # Step 2: Fill the inputs based on data_line_matrix
        for field_id, value in data_line_matrix.items():
            if isinstance(value, bool):  # Checkbox input
                checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                # Check or uncheck based on the value
                if checkbox.is_selected() != value:
                    checkbox.click()
                print(f"Checkbox '{field_id}' set to {value}.")

            elif "RadComboBox" in field_id:  # Handle dropdowns
                try:
                    # Click the input to open the dropdown
                    dropdown_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, field_id + "_Input"))
                    )
                    dropdown_input.click()
                    sleep(1)

                    # Locate dropdown list and select the correct option
                    dropdown_list = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, field_id + "_DropDown"))
                    )
                    
                    options = dropdown_list.find_elements(By.CLASS_NAME, "rcbItem")
                    for option in options:
                        if option.text.strip() == value:
                            option.click()
                            print(f"Selected '{value}' in dropdown '{field_id}'.")
                            break
                    else:
                        print(f"Value '{value}' not found in dropdown '{field_id}'.")
                except Exception as e:
                    print(f"Dropdown '{field_id}' error: {e}")

            elif "DateTimePicker" in field_id:  # Handle date/time pickers
                try:
                    # Click the date input field
                    datetime_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, field_id))
                    )
                    # datetime_input.clear()
                    datetime_input.send_keys(value)
                    print(f"DateTime picker '{field_id}' set to '{value}'.")
                except Exception as e:
                    print(f"DateTime picker '{field_id}' error: {e}")

            else:  # Default case: Text input
                try:
                    text_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, field_id))
                    )
                    text_input.clear()
                    text_input.send_keys(value)
                    print(f"Text input '{field_id}' set to '{value}'.")
                except Exception as e:
                    print(f"Text input '{field_id}' error: {e}")
                    # Step 3: Click the 'Save Line' button
       
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_btnSavelineInsert"))
        )
        save_button.click()
        print("Save Line button clicked.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def eliminate_line(driver, row_index):
    """
    Function to delete a specific row in a dynamic table by clicking the 'trash' icon.

    Args:
        driver: Selenium WebDriver instance.
        row_index: Index of the row to delete (0-based index).
    """
    try:
        # Step 1: Locate the table and rows
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Validate row_index
        if row_index < 0 or row_index >= len(rows):
            print(f"Invalid row_index: {row_index}. Row does not exist.")
            return

        target_row = rows[row_index]
        print(f"Row {row_index} found: {target_row.text}")

        # Step 2: Locate and click the 'trash' icon
        trash_icon = target_row.find_element(By.CLASS_NAME, "fa-trash")
        driver.execute_script("arguments[0].scrollIntoView(true);", trash_icon)
        trash_icon.click()
        print("Trash icon clicked. Waiting for the row to be deleted...")

        # Step 3: Wait for the row to disappear
        WebDriverWait(driver, 10).until(EC.staleness_of(target_row))
        print(f"Row {row_index} successfully deleted.")

    except TimeoutException:
        print("Timeout: Table, row, or delete button was not found.")
    except NoSuchElementException:
        print(f"Trash icon not found for row {row_index}.")
    except Exception as e:
        print(f"An error occurred while deleting the row: {e}")
        
def add_line_with_pop_up_grid(driver, modal_id,button_id,tree_id):
    """
    Clicks a specific line number from the tree view inside a modal popup.

    Parameters:
    - driver: WebDriver instance.
    - modal_id: ID of the modal popup.
    - line_number: The index (1-based) of the tree item to click.
    """
    try:
        # Step 1: Click the 'New Line' button
        sleep(3)
        new_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, button_id))
        )
        new_button.click()
        
        # Step 2: Wait for the popup's container div to appear
        print("Waiting for the popup container to load...")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, modal_id))
        )
        print("Popup container is visible.")
        

        grid_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_SearchLocations_btnGridViewPanel"))
        )
        sleep(1)  # Wait for the page to load completely
        grid_button.click()
        sleep(5)  # Wait for the page to load completely

        target_row = filter_column(driver, "Hotel", "ctl00_ContentPlaceHolderMain_SearchLocations_grdLocation_ctl00_ctl02_ctl02_FilterTextBox_deslocal", "ctl00_ContentPlaceHolderMain_SearchLocations_grdLocation_ctl00_Header")
        target_cell = target_row.find_elements(By.TAG_NAME, "td")[2]  # Select the 3rd <td> (Hotel)

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView(true);", target_cell)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(target_cell))
        driver.execute_script("arguments[0].click();", target_cell)
    
    except TimeoutException:
        print("Timeout: Could not locate an element in time.")
    except IndexError as ie:
        print(f"Error: {ie}")
    except Exception as e:
        print(f"An error occurred: {e}")

