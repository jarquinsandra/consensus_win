"""

AUTOR: jarquinsandra


"""
from . import db_manager
from io import BytesIO, StringIO
import os
import io
import urllib.request
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from flask import url_for, redirect, render_template, request, url_for, make_response, flash, Response, send_file, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from .forms import CalculateConsensusForm
from .forms import DownloadFile
from .forms import NormalizationForm
from app.models import TempSpectra
from app.models import TempSpectra2
from bokeh.plotting import figure
from bokeh.embed import components
import sqlalchemy
from app import db
from werkzeug.utils import secure_filename
import zipfile
from zipfile import ZipFile
engine = create_engine('mysql+pymysql://root:root@localhost:3306/consensus')

#General function for binning
def slidefunc (data,window,step):
    "This function do a binning sliding window using window and step parameters, data must contain the first two colums as mz and relative intensity. The first column name has to be mz and data must be previously ordered by mz"
    minmz = data['mz'].min()
    maxmz = data['mz'].max()
    bins = []
    minbin = minmz+window
    maxbin = maxmz-window
    bins= np.arange(minbin,maxbin,step)
        
        #minus 1 correction for python index
    m = len(bins)-2
    i = 0
    j = 0
    first = 0
    n = 0
    accum = 0
    mzbins = pd.DataFrame(bins, columns= ['bins'])
    mzbins['int_rel'] = np.nan
    mzbins['samples'] = np.nan
    data = data.sort_values(by=['mz'])
    while (j<=m):
        lower = bins[j]- window
        upper = bins[j]+ window
        while data.iat[i,0]<= lower:
            i = i + 1
        first = i
        while data.iat[i,0]< upper:            
            accum = accum + data.iat[i,1]
            n = n + 1
            i = i + 1
        if (n):
            mzbins.iat[j,1] = accum/n
            mzbins.iat[j,2] = n
            #a = accum/n
            #b = n
            accum = 0 
            n = 0
        j = j + 1
        i = first
    mzbins = mzbins.fillna(0)   
    return mzbins
     
#Function for calculation of mean intensity and mass
def peak_search(dataframe, noise_level): 
    peaks = pd.DataFrame(columns=['mz','int_rel'])
    peak_search_active = 0
    top = len(dataframe)
    for s in range (1, top):
        mzbin_int = dataframe.iloc[s]['int_rel']
        if mzbin_int>0 and peak_search_active==0 :
            peak_start=s
            peak_search_active=1
        if mzbin_int==0 and peak_search_active ==1:
            peak_stop =s-1
            peak_mz = dataframe[['bins']].iloc[[peak_start,peak_stop]].mean()
            peak_int = dataframe[['int_rel']].iloc[[peak_start,peak_stop]].mean()
            peak_means = pd.DataFrame([[peak_mz.iloc[0],peak_int.iloc[0]]], columns=['mz','int_rel'])
            if peak_int.iloc[0] > noise_level:
                peaks = peaks.append(peak_means, ignore_index=True)
            peak_search_active = 0
    return peaks


#route to calculate consensus
@db_manager.route('/custome_consensus', methods = ['GET','POST'])
def calculate_consensus():
    #obtains information from the form (user)
    form = CalculateConsensusForm()
    window = form.window.data
    step = form.step.data
    noise_level = form.noise_level.data
    peak_presence = form.peak_presence.data
     
    if form.validate_on_submit():
        f =form.file.data
        mylist = []
        content = pd.DataFrame()
        i = 0 
        #loops all the files to obtain data, change skiprows if your data doesn't have any information previous to numerical data, a number 4 was set as a compromise but it dismisses sometimes the first masses, which are not usually relevant for the consensus spectra calculation, for more accuracy your files should not contain any more than numerical data and skiprows should be set to 0
        
        for file in f:
            filename = secure_filename(file.filename)
            content_loop = pd.read_csv(file, sep="\t", header=None, skip_blank_lines=True, skiprows=4)
            mylist.append(filename)
            content_loop = content_loop.iloc [:,0:2]
            content_loop=content_loop.rename(columns = {0:'mz',1:'intensity'})
            content_loop['filename'] = filename
            content_loop =content_loop.dropna(axis=1, how='all')
            content = content.append(content_loop, ignore_index=True)
            i+=1 
        content['species'] = content['filename'].str.split('_').str[0]
        content['wd'] = content['filename'].str.split('_').str[1]
        content['origin'] = content['filename'].str.split('_').str[2]
        content = content.dropna()
        content['origin'] = content.origin.replace({'.txt':''}, regex=True)
        content = content.drop(['filename','origin','wd','species'], axis=1)
        content = content.sort_values(by=['mz'])
        content = content.reset_index(drop=True)       
        cut = i*peak_presence
        
        slidexy=slidefunc(content,window,step)
        slidexy.loc[slidexy['samples'] < cut, 'int_rel'] = 0
        peaks = pd.DataFrame(columns=['mz','int_rel'])
        peak_search_active = 0
        top = len(slidexy)
        for s in range (1, top):
            mzbin_int = slidexy.iloc[s]['int_rel']
            if mzbin_int>0 and peak_search_active==0 :
                peak_start=s
                peak_search_active=1
            if mzbin_int==0 and peak_search_active ==1:
                peak_stop =s-1
                peak_mz = slidexy[['bins']].iloc[[peak_start,peak_stop]].mean()
                peak_int = slidexy[['int_rel']].iloc[[peak_start,peak_stop]].mean()
                peak_means = pd.DataFrame([[peak_mz.iloc[0],peak_int.iloc[0]]], columns=['mz','int_rel'])                
                if peak_int.iloc[0] > noise_level:
                    peaks = peaks.append(peak_means, ignore_index=True) 
                
                peak_search_active = 0
        db.session.query(TempSpectra).delete()
        db.session.commit()
        db.session.query(TempSpectra2).delete()
        db.session.commit()
        peaks.to_sql('temp_spectra', con = db.engine,  if_exists='append', index=False)
        content.to_sql('temp_all_spectra', con = db.engine, if_exists='append', index=False)       
        return redirect(url_for('db_manager.show_dashboard'))
     
    return render_template('custome_consensus.html', form=form)
