import pontotel
from flask import Flask
# from database import database


app = Flask(__name__)
# setup with the configuration provided by the user / environment
app.config.from_object('config')

pontotel.config(app)
# database.init_app(app)

if __name__ == "__main__":
	app.run()