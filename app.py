#######################################################
# Configuration
#######################################################

from datetime import datetime
from flask import Flask, jsonify, render_template
from flask import redirect, request, url_for
from wtforms import Form, DateField, validators
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
# Input Data Class Object
#######################################################
class InputForm(Form):
    Start = DateField(label='date (MM/DD/YY)',
        format='%m/%d/%Y', default= datetime(2006, 1, 1),
        validators=[validators.InputRequired()])
    End = DateField(label='date (MM/DD/YY)',
        format='%m/%d/%Y', default= datetime(2016, 8, 23),
        validators=[validators.InputRequired()])

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
    return render_template("home.html")

# The /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return render_template("aboutUs.html")

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prcp_list = []
    for measure in session.query(measurement).limit(10):
        prcp_dict = {}
        print(measure.id, measure.station, measure.date, measure.prcp, measure.tobs)
        prcp_dict['station'] = measure.station
        prcp_dict[measure.date] = measure.prcp
        prcp_list.append(prcp_dict)
    session.close()

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations", methods=['POST', 'GET'])
def stations():
    print("Server received request for 'Stations' page...")
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all unique station names"""
    # Query all stations
    results = session.query(measurement.station).\
                group_by(measurement.station).order_by(measurement.station.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    return render_template(
        'stations.html',
        number = len(all_names),
        my_list = all_names
        )

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' page...")
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
    stat_name = f"The most active station in {last_year} is :{results[0]}"
    stat_rec = f"The number of records = {results[1]}"
    tobs_results = session.query(date_conv, measurement.tobs.label('temp_observations')).\
                        filter(extract('year', date_conv) == last_year).filter(measurement.station == act_station).\
                        order_by(measurement.tobs.desc()).limit(20).all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return render_template(
        'temperature.html',
        msg_1 = stat_name,
        msg_2 = stat_rec,
        my_list=tobs_results
        )

@app.route("/api/v1.0/period", methods=['GET','POST'])
def period():
    print("Server received request for 'Request for period' page...")
    form = InputForm(request.form)
    # Create our session (link) from Python to the DB
    session = Session(engine)
    if request.method == 'POST' and form.validate():
        date_conv = func.date(measurement.date, type_=Date)
        results = session.query(measurement.station, func.min(measurement.tobs),
                            func.max(measurement.tobs), func.avg(measurement.tobs)).\
                            filter((date_conv >= form.Start.data) & (date_conv <= form.End.data)).\
                            group_by(measurement.station).all()
        session.close()
    else:
        results = []

    return render_template('period.html', form = form, results= results)

# Run Server
if __name__ == "__main__":
    app.run(debug=True)
