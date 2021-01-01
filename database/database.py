from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def config(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/alpha"
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    
    def __repr__(self):
        return f"<User {self.user_name}>"

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<Company {self.name}>"

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10)) 
    company = db.relationship("Company", backref=SQLAlchemy("share", uselist=False))
    def __repr__(self):
        return f"<Share {self.symbol}>"

@app.cli.command()
def createdb():
    db.create_all()

def init_app(app):
    db.init_app(app)
