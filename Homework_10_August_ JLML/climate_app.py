import pandas as pd
import matplotlib.pyplot as plt

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func

from flask import Flask,jsonify

from datetime import datetime as dt

import numpy as np

#IMPORT DATA
hawaii_input="hawaii.sqlite"

#PREP
Base=automap_base()
engine=create_engine(f"sqlite:///{hawaii_input}")
Base.prepare(engine,reflect=True)

Mmt=Base.classes.measurement
Stn=Base.classes.station




app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to Climate Analysis App!</br>"
        f"Available Routes:</br>"
        f"- Precipitation:</br>"
        f"/api/v1.0/precipitation</br></br>"
        f"- Stations:</br>"
        f"/api/v1.0/stations</br></br>"
        f"- Temperature Observations:</br>"
        f"/api/v1.0/tobs</br></br></br>"
        f"-Start date:</br>"
        f"/api/v1.0/<start></br></br>"
        f"-Date range:</br>"
        f"/api/v1.0/<start>/<end></br></br>"
    )
@app.route("/api/v1.0/precipitation")
def precipitaion():
    session=Session(engine)
    
#12M Info
    Months12=session.query(Mmt.id,Mmt.station,Mmt.date,Mmt.prcp,Mmt.tobs).\
    filter(Mmt.date>"2016-08-22").\
    order_by(Mmt.date.desc()).all()

#12M Average Precipitation Info
    Months12_prcp=session.query(Mmt.date,func.avg(Mmt.prcp)).\
        filter(Mmt.date>"2016-08-22").\
        group_by(Mmt.date).\
        order_by(Mmt.date.desc()).all()

    session.close()

    daily_averages=[]
    for date,prcp in Months12_prcp:
        date_dict={}
        date_dict[date]=prcp
        daily_averages.append(date_dict)

    return jsonify(daily_averages)


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)

    stations=session.query(Stn.name).all()

    session.close()

#Stations available
    all_stations=list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
#12M Average Precipitation Info
    session=Session(engine)

    Months12_tobs=session.query(Mmt.date,Mmt.station,Mmt.tobs).\
        filter(Mmt.date>"2016-08-22").\
        group_by(Mmt.date).\
        order_by(Mmt.date.desc()).all()

    session.close()

    temperatures=list(np.ravel(Months12_tobs))
    return jsonify(temperatures)

if __name__ == "__main__":
        app.run(debug=True)