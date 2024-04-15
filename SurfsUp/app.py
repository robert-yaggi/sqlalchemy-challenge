# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes"""
    return ( 
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
        f'Note: to access, start and end date format: yyyy-mm-dd/yyyy-mm-dd'
    )

#route for precipitation
# Create a route that queries precipitation levels and dates 
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
        

    # Create a dictionary from the row data and append to precipitation list
    precipitation_list = []
    for  date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict[date] = prcp 
        precipitation_list.append(date_prcp_dict)

    return jsonify(precipitation_list)
    
#route for stations
@app.route('/api/v1.0/stations<br/>')
def stations():
    #Create session link 
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()

    #Convert to a list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Tobs route
@app.route('/api/v1.0/tobs<br/>')
def temperature():

    #Query the dates and temperature of the most active station for the previous year. 
    session = Session(engine)
    year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= year_date).all()
    session.close()

    #Return a Json list of temperatures for the previous year. 
    all_temps=[]
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        all_temps.append(tobs_dict)
    return jsonify(all_temps)

#Route for start and start/end
@app.route('/api/v1.0/start<br/>')
def get_t_start(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    all_tobs = []
    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max 
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route('/api/v1.0/start/end<br/>')
def temp_start_stop(start,stop):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    all_tobs = []
    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max 
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug = True)