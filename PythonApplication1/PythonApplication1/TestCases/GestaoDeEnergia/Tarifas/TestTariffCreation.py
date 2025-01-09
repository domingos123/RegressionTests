from selenium import webdriver
from Utils.Asserts.Grids import Assert_Screen_Values, Assert_Table_Lines
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

    

       
def test_tariff_creation():  
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
        data = datetime.now().strftime('%Y%m%d%H%M%S')  # Format as 'YYYYMMDDHHMMSS' without special characters

        # Combine the string with the current date  
        data_matrix = {
            "codigo": "TR" + data,
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

        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # If a matching row was found, click on the button
        if target_row:
            button_cell = target_row.find_element(By.XPATH, ".//td[1]//a")  # Adjust the XPath if necessary
            button_cell.click()
        else:
            assert False, f"No row found with code: {data_matrix['codigo']}"
    
        element_id_matrix = {
            "codigo": "ContentPlaceHolderMain_txtCode",
            "descricao": "ContentPlaceHolderMain_txtDescription",
            "cod_ciclo": "ContentPlaceHolderMain_txtCycleCode",
            "cod_horario": "ContentPlaceHolderMain_txtScheduleCode",
        }
        Assert_Screen_Values(driver, data_matrix, element_id_matrix)
        
        
        print("teste test_tariff_creation concluido com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()
        
def test_tariff_creation_with_none_mandatory_fields():  
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
        data = datetime.now().strftime('%Y%m%d%H%M%S')  # Format as 'YYYYMMDDHHMMSS' without special characters
        
        data_line_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "Vazio",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Ver\u00e3o",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Monday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "09:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "23:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True
        }
        data_matrix = {
            "codigo": "TR2" + data,
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        # fill_mandatory_fields(driver, codigo, descricao, cod_ciclo, cod_horario)
        fill_mandatory_fields(driver, data_matrix)        
        add_line(driver, data_line_matrix)
        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        sleep(5)  # Wait for the page to load completely


        save_button.click()
        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # If a matching row was found, click on the button
        if target_row:
            button_cell = target_row.find_element(By.XPATH, ".//td[1]//a")  # Adjust the XPath if necessary
            button_cell.click()
        else:
            assert False, f"No row found with code: {data_matrix['codigo']}"

        data_screen_line_matrix = {
            "tariffType": "Vazio",
            "period": "Ver\u00e3o",
            "dayOfTheWeek": "SG",
            "beginHour": "09:00",
            "endHour": "23:00",
            "annulled": True
        }
        Assert_Table_Lines(driver, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00", data_screen_line_matrix)

        element_id_matrix = {
            "codigo": "ContentPlaceHolderMain_txtCode",
            "descricao": "ContentPlaceHolderMain_txtDescription",
            "cod_ciclo": "ContentPlaceHolderMain_txtCycleCode",
            "cod_horario": "ContentPlaceHolderMain_txtScheduleCode",
        }
        Assert_Screen_Values(driver, data_matrix, element_id_matrix)
        
        print("teste test_tariff_creation_mandatory_only_fields concluido com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()


# novo_url = driver.current_url
