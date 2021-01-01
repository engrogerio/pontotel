import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    ALPHA_API_KEY = '0S4J0EX4F61FJ0M'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
class ProductionConfig(Config):
    ENV="production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://xgsnvmas:G5t4_1dgrfM1_ccRbAJnDWOUwRIReKZn@tuffi.db.elephantsql.com:5432/xgsnvmas'
    SQLALCHEMY_DATABASE_PWD = 'G5t4_1dgrfM1_ccRbAJnDWOUwRIReKZn'
    
class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgres://xgsnvmas:G5t4_1dgrfM1_ccRbAJnDWOUwRIReKZn@tuffi.db.elephantsql.com:5432/xgsnvmas'
    SQLALCHEMY_DATABASE_PWD = 'G5t4_1dgrfM1_ccRbAJnDWOUwRIReKZn'