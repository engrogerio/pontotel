import pytest
import alpha
from pytest import fixture

def fake_get_symbols():
    symbols = { 
        'Petroleo Brasileiro-Petrobras': 'PBR',
        'SABESP': 'SBS',
        'Telefonica Brasil': 'VIV',
        'TIM Participacoes': 'TSU',

    }
    return {'companies': [{'name':k, 'symbol':v} for k, v in symbols.items()]}

def fake_get_company_size(symbol: str, index: str):
    values = {'PBR': 2, 'SBS': 9, 'SUZ': 1, 'VIV': 6, 'TSU': 3, 'UGP': 2, 'VALE': 4, 'XP': 8}
    return values.get(symbol, 0)

def fake_get_api_data(symbol: str, function: str):

    fake_return = {
    "VIV": {
        "GLOBAL_QUOTE": 
            {
                "Global Quote": {
                    "01. symbol": "VIV",
                    "02. open": "7.1200",
                    "03. high": "7.3400",
                    "04. low": "7.0800",
                    "05. price": "7.2600",
                    "06. volume": "1312608",
                    "07. latest trading day": "2020-10-29",
                    "08. previous close": "7.2800",
                    "09. change": "-0.0200",
                    "10. change percent": "-0.2747%"
                }
            },
            "OVERVIEW":
            {
                "Symbol": "VIV",
                "AssetType": "Common Stock",
                "Name": "None",
                "Description": "Telefnica Brasil S.A.",
                "Exchange": "NYSE",
                "Currency": "USD",
                "Country": "USA",
                "Sector": "Communication Services",
                "Industry": "Telecom Services",
                "Address": "None",
                "FullTimeEmployees": "32793",
                "FiscalYearEnd": "December",
                "LatestQuarter": "2020-06-30",
                "MarketCapitalization": "444444",
                "GrossProfitTTM": "777777",
               
            }
        },
    "TSU": {
        "GLOBAL_QUOTE": 
            {
                "Global Quote": {
                    "01. symbol": "TSU",
                    "02. open": "2.1200",
                    "03. high": "2.3400",
                    "04. low": "2.0800",
                    "05. price": "2.2600",
                    "06. volume": "1312608",
                    "07. latest trading day": "2020-10-30",
                    "08. previous close": "2.2800",
                    "09. change": "0.0200",
                    "10. change percent": "0.2747%"
                }
            },
            "OVERVIEW":
            {
                "Symbol": "TSU",
                "AssetType": "Common Stock",
                "Name": "None",
                "Description": "TIM Participacoes",
                "Exchange": "NYSE",
                "Currency": "USD",
                "Country": "USA",
                "Sector": "Communication Services",
                "Industry": "Telecom Services",
                "Address": "None",
                "FullTimeEmployees": "32793",
                "FiscalYearEnd": "December",
                "LatestQuarter": "2020-06-30",
                "MarketCapitalization": "111111",
                "GrossProfitTTM": "666666",
            }
        },
    "SBS": {
        "GLOBAL_QUOTE": 
            {
                "Global Quote": {
                    "01. symbol": "SBS",
                    "02. open": "9.1200",
                    "03. high": "9.3400",
                    "04. low": "9.0800",
                    "05. price": "9.2600",
                    "06. volume": "1312608",
                    "07. latest trading day": "2020-10-30",
                    "08. previous close": "9.2800",
                    "09. change": "0.0200",
                    "10. change percent": "0.33%"
                }
            },
            "OVERVIEW":
            {
                "Symbol": "SBS",
                "AssetType": "Common Stock",
                "Name": "None",
                "Description": "Sabesp",
                "Exchange": "NYSE",
                "Currency": "USD",
                "Country": "USA",
                "Sector": "Water",
                "Industry": "Water Services",
                "Address": "None",
                "FullTimeEmployees": "32793",
                "FiscalYearEnd": "December",
                "LatestQuarter": "2020-06-30",
                "MarketCapitalization": "333333",
                "GrossProfitTTM": "111111",
            }
        },
    "PBR": {
        "GLOBAL_QUOTE": 
            {
                "Global Quote": {
                    "01. symbol": "PBR",
                    "02. open": "99.1200",
                    "03. high": "99.3400",
                    "04. low": "99.0800",
                    "05. price": "99.2600",
                    "06. volume": "1312608",
                    "07. latest trading day": "2020-10-30",
                    "08. previous close": "99.2800",
                    "09. change": "0.0200",
                    "10. change percent": "0.33%"
                }
            },
            "OVERVIEW":
            {
                "Symbol": "PBR",
                "AssetType": "Common Stock",
                "Name": "None",
                "Description": "Petroleo Brasileiro-Petrobras",
                "Exchange": "NYSE",
                "Currency": "USD",
                "Country": "USA",
                "Sector": "Oil",
                "Industry": "Oil Services",
                "Address": "None",
                "FullTimeEmployees": "32793",
                "FiscalYearEnd": "December",
                "LatestQuarter": "2020-06-30",
                "MarketCapitalization": "222222",
                "GrossProfitTTM": "999999",
            }
        },
    }
    return fake_return[symbol][function]

@pytest.fixture()
def alpha_instance():
    return alpha.Alpha()

@pytest.fixture()
def symbol():
    # We may pass anything here since it will not be 
    # used by fake_get_api_data as fake API on this test,
    # returns only one company symbol
    return 'VIV'

@pytest.fixture(autouse=True)
def setup(monkeypatch, alpha_instance):
    monkeypatch.setattr(alpha_instance, "get_api_data", fake_get_api_data)
    monkeypatch.setattr(alpha_instance, "get_symbols", fake_get_symbols)

def test_get_mci_index(alpha_instance, symbol):
    # Act
    result = alpha_instance.get_mci_index(symbol)

    # Assert
    assert result == 444444

def test_get_gross_profit(alpha_instance, symbol):
    # Act
    result = alpha_instance.get_gross_profit(symbol)

    # Assert
    assert result == 777777

def test_get_n_biggest_brazilian_companies_MCI(alpha_instance):
    # Act
    result = alpha_instance.get_n_biggest_brazilian_companies(4, 'MCI')
    
    # Assert
    assert result == [
        ('Telefonica Brasil', 'VIV', 444444),
        ('SABESP', 'SBS', 333333),
        ('Petroleo Brasileiro-Petrobras', 'PBR', 222222),
        ('TIM Participacoes', 'TSU', 111111),
        ]
    

def test_get_n_biggest_brazilian_companies_GP(alpha_instance):
    # Act
    result = alpha_instance.get_n_biggest_brazilian_companies(4, 'GP')

    # Assert
    assert result == [
        ('Petroleo Brasileiro-Petrobras', 'PBR', 999999),
        ('Telefonica Brasil', 'VIV', 777777),
        ('TIM Participacoes', 'TSU', 666666),
        ('SABESP', 'SBS', 111111),
        ]


def test_get_symbol_last_quote(alpha_instance):
    # Arrange
    
    # Act
    result = alpha_instance.get_symbol_last_quote('SBS')

    # Assert
    assert result == {"value": "9.2600", "currency": "USD", "date": "2020-10-30"}