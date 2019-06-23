# import numpy as np
# import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Database Setup

# engine = create_engine("sqlite:///db/data.sqlite")
# Base = automap_base()
# Base.prepare(engine, reflect=True)

# Happy = Base.classes.happiness
# GiNi = Base.classes.gini
# demo = Base.classes.demographic

# session = Session(engine)

# Flask Setup

app = Flask(__name__)
CORS(app)

# Database Setup
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or 'sqlite:///db/data.sqlite'
# db = SQLAlchemy(app)

# Flask Routes

@app.route("/")
def home():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    demo = Base.classes.demographic
    Happy = Base.classes.happiness
    GiNi = Base.classes.gini
    session = Session(engine)
    sel = [Happy.country,
            Happy.year,
            Happy.happiness]
    data = session.query(*sel).\
        order_by(Happy.happiness.desc()).all()
    return render_template("index.html", data=data)

@app.route("/api/demographic")
def demographic():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    demo = Base.classes.demographic
    session = Session(engine)
    results = session.query(demo).all()

    all_countries = []

    for i in results:
        demo_dict = {}
        demo_dict["country"] = i.country
        demo_dict["region_id"] = i.region_id
        demo_dict["gdp"] = i.gdp
        demo_dict["population"] = i.population
        demo_dict["lat"] = i.lat
        demo_dict["lon"] = i.lon
        all_countries.append(demo_dict)
   
    return jsonify(all_countries)
    

@app.route("/api/happiness")
def happiness():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Happy = Base.classes.happiness
    session = Session(engine)
    h_results = session.query(Happy).all()
    countries = []
    for i in h_results:
        happy_dict = {}
        happy_dict["country"] = i.country
        happy_dict["year"] = i.year
        happy_dict["happiness"] = i.happiness
        happy_dict["lat"] = i.lat
        happy_dict["lon"] = i.lon
        countries.append(happy_dict)
    return jsonify(countries)


@app.route("/api/gini")
def gini():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    GiNi = Base.classes.gini
    session = Session(engine)
    g_results = session.query(GiNi).all()
    countries_gini = []
    for i in g_results:
        gini_dict = {}
        gini_dict["country"] = i.country
        gini_dict["country_code"] = i.country_code
        gini_dict["year"] = i.year
        gini_dict["gini"] = i.gini
        gini_dict["lat"] = i.lat
        gini_dict["lon"] = i.lon
        countries_gini.append(gini_dict)
    return jsonify(countries_gini)


@app.route("/api/geographic")
def geographic():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Geo = Base.classes.geo
    session = Session(engine)
    geo_results = session.query(Geo).all()
    countries_geo = []
    for i in geo_results:
        geo_dict = {}
        geo_dict["country"] = i.country
        geo_dict["country_init"] = i.init
        geo_dict["lat"] = i.lat
        geo_dict["lon"] = i.lon
        countries_geo.append(geo_dict)
    return jsonify(countries_geo)

@app.route("/api/grouped_data")
def group():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Join = Base.classes.join
    session = Session(engine)
    joined_results = session.query(Join).all()
    countries_joined = []
    for i in joined_results:
        joined_dict = {}
        joined_dict["country"] = i.country
        joined_dict["country_code"] = i.country_code
        joined_dict["region_id"] = i.region_id
        joined_dict["gdp"] = i.gdp
        joined_dict["population"] = i.population
        joined_dict["lat"] = i.lat
        joined_dict["lon"] = i.lon
        joined_dict["gini"] = i.gini
        joined_dict["happiness"] = i.happiness
        joined_dict["gdpPerCap"] = i.gdpPerCap
        countries_joined.append(joined_dict)
    return jsonify(countries_joined)

@app.route("/api/grouped_data/<region_id>")
def region(region_id):
    canonicalized = region_id.replace(" ", "").lower()
    
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Join = Base.classes.join
    session = Session(engine)
    joined_results = session.query(Join).all()
    countries_joined = []
    for i in joined_results:
        joined_dict = {}
        joined_dict["country"] = i.country
        joined_dict["country_code"] = i.country_code
        joined_dict["region_id"] = i.region_id
        joined_dict["gdp"] = i.gdp
        joined_dict["population"] = i.population
        joined_dict["lat"] = i.lat
        joined_dict["lon"] = i.lon
        joined_dict["gini"] = i.gini
        joined_dict["happiness"] = i.happiness
        joined_dict["gdpPerCap"] = i.gdpPerCap
        
        search_term = joined_dict["region_id"].replace(" ", "").lower()

        if search_term == canonicalized:
            countries_joined.append(joined_dict)
    
    return jsonify(countries_joined)

@app.route("/api/happiness_explain")
def explain():
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Explain = Base.classes.explain
    session = Session(engine)
    explain_results = session.query(Explain).all()
    countries_explain = []
    for i in explain_results:
        explain_dict = {}
        explain_dict["country"] = i.country
        explain_dict["happiness"] = i.happiness
        explain_dict["gdpPerCap"] = i.gdppercap
        explain_dict["social"] = i.social
        explain_dict["health"] = i.health
        explain_dict["freedom"] = i.freedom
        explain_dict["generosity"] = i.generosity
        explain_dict["corruption"] = i.corruption
        explain_dict["residual"] = i.residual
        countries_explain.append(explain_dict)
    return jsonify(countries_explain)


@app.route("/api/happiness_explain/<country>")
def explainbycounty(country):
    canonicalized = country.replace(" ", "").lower()
    
    engine = create_engine("sqlite:///db/data.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Explain = Base.classes.explain
    session = Session(engine)
    explain_results = session.query(Explain).all()
    countries_explain = []
    for i in explain_results:
        explain_dict = {}
        explain_dict["country"] = i.country
        explain_dict["happiness"] = i.happiness
        explain_dict["gdpPerCap"] = i.gdppercap
        explain_dict["social"] = i.social
        explain_dict["health"] = i.health
        explain_dict["freedom"] = i.freedom
        explain_dict["generosity"] = i.generosity
        explain_dict["corruption"] = i.corruption
        explain_dict["residual"] = i.residual
    
        search_term = explain_dict["country"].replace(" ", "").lower()

        if search_term == canonicalized:
            countries_explain.append(explain_dict)

    return jsonify(countries_explain)



if __name__ == "__main__":
    app.run(debug=True)