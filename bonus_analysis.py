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

# Date trip
start_trip = '2012-02-28'
end_trip = '2012-03-05'

# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax
# for your trip using the previous year's data for those same dates.
start_trip = datetime.strptime(start_trip, "%Y-%m-%d")
new_start_trip = start_trip + dt.timedelta(days=-365)
end_trip = datetime.strptime(end_trip, "%Y-%m-%d")
new_end_trip = end_trip + dt.timedelta(days=-365)

# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
session = Session(engine)
stmt = session.query(measurement.station, func.sum(measurement.prcp).label('tot_prcp'), station.name, station.latitude,
                     station.longitude, station.elevation).\
                    filter(measurement.station == station.station).group_by(measurement.station).\
                    filter((measurement.date >= new_start_trip) & (measurement.date <= new_end_trip) ).\
                    order_by(desc('tot_prcp')).statement
rainfall_data = pd.read_sql_query(stmt, session.bind)
print(rainfall_data.head(10))

# Create a query that will calculate the daily normals
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.

    Args:
        date (str): A date string in the format '%m-%d'

    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax

    """

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", measurement.date) == date).all()

print(daily_normals("01-01"))

# Create list of trip dates
num_days = abs((new_end_trip - new_start_trip).days)
print("Trip, number of days:", num_days)
date_list = [new_start_trip]
for i in range(1,num_days):
    new_day = date_list[0] + dt.timedelta(days=i)
    date_list.append(new_day)
print(date_list)

# Create Data Frame with daily_normals
trip_pd = pd.DataFrame()
d_list = []
min_list = []
avg_list = []
max_list = []
for i in range(len(date_list)):
    y = date_list[i].strftime('%y')
    m = date_list[i].strftime('%m')
    d = date_list[i].strftime('%d')
    d_list.append(y + '-' + m + '-' + d)
    date_list[i] = m + '-' + d
    day_norm = daily_normals(date_list[i])[0]
    min_list.append(day_norm[0])
    avg_list.append(day_norm[1])
    max_list.append(day_norm[2])
trip_pd = pd.DataFrame({'Trip_Date': d_list, 'Temp_min': min_list,
                        'Temp_avg': avg_list, 'Temp_max': max_list})
trip_pd = trip_pd.set_index('Trip_Date')
print(trip_pd)

ax = trip_pd.plot.area(stacked=False)
ax.set_title('Daily Rainfall Average over Trip Dates')
ax.set_ylabel('Temperature', fontsize='medium')
plt.show()
