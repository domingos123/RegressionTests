from TestCases.GestaoDeEnergia.PrecarioDeTarifas.TestTariffPricingCreation import test_tariffPricing_creation, test_tariffPricing_creation_with_none_mandatory_fields
from TestCases.GestaoDeEnergia.PrecarioDeTarifas.TestTariffPricingUpdate import test_tariffPricing_update_with_none_mandatory_fields
from TestCases.GestaoDeEnergia.Tarifas.TestTariffCreation import test_tariff_creation
from TestCases.GestaoDeEnergia.Tarifas.TestTariffCreation import test_tariff_creation_with_none_mandatory_fields
from TestCases.GestaoDeEnergia.Tarifas.TestTariffError import test_errors_in_tariff_creation_with_lines
from TestCases.GestaoDeEnergia.Tarifas.TestTariffUpdate import test_tariff_update

if __name__ == "__main__":
    #tarifas
    # test_tariff_creation()
    # test_tariff_creation_with_none_mandatory_fields()
    
    # test_tariff_update()
    
    # test_errors_in_tariff_creation_with_lines()
    

    #precario de tarifas
    # test_tariffPricing_creation()
    # test_tariffPricing_creation_with_none_mandatory_fields()
    test_tariffPricing_update_with_none_mandatory_fields()