from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Assert_Table_Lines(driver, table_id, data_matrix):
    """
    Assert that both data_matrix are present as rows in the table.

    :param driver: The Selenium WebDriver instance.
    :param table_id: The ID of the table to extract.
    :param data_matrix: A dictionary containing the first line of data.
    :raises AssertionError: If either line is not found in the table.
    """
    matrix = []

    try:
        # Wait until the table is present in the DOM
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, table_id))
        )
        
        # Extract rows of the table body
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_values = [cell.text.strip() for cell in cells]
            if row_values:  # Ensure the row is not empty
                matrix.append(row_values)

        # Convert the input dictionaries to lists of values for easy comparison
        data_matrix_values = list(data_matrix.values())

        # Normalize the matrix rows and input values (convert all booleans to strings and remove empty values)
        matrix_normalized = []
        for row in matrix:
            row_normalized = [str(item) if isinstance(item, bool) else item for item in row if item != '']
            matrix_normalized.append(row_normalized)

        data_matrix_values_normalized = [str(item) if isinstance(item, bool) else item for item in data_matrix_values]

        # Assertions
        assert data_matrix_values_normalized in matrix_normalized, f"Row {data_matrix_values_normalized} not found in table."

        print("rows are present in the table.")

    except Exception as e:
        print(f"Error asserting table rows: {e}")
        raise

# def Assert_Screen_Values(driver, screen_data_matrix):
#      detail_code = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.ID, "ContentPlaceHolderMain_txtCode"))
#      ).get_attribute("value")
     
#      detail_description = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.ID, "ContentPlaceHolderMain_txtDescription"))
#      ).get_attribute("value")
     
#      detail_cod_ciclo = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.ID, "ContentPlaceHolderMain_txtCycleCode"))
#      ).get_attribute("value")
     
#      detail_cod_horario = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.ID, "ContentPlaceHolderMain_txtScheduleCode"))
#      ).get_attribute("value")
     
#      # Verify if the details match the inputs
#      assert detail_code == screen_data_matrix['codigo'], f"Code mismatch! Expected: {screen_data_matrix['codigo']}, Found: {detail_code}"
#      assert detail_description == screen_data_matrix['descricao'], f"Description mismatch! Expected: {screen_data_matrix['descricao']}, Found: {detail_description}"
#      assert detail_cod_ciclo == screen_data_matrix['cod_ciclo'], f"Cycle mismatch! Expected: {screen_data_matrix['cod_ciclo']}, Found: {detail_cod_ciclo}"
#      assert detail_cod_horario == screen_data_matrix['cod_horario'], f"Schedule mismatch! Expected: {screen_data_matrix['cod_horario']}, Found: {detail_cod_horario}"
     
def Assert_Screen_Values(driver, data_matrix, element_id_matrix):
    """
    Generalized function to verify screen values based on two matrices:
    1. data_matrix: Contains the expected values (key is a logical name, value is the expected value).
    2. element_id_matrix: Maps logical names to HTML element IDs.

    :param driver: Selenium WebDriver instance
    :param data_matrix: A dictionary where keys are logical field names and values are the expected values.
    :param element_id_matrix: A dictionary mapping logical field names to the corresponding element IDs.
    """
    for key, expected_value in data_matrix.items():
        if key not in element_id_matrix:
            raise KeyError(f"Missing element ID mapping for '{key}' in element_id_matrix.")

        element_id = element_id_matrix[key]  # Retrieve the element ID from the mapping
        
        # Wait for the element to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        
        # Determine if the element is a checkbox
        tag_name = element.tag_name.lower()
        if tag_name == "input" and element.get_attribute("type") == "checkbox":
            actual_value = element.is_selected()  # Retrieve checkbox state (True/False)
        else:
            actual_value = element.get_attribute("value")  # For other input types
        
        # Assert and compare the values
        assert str(actual_value).strip() == str(expected_value).strip(), (
            f"'{key}' (ID: '{element_id}') mismatch! "
            f"Expected: '{expected_value.strip()}', Found: '{str(actual_value).strip()}'"
        )