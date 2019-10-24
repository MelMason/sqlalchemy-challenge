import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create an app, being sure to pass __name__
app = Flask(__name__)

# Available Routes

@app.route("/")
def welcome():
    session = Session(engine)
    return (
        f"Welcome to the Hawaii Weather Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all date and precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp in results:
        all_dates_dict = {}
        all_dates_dict["date"] = date
        all_dates_dict["prcp"] = prcp
        all_dates.append(all_dates_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    staions = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()


    return jsonify(staions)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs= session.query(Measurement.tobs).\
    filter(Measurement.date >=  '2016-08-23').filter(Measurement.date <= '2017-08-23').all()

   

    session.close()

    return jsonify(tobs)



@app.route("/api/v1.0/Measurement/date/<start>")
def start_date(start):
    session = Session(engine)
    
    start_stats = session.query((func.min(Measurement.tobs)),(func.max(Measurement.tobs)),\
              (func.avg(Measurement.tobs))).filter(Measurement.date >= "start").all()
    session.close()
    
    return jsonify(start_stats)

@app.route("/api/v1.0/Measurement/date/<start>/<end>")
def start_end_date(start_end):
    session = Session(engine)
    
    start_end_stats = session.query((func.min(Measurement.tobs)),(func.max(Measurement.tobs)),\
              (func.avg(Measurement.tobs))).filter(Measurement.date >= "start").\
              filter(Measurement.date <= "end").all()
    session.close()
    
    return jsonify(start_end_stats)
    
if __name__ == "__main__":
    app.run(debug=True)