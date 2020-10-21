import os
import json
from flask import Flask, render_template, request, jsonify
from alpha import Alpha, logger


app = Flask(__name__)
alpha = Alpha()

@app.route('/pontotel',  methods=['GET'])
def index():
    """

    """
    if request.method == 'GET':
        logger.info('Requesting ibov data.')
        ibov_points = f"Bovespa Index: {alpha.get_symbol_last_quote('IBOV11.SAO')['value']}"
        logger.debug(f'Bovespa response: {ibov_points}')
        logger.info('Requesting biggest companies.')
        biggest = alpha.get_n_biggest_brazilian_companies(10)
        logger.debug(f'Biggest companies {biggest}')
        try:
            return  render_template('index.html', ibov=ibov_points, biggest=biggest, success=None)
        except Exception as e:
            logger.error(f'Rendering template index.html returns error {e}')
            raise e

@app.route('/pontotel/show',  methods=['POST'])
def get_value():
    symbol = request.form['value']
    
    # TODO: if necessary, start a thread here...
    result = alpha.get_symbol_last_quote(symbol)
    logger.info(result)
    value = f"{symbol} value on {result['date']} => {result['currency']} {result['value']}"

    return {"success": True , "value": value}

if __name__ == "__main__":
	app.run()
