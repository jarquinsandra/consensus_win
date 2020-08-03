"""

AUTOR: jarquinsandra


"""
import os
from app import create_app
from flask import render_template
from waitress import serve

#As its name says this module is intended as an entrypoint to the application, the app_settings module need to be loaded as an enviromental variable
#The wgsi server configurationis set here, right now is set to work on waitress, but it can be configured to work with gunicorn or other production server


#settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #Configuration for waitress just with Windows otherwise use the information above
    serve(app, host='0.0.0.0', port=5000)