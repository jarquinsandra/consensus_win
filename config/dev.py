"""

AUTOR: jarquinsandra


"""
# config/dev.py
from .default import *

APP_ENV = APP_ENV_DEVELOPMENT
#Here you need to define the URI database, with the following data 'mysql+pymysql:user:password@host:port/database' you can change the data according to your needs

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:askl@localhost:3306/consensus'
SQLALCHEMY_ECHO = True