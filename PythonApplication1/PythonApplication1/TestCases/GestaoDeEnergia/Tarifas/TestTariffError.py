from selenium import webdriver
from Utils.Asserts.Error import assert_error_message
from Utils.LineGrids import add_line
from Utils.ScreenControlsFunctions import fill_input_field, select_dropdown_option, filter_column
from Utils.login import login
from Utils.navigation import navigate_to_page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime


def fill_mandatory_fields(driver, data_matrix):
    """Fill mandatory fields in the form."""
    # Fill in 'Código' field
    fill_input_field(driver, "ContentPlaceHolderMain_txtCode", data_matrix['codigo'])

    # Fill in 'Descrição' field
    fill_input_field(driver, "ContentPlaceHolderMain_txtDescription", data_matrix['descricao'])

    # Select 'Ciclo' dropdown option
    select_dropdown_option(driver, "ctl00_ContentPlaceHolderMain_RadComboBoxCycle_Input", data_matrix['cod_ciclo'])

    # Select 'Horário' dropdown option
    select_dropdown_option(driver, "ctl00_ContentPlaceHolderMain_RadComboBoxSchedule_Input",data_matrix['cod_horario'])

  
def create_default_tariff():  
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/Tariffs/Default"

    try:
        login(driver)
             # Check if the popup is present
        try:
            popup_locator = (By.CLASS_NAME, "introjs-tooltip")
            cancel_button_locator = (By.XPATH, "//a[contains(@class, 'introjs-button') and text()='Cancelar']")

            # Wait for the popup to appear (timeout after 5 seconds)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(popup_locator))

            # If popup is present, find the "Cancelar" button and click it
            cancel_button = driver.find_element(*cancel_button_locator)
            cancel_button.click()
            print("Popup detected and 'Cancelar' button clicked.")

        except Exception as e:
            print("No popup detected or 'Cancelar' button not found.")
            
        navbar_buttons = ["Gest\u00e3o de Energia", "Tarifas"]
        navigate_to_page(driver, navbar_buttons)
                
        assert driver.current_url == desired_url, f"Expected URL {desired_url}, but got {driver.current_url}"

        novo_button = driver.find_element(By.ID, "ContentPlaceHolderMain_btnNewTariff")
        novo_button.click()  

        expected_url = "https://dev.nextbitt.net/Tariffs/New?rtnURL=/Tariffs/Default.aspx"
        assert driver.current_url == expected_url, f"Expected to be on the Create page, but was on {driver.current_url}"

        sleep(5)  # Wait for the page to load completely
        # Get the current date in the desired format
        data = datetime.now().strftime('%Y%m%d')  # Format as 'YYYYMMDD' without special characters

        # Combine the string with the current date  
        data_matrix = {
            "codigo": "TRErro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        # fill_mandatory_fields(driver, codigo, descricao, cod_ciclo, cod_horario)
        fill_mandatory_fields(driver, data_matrix)
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()       
        
        print("default tariff created with success!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()  
 
def test_errors_in_tariff_creation_with_lines():  
    create_default_tariff()
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/Tariffs/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Tarifas"]
        navigate_to_page(driver, navbar_buttons)
        
        assert driver.current_url == desired_url, f"Expected URL {desired_url}, but got {driver.current_url}"

        novo_button = driver.find_element(By.ID, "ContentPlaceHolderMain_btnNewTariff")
        novo_button.click()  

        expected_url = "https://dev.nextbitt.net/Tariffs/New?rtnURL=/Tariffs/Default.aspx"
        assert driver.current_url == expected_url, f"Expected to be on the Create page, but was on {driver.current_url}"

        sleep(5)  # Wait for the page to load completely

        # Get the current date in the desired format
        data = datetime.now().strftime('%Y%m%d')  # Format as 'YYYYMMDD' without special characters
        data_matrix_error = {
            "codigo": "TRErro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        fill_mandatory_fields(driver, data_matrix_error)
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()
        
        # Step 6: Validate the error message using the function
        expected_error_message = "J\u00e1 existe outro registo com o mesmo C\u00f3digo."
        assert_error_message(driver, expected_error_message)        
        sleep(5)  # Wait for the page to load completely


        data_line_matrix_error = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "tipo2",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "22:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "01:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        add_line(driver, data_line_matrix_error)
        # Step 6: Validate the error message using the function
        expected_error_message = "A data final tem de ser superior \u00e0 data inicial."
        assert_error_message(driver, expected_error_message) 

        data_matrix = {
            "codigo": "TR2Erro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        
        data_line_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "tipo2",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "02:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "21:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        fill_mandatory_fields(driver, data_matrix)
        add_line(driver, data_line_matrix)
        sleep(5)

        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()
        sleep(10)
        assert driver.current_url == "https://dev.nextbitt.net/Tariffs/Default", \
        f"Expected URL 'https://dev.nextbitt.net/Tariffs/Default', but got '{driver.current_url}'"
        
        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()
        
        # assert driver.current_url == "https://dev.nextbitt.net/Tariffs/Default", f"Expected URL {"https://dev.nextbitt.net/Tariffs/Default"}, but got {driver.current_url}"

        data_matrix_error = {
            "codigo": "TRErro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        fill_mandatory_fields(driver, data_matrix_error)
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()
        
        # Step 6: Validate the error message using the function
        expected_error_message = "J\u00e1 existe outro registo com o mesmo C\u00f3digo."
        assert_error_message(driver, expected_error_message)        
        sleep(5)  # Wait for the page to load completely


        data_line_matrix_error = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "tipo2",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "22:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "01:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        add_line(driver, data_line_matrix_error)
        # Step 6: Validate the error message using the function
        expected_error_message = "A data final tem de ser superior \u00e0 data inicial."
        assert_error_message(driver, expected_error_message) 
        
        # # Step 6: Validate the error message using the function
        # expected_error_message = "A data final tem de ser superior \u00e0 data inicial."
        # assert_error_message(driver, expected_error_message) 
        data_matrix_error = {
            "codigo": "TR2Erro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        fill_mandatory_fields(driver, data_matrix_error)
        
        data_line_matrix= {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "Vazio",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Ver\u00e3o",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Monday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "02:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "10:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        add_line(driver, data_line_matrix)
        
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)  # Scroll to the button
        sleep(1)  # Add a slight delay to ensure scrolling completes
        save_button.click()

        
        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()
        

        data_matrix_error = {
            "codigo": "TRErro" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        fill_mandatory_fields(driver, data_matrix_error)
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()
        
        # Step 6: Validate the error message using the function
        expected_error_message = "J\u00e1 existe outro registo com o mesmo C\u00f3digo."
        assert_error_message(driver, expected_error_message)        
        sleep(5)  # Wait for the page to load completely


        data_line_matrix_error = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "tipo2",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "22:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "01:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        add_line(driver, data_line_matrix_error)
        # Step 6: Validate the error message using the function
        expected_error_message = "A data final tem de ser superior \u00e0 data inicial."
        assert_error_message(driver, expected_error_message) 
        
        data_line_matrix= {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "Vazio",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Ver\u00e3o",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Monday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "02:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "10:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        add_line(driver, data_line_matrix)
        
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)  # Scroll to the button
        sleep(1)  # Add a slight delay to ensure scrolling completes
        save_button.click()
        
    finally:
        # Step 3: Close the driver
        driver.quit()
        

