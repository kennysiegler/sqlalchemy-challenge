# Import the dependencies.
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect an existing database into a new model

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table


# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    
    print('User touched down on the main page')
    return (f"Hello! Welcome to my sqlalchemy challenge<br />"
            f"The following endpoints are available:  <br />"
            f"/api/v1.0/precipitation<br />"
            f"/api/v1.0/stations <br />"
            f"/api/v1.0/tobs <br />"
            f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
           )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    print('User has visited the precipitation endpoint')
    
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > year_prior).all()
    session.close()
    all_precip = []
    for date, prcp in results:
        data = {date:prcp}
        all_precip.append(data)
    
    return jsonify(all_precip)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    print("User has landed on the stations endpoint")
    data = session.query(Station)
    stations = []
    for row in data:
        station_dict ={}
        station_dict["ID"] =row.id 
        station_dict["Station"] = row.station,
        station_dict["Name"] = row.name
        station_dict["Lat"] = row.latitude 
        station_dict["Lon"] = row.longitude  
        station_dict["Elevation"] = row.elevation
           
        stations.append(station_dict)
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    start_date = '2016-08-18'
    end_date = '2017-08-18'
    station = 'USC00519397'
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station).filter(Measurement.date > start_date).all()
    
    data_list = []
    for date, tobs in data:
        data_dict = {}
        data_dict['date'] = date
        data_dict['tobs'] = tobs
        data_list.append(data_dict)
    return jsonify(data_list)
           

if __name__ == "__main__":
    app.run(debug=True)
