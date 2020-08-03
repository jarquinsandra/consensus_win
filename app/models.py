"""

AUTOR: jarquinsandra


"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import db
import datetime
#Here we create all the tables needed for the consensus to be calculated, this tables are replaced everytime the application is run. 
#This table stores the consensus spectra calculated from the temp_all_spectra  table

class TempSpectra(db.Model):
	__tablename__= 'temp_spectra'
	id = db.Column(db.Integer, primary_key = True)
	mz = db.Column(db.Float, unique=False, nullable=False)
	int_rel = db.Column(db.Float, unique=False, nullable=False)

#This table contains all the spectra that are loaded into the app before the calculation

class TempSpectra2(db.Model):
	__tablename__= 'temp_all_spectra'
	id = db.Column(db.Integer, primary_key = True)
	mz = db.Column(db.Float, unique=False, nullable=False)
	intensity = db.Column(db.Float, unique=False, nullable=False)
