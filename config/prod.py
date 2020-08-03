"""

AUTOR: jarquinsandra


"""

# config/prod.py
from .default import *
SECRET_KEY = '5e04a4955d8878191923e86fe6a0dfb24edb226c87d6c7787f35ba4698afc86e95cae409aebd47f7'
APP_ENV = APP_ENV_PRODUCTION
#Here you need to define the URI database, with the following data 'mysql+pymysql:user:password@host:port/database' you can change the data according to your needs
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:askl@localhost:3306/consensus'
