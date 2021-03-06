import logging
import logging.config
import requests
import json
import operator
import os
from urllib.parse import urlencode


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': str(BASE_DIR)+'\\log.txt'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Alpha:
    """
    Class that implement methods that consumes the alpha api services
    and return the values for the interface.
    
    """
    GLOBAL_QUOTE = 'GLOBAL_QUOTE'
    TIME_SERIES_INTRADAY_EXTENDED = 'TIME_SERIES_INTRADAY_EXTENDED'
    TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
    TIME_SERIES_DAILY_ADJUSTED = 'TIME_SERIES_DAILY_ADJUSTED'
    TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
    TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
    TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
    OVERVIEW = 'OVERVIEW'
    
    def __init__(self):

        try:
            self.apikey = os.environ['ALPHA_API_KEY']
            self.has_prod_api = True
        except KeyError as ex:
            print('Missing environment variable "ALPHA_API_KEY"!\nDetails on https://www.alphavantage.co/support/#api-key\nUsing DEMO API KEY!')
            self.has_prod_api = False
            self.apikey = '0S4J0EX4F61FJ0NJ'

    def get_api_data(self, symbol: str, function: str) -> dict:
        """
            Return data from the api call.
            Params:
                symbol: The company symbol to extract data from.

                function: The api function name to be called.
            
            Return:
        """
        params = {}
        params['symbol'] = symbol
        params['function'] = function
        params['apikey'] = self.apikey

        url =f'https://www.alphavantage.co/query?{urlencode(params)}'
        logger.info(f'Requesting url {url}...')
        response = requests.get(url)
        logger.debug(f'Response = {response.text}')
        return json.loads(response.text)

    def get_mci_index(self, symbol: str) -> int:
        """
            Market Capitalization index.
            Commonly referred to as "market cap," it is calculated
            by multiplying the total number of a company's outstanding
            shares by the current market price of one share.

            Params:
                symbol: The NYSE symbol for a specific company.
            
            Return:
                A number that represents the index value.
        """
        return int(self.get_api_data(symbol, self.OVERVIEW).get('MarketCapitalization', '0'))

    def get_gross_profit(self, symbol: str) -> int:
        """
        * Gross Profit TTM :
            Gross Profit (TTM) = Sales (TTM) - Cost of Goods Sold (TTM)

            Params:
                symbol: The NYSE symbol for a specific company.
            
            Return:
                A number that represents the index value.
        """
        return int(self.get_api_data(symbol, self.OVERVIEW).get('GrossProfitTTM', '0'))

    def get_company_size(self, symbol: str, index: str) -> int:
        """
            The company size estimated by using one of the 2 indexes:
            MCI - Market Capitalization index (default) or GP - Gross profit
            Params:

                symbol: The NYSE symbol for a specific company.

                index_name: 'MCI' or 'GP' - The name of the index used
                for the company size calculation.
        """
        if index == 'MCI': 
            return self.get_mci_index(symbol)
        if index == 'GP':
            return self.get_gross_profit(symbol)
        return 0
        
    def get_symbols(self) -> dict:
        """
            Return all Brazilian companies symbols available on 
            NYSE stock market.
            Alpha API has no method to get symbols by country that
            could be used without a paid API KEY.
            
        """
        if self.has_prod_api:
            symbols =  {
                    'AMBEV S.A': 'ABEV',
                    'Azul': 'AZUL',
                    'Banco Bradesco': 'BBD',
                    'Banco Santander Brasil': 'BSBR',
                    'BrasilAgro': 'LND',
                    'Braskem': 'BAK',
                    'BRF S.A.':	'BRFS',
                    'Centrais Eletricas Brasileiras': 'EBR',
                    'Comp. Paranaense de Energia-COPEL': 'ELP',
                    'Companhia Brasileira de Distribuica': 'CBD',
                    #'Companhia Energetica de Minas Gerais-CEMIG': 'CIG/C',                
                    'Companhia Energetica de Minas Gerais-CEMIG': 'CIG',
                    'Companhia Siderurgica Nacional-CSN': 'SID',
                    'CPFL Energia':	'CPL',
                    'Embraer': 'ERJ',
                    'Gafisa': 'GFA',
                    'Gerdau': 'GGB',
                    'Gol Linhas': 'GOL',
                    'Itau Unibanco': 'ITUB',
                    'Linx': 'LINX',
                    'Oi': 'OIBR.C',
                    'Petroleo Brasileiro-Petrobras': 'PBR',
                    'SABESP': 'SBS',
                    'Suzano S.A.': 'SUZ',
                    'Telefonica Brasil': 'VIV',
                    'TIM Participacoes': 'TSU',
                    'Ultrapar':	'UGP',
                    'Vale':	'VALE',
                    'XP Inc': 'XP'
                }
        # Using a small subset due to the free API key restrictions
        else:
            symbols = { 
                    'Petroleo Brasileiro-Petrobras': 'PBR',
                    'SABESP': 'SBS',
                    'Suzano S.A.': 'SUZ',
                    'Telefonica Brasil': 'VIV',
                    'TIM Participacoes': 'TSU',
                    'Ultrapar':	'UGP',
                    'Vale':	'VALE',
                    'XP Inc': 'XP'
            }

        return {'companies': [{'name':k, 'symbol':v} for k, v in symbols.items()]}

    def get_n_biggest_brazilian_companies(self, n: int, index: str) -> list:
        """
            Return a list of tuples with the n biggest companies (name, symbol)

            Params:

                n: Number of companies requested for the returning list

                index: Name of the index used to calculate the company size:
                "MCI" - Market Capitalization index or "GP" - Gross profit
        """

        symbols = self.get_symbols()['companies']
        values = [(dic_item['name'], dic_item['symbol'], self.get_company_size(dic_item['symbol'], index)) for dic_item in symbols]
        
        ord_values = sorted(values, key=operator.itemgetter(2),reverse=True)
        logger.info(f'biggest companies: {ord_values}')
        return ord_values[:n]

    def get_symbol_last_quote(self, symbol: str) -> dict:
        """
            Get data related to the last quote available from a company
        using GLOBAL_QUOTE API function call.

            Params:
                symbol: The NYSE symbol for a specific company.

            Return:
                dictionary with value, currency and date values
                for the last quote available for the passed parameter.
        """

        data = self.get_api_data(symbol, self.GLOBAL_QUOTE).get('Global Quote') # API Returns a json with 'Global Quote' Key
        logger.debug(f'Getting company {symbol} values: {data}')
        
        try:
            value = data.get('05. price',0)
            currency = 'USD'
            date = data.get('07. latest trading day',0)
        except AttributeError:
            value = 'Api error due to timming restrictions. Please try again in 5 minutes!'
            currency = ''
            date = ''
        return {"value": value, "currency": currency, "date": date}