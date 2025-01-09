from selenium import webdriver
from Utils.Asserts.Grids import Assert_Screen_Values, Assert_Table_Lines
from Utils.LineGrids import add_line
# from Utils.LineGrids import add_line
from Utils.ScreenControlsFunctions import fill_input_field, select_dropdown_option, filter_column, select_first_popup_row, select_popup_row, set_checkbox_state
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
    select_dropdown_option(driver, "ctl00_ContentPlaceHolderMain_RadComboBoxContractType_Input", data_matrix['tipo_contrato'])

    # Select 'Horário' dropdown option
    select_popup_row(driver,"ContentPlaceHolderMain_btnSearchSupplier","ModalSearchSupplier", "ctl00_ContentPlaceHolderMain_SearchSupplier_grdSupplier_ctl00", "ctl00_ContentPlaceHolderMain_SearchSupplier_grdSupplier_ctl00_ctl02_ctl02_FilterTextBox_su_name", data_matrix['fornecedor'])
    
    select_first_popup_row(driver,"ContentPlaceHolderMain_btnSearchTariff", "ContentPlaceHolderMain_SearchTariffs_ModalSearchTariffs","ctl00_ContentPlaceHolderMain_SearchTariffs_RadGridSearchTariffs_ctl00")

def fill_non_mandatory_fields(driver, data_matrix):
    """Fill mandatory fields in the form."""
    # Fill in 'Código' field
    fill_input_field(driver, "ContentPlaceHolderMain_txtNrContract", data_matrix['n_contrato'])

    # Fill in 'Descrição' field
    fill_input_field(driver, "ctl00_ContentPlaceHolderMain_RadDateTimeStartDate_dateInput", data_matrix['data_inicio'])

    # Select 'Ciclo' dropdown option
    fill_input_field(driver, "ctl00_ContentPlaceHolderMain_RadDateTimeEndDate_dateInput", data_matrix['data_fim'])

    # Select 'Horário' dropdown option
    set_checkbox_state(driver,"ContentPlaceHolderMain_CheckBoxAnnulled", data_matrix['anulado'])
    

    data_line_matrix = {
        "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "asd ed",
        "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_txtPriceInsert": "45,000",
        "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True   
    }
    add_line(driver, data_line_matrix)


       
def test_tariffPricing_creation():  
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/TariffSchedule/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Pre\u00e7\u00e1rios de Tarifas"]
        navigate_to_page(driver, navbar_buttons)
                
        assert driver.current_url == desired_url, f"Expected URL {desired_url}, but got {driver.current_url}"

        novo_button = driver.find_element(By.ID, "ContentPlaceHolderMain_btnNewTariffSchedule")
        novo_button.click()  

        expected_url = "https://dev.nextbitt.net/TariffSchedule/New?rtnURL=/TariffSchedule/Default.aspx"
        assert driver.current_url == expected_url, f"Expected to be on the Create page, but was on {driver.current_url}"

        sleep(5)  # Wait for the page to load completely
        # Get the current date in the desired format
        data = datetime.now().strftime('%Y%m%d%H%M%S')  # Format as 'YYYYMMDDHHMMSS' without special characters

        # Combine the string with the current date  
        data_matrix = {
            "codigo": "TRCreation",
            "descricao": "testeinput",
            "fornecedor": "A.BORGES DO AMARAL",
            "tipo_contrato": "teste01",
            "tarifa": "Nova2"
        }
        # fill_mandatory_fields(driver, codigo, descricao, cod_ciclo, cod_horario)
        fill_mandatory_fields(driver, data_matrix)
        sleep(10)  # Allow popup to open

        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()

        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00_ctl02_ctl02_FilterTextBox_tp_code", "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00")

        # If a matching row was found, click on the button
        if target_row:
            button_cell = target_row.find_element(By.XPATH, ".//td[1]//a")  # Adjust the XPath if necessary
            button_cell.click()
        else:
            assert False, f"No row found with code: {data_matrix['codigo']}"
    
        element_id_matrix = {
            "codigo": "ContentPlaceHolderMain_txtCode",
            "descricao": "ContentPlaceHolderMain_txtDescription",
            "fornecedor": "ContentPlaceHolderMain_txtSupplier",
            "tipo_contrato": "ContentPlaceHolderMain_txtContractType",
            "tarifa": "ContentPlaceHolderMain_txtTariff"
        }
        Assert_Screen_Values(driver, data_matrix, element_id_matrix)
        
        
        print("teste test_tariffPricing_creation concluido com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()
        
def test_tariffPricing_creation_with_none_mandatory_fields():  
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/TariffSchedule/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Pre\u00e7\u00e1rios de Tarifas"]
        navigate_to_page(driver, navbar_buttons)
                
        assert driver.current_url == desired_url, f"Expected URL {desired_url}, but got {driver.current_url}"

        novo_button = driver.find_element(By.ID, "ContentPlaceHolderMain_btnNewTariffSchedule")
        novo_button.click()  

        expected_url = "https://dev.nextbitt.net/TariffSchedule/New?rtnURL=/TariffSchedule/Default.aspx"
        assert driver.current_url == expected_url, f"Expected to be on the Create page, but was on {driver.current_url}"

        sleep(5)  # Wait for the page to load completely
        
        # Combine the string with the current date  
        data_matrix = {
            "codigo": "TRCreationAll",
            "descricao": "testeinput",
            "fornecedor": "A.BORGES DO AMARAL",
            "tipo_contrato": "teste01",
            "n_contrato": "23",
            "tarifa": "Nova2",
            "data_inicio": "14/12/2024 00:00:00",
            "data_fim": "17/12/2024 00:00:00",
            "anulado": True   
        }
        # fill_mandatory_fields(driver, codigo, descricao, cod_ciclo, cod_horario)
        fill_mandatory_fields(driver, data_matrix)
        fill_non_mandatory_fields(driver, data_matrix)
        sleep(30)  # Allow popup to open

        # Step 5: Save the new tariff
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnSavePanel"))
        )
        save_button.click()

        target_row = filter_column(driver, data_matrix['codigo'], "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00_ctl02_ctl02_FilterTextBox_tp_code", "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00")

        # If a matching row was found, click on the button
        if target_row:
            button_cell = target_row.find_element(By.XPATH, ".//td[1]//a")  # Adjust the XPath if necessary
            button_cell.click()
        else:
            assert False, f"No row found with code: {data_matrix['codigo']}"
    
        element_id_matrix = {
            "codigo": "ContentPlaceHolderMain_txtCode",
            "descricao": "ContentPlaceHolderMain_txtDescription",
            "fornecedor": "ContentPlaceHolderMain_txtSupplier",
            "tipo_contrato": "ContentPlaceHolderMain_txtContractType",
            "n_contrato": "ContentPlaceHolderMain_txtNrContract",
            "tarifa": "ContentPlaceHolderMain_txtTariff",
            "data_inicio": "ContentPlaceHolderMain_txtStartDate",
            "data_fim": "ContentPlaceHolderMain_txtEndDate",
            "anulado": "ContentPlaceHolderMain_CheckBoxAnnulled" 
        }
        Assert_Screen_Values(driver, data_matrix, element_id_matrix)
        data_screen_line_matrix = {
            "TariffType": "asd ed",
            "Value": "45,000",
            "annulled": True   
        }
        
        Assert_Table_Lines(driver, "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00", data_screen_line_matrix)
        
        print("teste test_tariffPricing_creation concluido com sucesso!!!")
    finally:
        # Step 3: Close the driver
        driver.quit()


# novo_url = driver.current_url
