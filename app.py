#--------------------
# Import dependencies
#--------------------
import datetime as dt
import numpy as np
import pandas as pd

# Import sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

# Set Flask engine
# Note: check_same_thread set to False
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# Reflect sqlite database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reference the sqlite tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link
session = Session(engine)

# Define Flask app
app = Flask(__name__)


#----------------------
# Create welcome route
#----------------------
@app.route("/")
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!<br>
        <br>
        Available Routes:<br>
        /api/v1.0/precipitation<br>
        /api/v1.0/stations<br>
        /api/v1.0/tobs<br>
        /api/v1.0/temp/start/end
        ''')

#---------------------------
# Create precipitation route
#---------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp). \
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#----------------------
# Create stations route
#----------------------
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#------------------
# Create tobs route
#------------------
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs). \
        filter(Measurement.station == 'USC00519281'). \
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#-------------------------
# Create temperature route
#-------------------------
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



#-------------------------
# Activate flask
#-------------------------

# Within IDE integrated terminal run the app by entering: python -m flask run
# See documentation: https://code.visualstudio.com/docs/python/tutorial-flask
# 
# OR
# 
# Uncomment the following two lines before runing code in terminal:
# if __name__ == "__main__":
#     app.run(debug=True)
#
#  -------------------
#
# Within anaconda prompt terminal
# 1) Navigate to file path
# 2) Enter:
#       set FLASK_APP = app.py
#       set FLASK_ENV = development
#       flask run
