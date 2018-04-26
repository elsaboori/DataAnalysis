import numpy as np
import pandas as pd
import datetime 
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)

#database connection
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#
Station = Base.classes.station
Measurements = Base.classes.measurements

#Create the session
session = Session(engine)

#first page


#The date of one year ago
last_year = datetime.today() - timedelta(days = 365)


#precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():

	last_year = datetime.today() - timedelta(days = 365)
	prcp = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date>last_year).all()

	#Creating the dictionary of the data
	total_prcp = []
	for day in prcp:
		row ={}
		row["date"] = prcp[0]
		row["prcp"] =prcp[1]
		total_prcp.append(row)
	return jsonify(total_prcp)
#The page will have the station name and station id
@app.route("/api/v1.0/station")
def station():
	station_query = session.query(Station.station, Station.name).all()
	station_list = []
	for st in station_query:
		row = {}
		row["station"] = station_query[0]
		row["name"] = station_query[1]
		station_list.append(station_query)
	return jsonify(station_list)

#The page will have the date and tobs from a year ago until the last day of data on the database
@app.route("/api/v1.0/tobs")
def tobs():
	tobs_data = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date>last_year).all()
	tobs_list = []
	for tob in tobs_data:
		row = {}
		row["date"] = tobs_data[0]
		row["tobs"] = tobs_data[1]
		tobs_list.append(row)
	return jsonify(tobs_list)

def min_max_avg_temp(start_date, end_date):
	min_temp = session.query(func.min(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).all()
	max_temp = session.query(func.max(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).all()
	avg_temp = session.query(func.avg(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).all()
	return[min_temp, max_temp,avg_temp]

#Min, max and average with start date, end date will be today's date
@app.route("/api/v1.0/<start>")
def trip_with_start_date(start_date):
	end_date = datetime.today()
	temp_info = min_max_avg_temp(start_date, end_date)
	return jsonify(temp_info)

#Min, max and average temperature with specified start and end date
@app.route("/api/v1.0/<start>/<end>")
def trip_with_start_end_date(start_date, end_date):
	temp_info = min_max_avg_temp(start_date, end_date)
	return jsonify(temp_info)

#first page with the link to all the APIs
@app.route("/")
def first_page():
	return(
		f"<br/>"
		f"Available APIs:<br/>"
		f"<br/>"
		f"<a href=""http://127.0.0.1:5000/api/v1.0/precipitation""> precipitation</a><br/>"
		f"<br/>"
		f"<a href=""http://127.0.0.1:5000/api/v1.0/station""> stations </a><br/>"
		f"<br/>"
		f"<a href=""http://127.0.0.1:5000/api/v1.0/tobs"">tobs</a><br/>"
		f"<br/>"
		f"<a href=""http://127.0.0.1:5000/api/v1.0/<start>"">"" Min, max and avg temperature with start date</a><br/>"
		f"<br/>"
		f"<a href=""http://127.0.0.1:5000/api/v1.0/<start>/<end>""> Min, max and avg temperature with start and end date</a>"
)
if __name__ == "__main__":
    app.run(debug=True)
