# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify
from sqlalchemy import and_, or_



#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()

Base.prepare(autoload_with=engine)

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    yearb4 = '2016-08-23'
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= yearb4).all()
    session.close()
    # print(results)
    dict1 = {}
    for date, prcp in results:
        dict1[date] = prcp
    return jsonify(dict1)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    list1 = [station.station for station in results]
    return jsonify(list1)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    yearb4 = '2016-08-23'
    results = session.query(measurement).filter(and_(measurement.date >=yearb4,measurement.station=="USC00519281" ))
    session.close()
    list1 = [measurement.tobs for measurement in results]
    return jsonify(list1)
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    startresults = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    list1 = list(np.ravel(startresults))

    return jsonify(list1)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session = Session(engine)
    startresults = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    list1 = list(np.ravel(startresults))

    return jsonify(list1)





    