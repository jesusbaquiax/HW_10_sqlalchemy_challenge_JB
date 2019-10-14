import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, url_for,jsonify,request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Type a start date in fortmat YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
   # Convert list of tuples into normal list
    prcp_list = list(np.ravel(results))
    return jsonify(prcp_list)
        
    
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    stations=session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>="2016-08-23").all()
    session.close()
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_date(start_date,end_date):
   session=Session(engine)
   tempS_E=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(func.strftime(Measurement.date)>=start_date,func.strftime(Measurement.date)<=end_date).all()
   session.close()
   temps = list(np.ravel(tempS_E))
   return jsonify(temps)

@app.route("/api/v1.0/<s_date>")
def s_date(s_date):
   session=Session(engine)
   tempS=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(func.strftime(Measurement.date)>=s_date).all()
   session.close()
   temps_list = list(np.ravel(tempS))
   return jsonify(temps_list)
   
 
if __name__=='__main__':
    app.run(debug=True)