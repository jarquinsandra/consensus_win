"""

AUTOR: jarquinsandra


"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, MultipleFileField, FileField,FloatField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length

#This form is for the calculation of the consensus spectra
class CalculateConsensusForm(FlaskForm):
    file = MultipleFileField('txt files')
    submit_file = SubmitField('calculate consensus')
    step = FloatField('bin', default=0.003)
    window = FloatField('window', default= 0.01)
    noise_level = FloatField('noise level', default = 1.0)
    peak_presence = FloatField('peak presence', default = 0.5)
#Form for download the file obtained in the calculation spectra
class DownloadFile(FlaskForm):
    submit = SubmitField('Download spectrum')
#form for normalization route
class NormalizationForm(FlaskForm):
    file = MultipleFileField('Input Files')
    submit_file = SubmitField('Normalize')

