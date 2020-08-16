from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pylab import rcParams
sns.set()
plt.rc('lines', linewidth=1)
rcParams['figure.figsize'] = 12,6
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
pd.set_option('display.max_colwidth', 40)
pd.options.display.float_format = '{:,.2f}'.format

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Use the Base class to reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
print(Base.classes.keys())

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
for measure in session.query(measurement).limit(10):
    print(measure.id, measure.station, measure.date, measure.prcp, measure.tobs)

# Earliest Date
date_conv = func.date(measurement.date, type_=Date)
early_date = session.query(date_conv).order_by(date_conv).first()
# print(early_date)

# Year Ago Date
year_ago = dt.date(2016,8,23)
# print(year_ago)

# Design a query to retrieve the last 12 months of precipitation data and plot the results
stmt = session.query(func.date(measurement.date).label('date'), measurement.prcp.label('precipitation')).\
                    filter(measurement.date > year_ago).\
                    order_by(measurement.date.desc()).statement
prcp_data = pd.read_sql_query(stmt, session.bind)
prcp_data = prcp_data.sort_values('date')
print(prcp_data.head(10))
# Use Pandas Plotting with Matplotlib to plot the data
prcp_data.set_index('date').plot()
plt.title("Precipitation Analysis over last 12 moths", size=14)
plt.ylabel('Inches')
# plt.savefig('images/prcp_analysis.png')
# Use Pandas to calcualte the summary statistics for the precipitation data
print(prcp_data.describe())

# Design a query to show how many stations are available in this dataset?
# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
stmt = session.query(measurement.station, func.count(measurement.station).label('total_number')).\
                    group_by(measurement.station).order_by(desc('total_number')).statement
prcp_station_data = pd.read_sql_query(stmt, session.bind)
active_station = prcp_station_data['station'][0]
print('Number of unique stations: ', len(prcp_station_data))
print(prcp_station_data)

# Using the station id from the previous query, calculate the lowest temperature recorded,
# highest temperature recorded, and average temperature of the most active station?
stmt = session.query(measurement.station, station.name, func.min(measurement.prcp).label('min_prcp'),
                    func.max(measurement.prcp).label('max_prcp'), func.avg(measurement.prcp).label('avg_prcp')).\
                    filter(measurement.station == station.station).\
                    group_by(measurement.station).filter(measurement.station == active_station).statement
active_station_data = pd.read_sql_query(stmt, session.bind)
print(active_station_data)

# Choose the station with the highest number of temperature observations
stmt = session.query(measurement.station, func.max(measurement.tobs).label('highest_number')).statement
tobs_data = pd.read_sql_query(stmt, session.bind)
tobs_station = tobs_data['station'][0]
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
stmt = session.query(func.date(measurement.date).label('date'), measurement.tobs.label('temp_observations')).\
                    filter(measurement.date > year_ago).filter(measurement.station == tobs_station).\
                    order_by(measurement.tobs.desc()).statement
tobs_station_data = pd.read_sql_query(stmt, session.bind)
tobs_station_data = tobs_station_data.set_index('date')
plt.figure(figsize=(10, 4.8))
sns.distplot(tobs_station_data)
plt.title(f"Distribution of Temperature Observations (tobs) for station {tobs_station} over the last 12 moths", size=14)
plt.ylabel('Frequency')
plt.xlabel('Temperature')
plt.show(sns)
# plt.savefig('images/tobs_analysis.png')
