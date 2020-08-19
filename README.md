# SQLAlchemy-challenge: Climate Analysis FLASK App

Data Science and Visualization Boot Camp (Northwestern University)

![GitHub last commit](https://img.shields.io/github/last-commit/OlegRyzhkov2020/sqlalchemy-challenge)
![GitHub top language](https://img.shields.io/github/languages/top/OlegRyzhkov2020/sqlalchemy-challenge)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![HitCount](http://hits.dwyl.com/OlegRyzhkov2020/oil-project.svg)](http://hits.dwyl.com/OlegRyzhkov2020/sqlalchemy-challenge)
![GitHub watchers](https://img.shields.io/github/watchers/OlegRyzhkov2020/sql-challenge?label=Watch&style=social)
![GitHub followers](https://img.shields.io/github/followers/OlegRyzhkov2020?label=Follow&style=social)

![presentation_slide](images/about_page.png)

## Exploratory Analysis

![presentation_slide](images/box_plot.png)

![presentation_slide](images/prcp_analysis.png)

![presentation_slide](images/tobs_analysis.png)

## Bonus Analysis
* Total amount of rainfall per weather station for trip dates
![presentation_slide](images/bonus_query.png)

```python
session = Session(engine)
stmt = session.query(measurement.station, func.sum(measurement.prcp).label('tot_prcp'), station.name, station.latitude,
                     station.longitude, station.elevation).\
                    filter(measurement.station == station.station).group_by(measurement.station).\
                    filter((measurement.date >= new_start_trip) & (measurement.date <= new_end_trip) ).\
                    order_by(desc('tot_prcp')).statement
rainfall_data = pd.read_sql_query(stmt, session.bind)
print(rainfall_data.head(10))
```

![presentation_slide](images/daily_rainfall.png)

## FLASK app

![presentation_slide](images/stations_page.png)

![presentation_slide](images/period_page.png)
