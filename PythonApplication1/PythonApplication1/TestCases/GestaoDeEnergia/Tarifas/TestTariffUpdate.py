from selenium import webdriver
from Utils.Asserts.Grids import Assert_Screen_Values, Assert_Table_Lines
from Utils.LineGrids import add_line, alter_line,eliminate_line
from Utils.ScreenControlsFunctions import fill_input_field, select_dropdown_option, filter_column
from Utils.login import login
from Utils.navigation import navigate_to_page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
 
def add_line_to_default_tariff():  
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/Tariffs/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Tarifas"]
        navigate_to_page(driver, navbar_buttons)
        
        data = datetime.now().strftime('%Y%m%d')  # Format as 'YYYYMMDD' without special characters

        codigo = "TR2" + data

        target_row = filter_column(driver, codigo, "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()

        data_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "Ponta",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Monday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "09:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "23:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": False
        }
        
        add_line(driver, data_matrix)
         # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        sleep(5)  # Wait for the page to load completely
        save_button.click()
        
        print("Registo default criado com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()



def test_tariff_update():  
    add_line_to_default_tariff()
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/Tariffs/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Tarifas"]
        navigate_to_page(driver, navbar_buttons)
        
        data = datetime.now().strftime('%Y%m%d')  # Format as 'YYYYMMDD' without special characters

        codigo = "TR2" + data
        
        target_row = filter_column(driver, codigo, "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()
        
        lines_data_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "Simples",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxPeriodInsert": "Ver\u00e3o",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxWeekdayInsert": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerStartDateInsert_dateInput": "09:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadDateTimePickerEndDateInsert_dateInput": "23:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": False
        }
        data_line_altered_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadComboBoxFareTypeEdit": "tipo2",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadComboBoxPeriodEdit": "Inverno",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadComboBoxWeekdayEdit": "Friday",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadDateTimePickerStartDateEdit_dateInput": "05:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadDateTimePickerEndDateEdit_dateInput": "22:00",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_LineCheckBoxAnnulledEdit": True
        }
        
        data_matrix = {
            "codigo": "TR2" + datetime.now().strftime('%Y%m%d%H%M%S'),
            "descricao": "testeinput",
            "cod_ciclo": "DIA - Diario",
            "cod_horario": "SIM - Horario Simples",
        }
        fill_mandatory_fields(driver, data_matrix)
        alter_line(driver, data_line_altered_matrix, 1)
        sleep(5)
        eliminate_line(driver,2)
        sleep(5)
        add_line(driver, lines_data_matrix)

         # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        sleep(5)  # Wait for the page to load completely


        save_button.click()
        target_row = filter_column(driver, codigo, "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00_ctl02_ctl02_FilterTextBox_tf_code", "ctl00_ContentPlaceHolderMain_RadGridTariffs_ctl00")

        # If a matching row was found, click on the button
        if target_row:
            button_cell = target_row.find_element(By.XPATH, ".//td[1]//a")  # Adjust the XPath if necessary
            button_cell.click()
        else:
            assert False, f"No row found with code: {codigo}"

        screen_line_data_matrix = {
            "tariffType": "Simples",
            "period": "Ver\u00e3o",
            "dayOfTheWeek": "SX",
            "beginHour": "09:00",
            "endHour": "23:00",
            "annulled": False
        }
        screen_line_data_altered_matrix = {
            "tariffTypeAltered": "tipo2",
            "periodAltered": "Inverno",
            "dayOfTheWeekAltered": "SX",
            "beginHourAltered": "05:00",
            "endHourAltered": "22:00",
            "annulledAltered": True
        }
              
        Assert_Table_Lines(driver, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00", screen_line_data_matrix)
        Assert_Table_Lines(driver, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00", screen_line_data_altered_matrix)
        
        element_id_matrix = {
            "codigo": "ContentPlaceHolderMain_txtCode",
            "descricao": "ContentPlaceHolderMain_txtDescription",
            "cod_ciclo": "ContentPlaceHolderMain_txtCycleCode",
            "cod_horario": "ContentPlaceHolderMain_txtScheduleCode",
        }
        Assert_Screen_Values(driver, data_matrix, element_id_matrix)

            
        print("teste test_tariff_update concluido com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()

