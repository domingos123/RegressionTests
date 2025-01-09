from selenium import webdriver
from Utils.Asserts.Grids import Assert_Screen_Values, Assert_Table_Lines
from Utils.LineGrids import add_line, add_line_with_pop_up_grid, alter_line, eliminate_line
# from Utils.LineGrids import add_line
from Utils.ScreenControlsFunctions import change_tab, fill_input_field, select_dropdown_option, filter_column, select_first_popup_row, select_popup_row, set_checkbox_state
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
        "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_txtPriceInsert_wrapper": 45,
        "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True   
    }
    add_line(driver, data_line_matrix)

def add_lines_to_default_Pricing_tariff():  
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/Tariffs/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Pre\u00e7\u00e1rios de Tarifas"]
        navigate_to_page(driver, navbar_buttons)
        
        codigo = "TRCreationAll"

        target_row = filter_column(driver, codigo, "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00_ctl02_ctl02_FilterTextBox_tp_code", "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00")

        # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()

        # data_line_matrix = {
        #     "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "tipo2",
        #     "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_txtPriceInsert": "23,000",
        #     "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True   
        # }
        # add_line(driver, data_line_matrix)
        change_tab(driver, "Localiza\u00e7\u00f5es")
        
        add_line_with_pop_up_grid(driver,"ModalSearchLocat","ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnNewLocationPanel","ctl00_ContentPlaceHolderMain_SearchLocations_treeLocation")
        add_line_with_pop_up_grid(driver,"ModalSearchLocat","ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnNewLocationPanel","ctl00_ContentPlaceHolderMain_SearchLocations_treeLocation")
        


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


       
def test_tariffPricing_update_with_none_mandatory_fields():
    add_lines_to_default_Pricing_tariff()
    driver = webdriver.Chrome()
    desired_url = "https://dev.nextbitt.net/TariffSchedule/Default"

    try:
        login(driver)
        
        navbar_buttons = ["Gest\u00e3o de Energia", "Pre\u00e7\u00e1rios de Tarifas"]
        navigate_to_page(driver, navbar_buttons)
                
        assert driver.current_url == desired_url, f"Expected URL {desired_url}, but got {driver.current_url}"
        
        target_row = filter_column(driver, "TRCreationAll", "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00_ctl02_ctl02_FilterTextBox_tp_code", "ctl00_ContentPlaceHolderMain_RadGridTariffSchedule_ctl00")


        # Step 3: Click on the dropdown toggle button
        dropdown_button = target_row.find_element(By.XPATH, ".//td[1]//button[@class='btn btn-xs btn-outline-dark dropdown-toggle']")
        dropdown_button.click()   

        # Step 4: Wait for the dropdown menu and click the Edit button
        edit_button = WebDriverWait(target_row, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ul[contains(@class, 'dropdown-menu')]//a[contains(@id, 'btnEdit')]"))
        )
        edit_button.click()
            
        data_matrix = {
            "codigo": "TRCreationAltered",
            "descricao": "testeinput2",
            "fornecedor": "ESAB",
            "tipo_contrato": "teste02",
            "tarifa": "desc"
        }
        # fill_mandatory_fields(driver, codigo, descricao, cod_ciclo, cod_horario)
        fill_mandatory_fields(driver, data_matrix)
        sleep(10)
        

        lines_data_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_RadComboBoxFareTypeInsert": "asd ed",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_txtPriceInsert": "45,000",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl02_ctl03_LineCheckBoxAnnulledInsert": True   
        }
        data_line_altered_matrix = {
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_RadComboBoxFareTypeEdit": "Fora de Vazio",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_txtPriceEdit": "20,000",
            "ctl00_ContentPlaceHolderMain_RadGridLines_ctl00_ctl05_LineCheckBoxAnnulledEdit": False  
        }
        alter_line(driver, data_line_altered_matrix, 1)
        sleep(5)
        eliminate_line(driver,2)
        sleep(5)
        add_line(driver, lines_data_matrix)
        
        change_tab(driver, "Localiza\u00e7\u00f5es")

        alter_line(driver, data_line_altered_matrix, 1)
        sleep(5)
        eliminate_line(driver,2)
        sleep(5)
        add_line_with_pop_up_grid(driver,"ModalSearchLocat","ctl00_ContentPlaceHolderMain_ctl00_ContentPlaceHolderMain_btnNewLocationPanel","ctl00_ContentPlaceHolderMain_SearchLocations_treeLocation", lines_data_matrix)


    finally:
        # Step 3: Close the driver
        driver.quit()


# novo_url = driver.current_url
