import pytest
import alpha
from pytest import fixture

def fake_get_api_data(symbol: str, function: str):
    fake_return = {
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
            "Description": "Telefnica Brasil S.A. provides mobile and fixed telecommunications services to residential and corporate customers in Brazil. Its fixed line services portfolio includes local, domestic long-distance, and international long-distance calls; and mobile portfolio comprises voice and broadband Internet access through 3G, 4G, and 4.5G, as well as mobile value-added services and wireless roaming services. The company also offers data services, including broadband and mobile data services. In addition, it provides pay TV services through direct to home satellite technology, IPTV, and cable, as well as pay-per-view and video on demand services; network services, such as rental of facilities; other services comprising Internet access, private network connectivity, computer equipment leasing, extended, caller identification, voice mail, cellular blocker, and others; wholesale services, including interconnection services to users of other network providers; and digital services, such as entertainment, cloud, and financial services. Further, the company offers multimedia communication services, which include audio, data, voice and other sounds, images, texts, and other information, as well as sells devices, such as smartphones, broadband USB modems, and other devices. Additionally, it provides telecommunications solutions and IT support to various industries, such as retail, manufacturing, services, financial institutions, government, etc. Telefnica Brasil S.A. markets and sells its solutions through own stores, dealers, retail and distribution channels, door-to-door sales, and telesales. The company was formerly known as Telecomunicaes de So Paulo S.A. - TELESP and changed its name to Telefnica Brasil S.A. in October 2011. The company was incorporated in 1998 and is headquartered in So Paulo, Brazil. Telefnica Brasil S.A. operates as a subsidiary of SP Telecomunicaes Participaes Ltda",
            "Exchange": "NYSE",
            "Currency": "USD",
            "Country": "USA",
            "Sector": "Communication Services",
            "Industry": "Telecom Services",
            "Address": "None",
            "FullTimeEmployees": "32793",
            "FiscalYearEnd": "December",
            "LatestQuarter": "2020-06-30",
            "MarketCapitalization": "4490851328",
            "EBITDA": "None",
            "PERatio": "17.5772",
            "PEGRatio": "0.7044",
            "BookValue": "11.14",
            "DividendPerShare": "0.41",
            "DividendYield": "0.0544",
            "EPS": "1.396",
            "RevenuePerShareTTM": "0",
            "ProfitMargin": "0.1034",
            "OperatingMarginTTM": "0",
            "ReturnOnAssetsTTM": "0.0395",
            "ReturnOnEquityTTM": "0.0649",
            "RevenueTTM": "0",
            "GrossProfitTTM": "23706290000",
            "DilutedEPSTTM": "1.396",
            "QuarterlyEarningsGrowthYOY": "-0.216",
            "QuarterlyRevenueGrowthYOY": "-0.051",
            "AnalystTargetPrice": "11.89",
            "TrailingPE": "17.5772",
            "ForwardPE": "12.7389",
            "PriceToSalesRatioTTM": "1.6942",
            "PriceToBookRatio": "1.066",
            "EVToRevenue": "0.1234",
            "EVToEBITDA": "0.2946",
            "Beta": "0.5231",
            "52WeekHigh": "14.68",
            "52WeekLow": "7.53",
            "50DayMovingAverage": "8.1253",
            "200DayMovingAverage": "8.8406",
            "SharesOutstanding": "1688690048",
            "SharesFloat": "444447315",
            "SharesShort": "3451290",
            "SharesShortPriorMonth": "3499520",
            "ShortRatio": "3.02",
            "ShortPercentOutstanding": "0",
            "ShortPercentFloat": "0",
            "PercentInsiders": "0",
            "PercentInstitutions": "14.398",
            "ForwardAnnualDividendRate": "0.41",
            "ForwardAnnualDividendYield": "0.0544",
            "PayoutRatio": "1.2002",
            "DividendDate": "None",
            "ExDividendDate": "2020-07-01",
            "LastSplitFactor": "None",
            "LastSplitDate": "None"
        }
    }
    return fake_return[function]

@pytest.fixture
def alpha_instance():
    return alpha.Alpha()

@pytest.fixture
def setup(monkeypatch):
    class fake_get_api_data(object):
        def __init__(self):
            pass
        

def test_get_mci_index(monkeypatch):
    # Arrange
    function = 'OVERVIEW'
    alpha_instance = alpha.Alpha()

    # Act
    monkeypatch.setattr(alpha_instance, "get_api_data", fake_get_api_data)
    result = alpha_instance.get_mci_index('VIV')

    # Assert
    assert result == 4490851328

def test_get_gross_profit():
    pass

def test_get_company_size():
    pass

def test_get_interval():
    pass

def test_get_symbols():
    pass

def test_get_n_biggest_brazilian_companies():
    pass

def test_get_symbol_last_quote():
    pass