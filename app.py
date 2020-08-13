#######################################################
# Configuration
#######################################################

from datetime import datetime
from flask import Flask, request, jsonify, render_template

import numpy as np
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#######################################################
# Database Setup
#######################################################

DB_URL = "sqlite:///Resources/hawaii.sqlite"
engine = create_engine(DB_URL)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#######################################################
# Flask Setup
#######################################################
# Init app
app = Flask(__name__)

#######################################################
# Flask Routes
#######################################################

# Provide all available routes on the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end>"
    )


# The /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prcp_list = []
    for measure in session.query(measurement).limit(10):
        prcp_dict = {}
        print(measure.id, measure.station, measure.date, measure.prcp, measure.tobs)
        prcp_dict['station'] = measure.station
        prcp_dict[measure.date] = measure.prcp
        prcp_list.append(prcp_dict)
        # print(measure.id, measure.station, measure.date, measure.prcp, measure.tobs)
    session.close()

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all unique station names"""
    # Query all stations
    results = session.query(measurement.station).\
                group_by(measurement.station).order_by(measurement.station.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs for the most active station over the last year """
    # Query tobs for the active station over the year
    date_conv = func.date(measurement.date, type_=Date)
    last_year = 2017
    results = session.query(measurement.station, func.count(measurement.station).label('total_number')).\
                        filter(extract('year', date_conv) == last_year).\
                        group_by(measurement.station).order_by(desc('total_number')).first()
    act_station = results[0]
    station_result = f"The most active station in {last_year} is :{results[0]}\n with the number of records = {results[1]}"
    tobs_results = session.query(date_conv, measurement.tobs.label('temp_observations')).\
                        filter(extract('year', date_conv) == last_year).filter(measurement.station == act_station).\
                        order_by(measurement.tobs.desc()).all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