#route to plot the consensus spectra
@db_manager.route('/dashboard/', methods = ['GET','POST'])
def show_dashboard():
    form = DownloadFile() 
    plots = []
    plots.append(make_plot())
    ref_spectra=pd.read_sql_table('temp_spectra', con= db.engine)
    
    if request.method == 'POST':
        resp = make_response(ref_spectra.to_csv(sep="\t", index=False))
        resp.headers["Content-Disposition"] = 'attachment; filename= "consensus_spectra.txt"'
        resp.headers["Content-Type"] = "text/csv"
        
        return resp
    return render_template('dashboard.html', plots=plots, form=form)
#route to draw the plot
def make_plot():
    
    ref_spectra=pd.read_sql_table('temp_spectra', con= db.engine)
    all_spectra= pd.read_sql_table('temp_all_spectra', con= db.engine)
    x2=ref_spectra['mz']
    y2=ref_spectra['int_rel']
    x = all_spectra['mz']
    y = all_spectra['intensity']
    TOOLTIPS = [("mass", "$x"), ("intensity", "$y")]
    plot = figure(plot_height=300, sizing_mode='scale_width', x_axis_label= 'm/z',
    y_axis_label= 'int %[BP]', tooltips=TOOLTIPS)
    plot.circle(x, y, line_width=1, alpha=0.4)
    plot.segment(x2, y2, x2, 0 , color="red", line_width=1)
    plot.segment(0,0,1000,0,color='black',line_width=1)
    #plot.circle(x2,y2, color = 'red', line_width=0.5)
    script, div = components(plot)
    db.session.query(TempSpectra).delete()
    db.session.commit()
    db.session.query(TempSpectra2).delete()
    db.session.commit()
    return script, div

#Define normalization of files when needed
@db_manager.route('/normalization', methods=['GET','POST'])
def normalize():
    form = NormalizationForm()
    if form.validate_on_submit():
        f =form.file.data
        
        content = pd.DataFrame()
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as csv_zip:
            for file in f:
                filename = secure_filename(file.filename)
                #Read file form txt files
                content_loop = pd.read_csv(file, sep="\t", header=None, skip_blank_lines=True, skiprows=0)
                #select the two columns corresponding to mz and intensity
                content_loop = content_loop.iloc [:,0:2]
                #rename columns to mz and intensity
                content_loop=content_loop.rename(columns = {0:'mz',1:'intensity'})
                #Drop all NA values, there should be none but just in case
                content_loop =content_loop.dropna(axis=1, how='all')
                #Obtains the maximum intensity value for the file
                max_100 = content_loop['intensity'].max()
                #calculates the relative intensity with the max value for each mz value
                content_loop['intensity2'] = (content_loop['intensity']*100)/max_100
                #delete absolute intensity from the file
                del content_loop['intensity']
                content_loop=content_loop.rename(columns= {'intensity2':'intensity'})
                data = zipfile.ZipInfo(filename)
                data.compress_type = zipfile.ZIP_DEFLATED
                csv_zip.writestr(data, content_loop.to_csv(sep="\t", index=False))
        memory_file.seek(0)    
        
        return send_file(memory_file, attachment_filename='normalized.zip', as_attachment=True)
            

        
    return render_template('normalization.html', form=form)
#information route
@db_manager.route('/info')
def info():
    return render_template('tutorial.html')
#sliding window explanation route
@db_manager.route('/sliding_window')
def sliding_window():
    return render_template('sliding_window.html')     
