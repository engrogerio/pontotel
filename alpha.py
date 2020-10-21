import logging
import logging.config
import requests
import json
import operator
import os
import sys
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
logger.setLevel(logging.DEBUG)

class Alpha:
    def __init__(self):
        self.FUNCTIONS = {'Global quote': 'GLOBAL_QUOTE', 'Intraday extended': 'TIME_SERIES_INTRADAY_EXTENDED',
                'Daily': 'TIME_SERIES_DAILY', 'Daily adjusted': 'TIME_SERIES_DAILY_ADJUSTED',
                'Weekly': 'TIME_SERIES_WEEKLY', 'Weekly adjusted': 'TIME_SERIES_WEEKLY_ADJUSTED',
                'Monthly': 'TIME_SERIES_MONTHLY', 'Overview': 'OVERVIEW'}
        try:
            self.apikey = os.environ['ALPHA_API_KEY']
        except KeyError as ex:
            print('Missing environment variable "ALPHA_API_KEY"!\nDetails on https://www.alphavantage.co/support/#api-key\nUsing DEMO API KEY!')
            self.apikey = '0S4J0EX4F61FJ0NJ'

        self.MCI = {"MCI": "get_mci_index", "GP": "get_gross_profit"}

    def get_api_data(self, symbol, function)-> dict:
        """
            Return data from the api call.
            Params:
                symbol: The company symbol to extract data from.

                function: The api funtion to be called.
            
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

    def get_mci_index(self, symbol: str) -> float:
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
        return int(self.get_api_data(symbol, self.FUNCTIONS['Overview']).get('MarketCapitalization', '0'))

    def get_gross_profit(self, symbol: str) -> int:
        """
        * Gross Profit TTM :
            Gross Profit (TTM) = Sales (TTM) - Cost of Goods Sold (TTM)

            Params:
                symbol: The NYSE symbol for a specific company.
            
            Return:
                A number that represents the index value.
        """
        return int(self.get_api_data(symbol, self.FUNCTIONS['Overview']).get('GrossProfitTTM', '0'))

    def get_company_size(self, symbol, index_name:str)-> int:
        """
            The company size estimated by using one of the 2 indexes:
            'MCI' (default) or 'GP'
            Params:
                symbol: The NYSE symbol for a specific company.
                index_name: 'MCI' or 'GP' - The name of the index used 
                for the company size calculation.
        """
        if index_name == 'GP':
            return self.get_gross_profit(symbol)
        else:
            return self.get_mci_index(symbol)
        
    def get_interval(self)->dict:
        return {'1': '1min', '5': '5min', '15': '15min', '30': '30min', '60': '60min'}

    def get_symbols(self)-> dict:
        """
            Return all Brazilian companies symbols available on 
            NYSE stock market.
            Alpha API has no method to get symbols by country that
            could be used without a paid API KEY.
            
        """
        
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
        # Using a small subset due to the API KEY restrictions
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

    def get_n_biggest_brazilian_companies(self, n)-> list:
        """
            Return a list of tuples with the n biggest companies (name, symbol)
        """
        symbols = self.get_symbols()['companies']
        values = [(dic_item["name"], dic_item["symbol"], self.get_company_size(dic_item['symbol'], 'MCI')) for dic_item in symbols]
        
        ord_values = sorted(values, key=operator.itemgetter(2),reverse=True)
        logger.info(f'biggest companies: {ord_values}')
        return ord_values[:n]

    def get_symbol_last_quote(self, symbol)-> dict:
        """
            Get data related to the last quote available from a company.

            Params:
                symbol: The NYSE symbol for a specific company.

            Return:
                Tuple (value, currency, date) for the last quote available
                for parameter.
        """

        data = self.get_api_data(symbol, self.FUNCTIONS.get('Global quote')).get('Global Quote')
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