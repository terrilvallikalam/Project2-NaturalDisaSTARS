from config import sqlpassword
from state_lookup import us_state_abbrev
from flask import Flask, jsonify
from flask import render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2
import pandas as pd

########### CONNECT TO DATABASE #############
engine = create_engine(f"postgres://postgres:{sqlpassword}@localhost:5432/tornado_db")
# engine = create_engine(f"postgres://ouvitqtn:{sqlpassword}@queenie.db.elephantsql.com:5432/ouvitqtn")
Base = automap_base()
Base.prepare(engine, reflect=True)
tornado_tbl = Base.classes.tornado_db
loss_tbl = Base.classes.losses
#############################################

app = Flask(__name__)

@app.route("/")
def index():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html")

@app.route("/charts")
def charts():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("charts.html")

@app.route("/tables")
def tables():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("tables.html")

@app.route("/map")
def HeatMap():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("map.html")


@app.route("/api/tornado_data/<state>")
def api(state = 'AL'):
    # postgres://ouvitqtn:{sqlpassword}@queenie.db.elephantsql.com:5432/ouvitqtn
    # db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
    db_conn = psycopg2.connect(host="localhost", database="tornado_db", user="postgres", password=f"{sqlpassword}", port="5432")
    db_cursor = db_conn.cursor()
    # write a statement that finds all the items in the db and sets it to a variable
    db_cursor.execute("SELECT * FROM tornado_db ORDER BY year ASC")
    tornado_table = db_cursor.fetchall()

    #list of dictionaries
    records = []
    for row in tornado_table:
        cols = db_cursor.description
        record = {}
        for i in range(len(cols)):
            record[cols[i].name] = row[i]
        records.append(record)
    db_conn.close()
    # render an index.html template and pass it the data you retrieved from the database
    return jsonify(records)

    # session = Session(engine)    
    # connect_string = f"postgres://postgres:{sqlpassword}@localhost:5432/tornado_db"
    # sql_engine = sqlalchemy.create_engine(connect_string)
    # if state == 'all': state = 'state'
    # query = f"SELECT * FROM tornado_db WHERE tornado_db.state='{state}'"
    # df = pd.read_sql_query(query, sql_engine)
    # exported_json = df.to_dict()
    # print(df)
    # results = session.query(f" * FROM tornado_tbl WHERE state = {state}")
    # print(results[0])

    # annual_summary = []

    # for result in results:
    #     annual_summary_dict = {}
    #     annual_summary_dict["tornado_num"] = result[1]
    #     annual_summary_dict["year"] = result[0]

    #     annual_summary_dict["injuries"] = int(result[2])
    #     annual_summary_dict["fatalities"] = int(result[3])
    #     annual_summary.append(annual_summary_dict)

    # session.close()

    # return jsonify(annual_summary)
    # return jsonify(exported_json)

    

@app.route("/api/annual_summary/<state>")
def annual_summary(state='all'):
    session = Session(engine)
    if state == 'all':
        group_by_columns = (tornado_tbl.year,)
    else:
        group_by_columns = (tornado_tbl.year,tornado_tbl.state)
    

    results = session.query(*group_by_columns, func.count(tornado_tbl.tornado_num.distinct()), func.sum(tornado_tbl.injury),\
        func.sum(tornado_tbl.fatalities))

    if state != 'all':
        results = results.filter_by(state=state)
    
    results = results.group_by(*group_by_columns).all()

    annual_summary = []

    for result in results:
        annual_summary_dict = {}
        annual_summary_dict["year"] = result[0]
        offset = 0
        if state != 'all':
            offset = 1
            annual_summary_dict["state"] = result[1]

        annual_summary_dict["tornado_sum"] = result[1+offset]
        annual_summary_dict["injuries"] = int(result[2+offset])
        annual_summary_dict["fatalities"] = int(result[3+offset])
        annual_summary.append(annual_summary_dict)

    session.close()

    return jsonify(annual_summary)

@app.route("/api/heat_map")
def heat_map():
    session = Session(engine)

    results = session.query(tornado_tbl.year, tornado_tbl.state, func.count(tornado_tbl.tornado_num.distinct()), func.sum(tornado_tbl.injury),\
        func.sum(tornado_tbl.fatalities)).\
        group_by(tornado_tbl.year, tornado_tbl.state).all()

    heat_map = []
    for year, state, torn_sum, injury, fatality in results:
        heat_map_dict = {}
        heat_map_dict["year"] = year
        heat_map_dict["state"] = state
        heat_map_dict["tornado_sum"] = torn_sum
        heat_map_dict["injuries"] = int(injury)
        heat_map_dict["fatalities"] = int(fatality)
        heat_map.append(heat_map_dict)
    session.close()

    return jsonify(annual_summary)

@app.route("/api/state_charts")
def state_charts():
    session = Session(engine)

    results = session.query(tornado_tbl.year, tornado_tbl.state, tornado_tbl.tornado_num, tornado_tbl.injury,\
        tornado_tbl.fatalities, tornado_tbl.miles_traveled, tornado_tbl.magnitude).all()

    state_summary = []
    for year, state, torn_sum, injury, fatality, miles, mag in results:
        state_summary_dict = {}
        state_summary_dict["year"] = year
        state_summary_dict["state"] = state
        state_summary_dict["tornado_sum"] = torn_sum
        state_summary_dict["injuries"] = injury
        state_summary_dict["fatalities"] = fatality
        state_summary_dict["miles_traveled"] = miles
        state_summary_dict["magnitude"] = mag
        state_summary.append(state_summary_dict)
    session.close()

    return jsonify(state_summary)

@app.route("/api/losses/<state>")
def losses(state="all"):
    session = Session(engine)
    if state == 'all':
        group_by_columns = (loss_tbl.year,)
    else:
        group_by_columns = (loss_tbl.year, loss_tbl.state)

    # results = session.query(*group_by_columns, func.count(tornado_tbl.tornado_num.distinct()), func.sum(tornado_tbl.injury),\
    #     func.sum(tornado_tbl.fatalities))

    results = session.query(*group_by_columns, func.count(loss_tbl.tornado_num.distinct()), func.sum(loss_tbl.injury),\
        func.sum(loss_tbl.fatalities), func.sum(loss_tbl.loss))

    if state != 'all':
        results = results.filter_by(state=state)
    
    results = results.group_by(*group_by_columns).all()

    loss_summary = []
    # for year, torn_sum, injury, fatality, loss in results:
    for result in results:
        loss_summary_dict = {}
        loss_summary_dict["year"] = result[0]
        offset = 0
        if state != "all":
            offset = 1
            loss_summary_dict["state"] = result[1]

        loss_summary_dict["tornado_sum"] = result[1+offset]
        loss_summary_dict["injuries"] = int(result[2+offset])
        loss_summary_dict["fatalities"] = int(result[3+offset])
        loss_summary_dict["losses"] = int(result[4+offset])
        loss_summary.append(loss_summary_dict)

    session.close()

    return jsonify(loss_summary)

# @app.route("/api/tornado_data_years")
# def api_year():
#     # postgres://ouvitqtn:BZiZY_67DtjmVHAZ7EtEAu5kMmDuUySX@queenie.db.elephantsql.com:5432/ouvitqtn
#     # db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
#     db_conn = psycopg2.connect(host="localhost", database="tornado_db", user="postgres", password=f"{sqlpassword}", port="5432")
#     db_cursor = db_conn.cursor()
#     # write a statement that finds all the items in the db and sets it to a variable
#     db_cursor.execute("SELECT * FROM tornado_db")
#     tornado_table = db_cursor.fetchall()

#     #list of dictionaries
#     records = []
#     for row in tornado_table:
#         cols = db_cursor.description
#         record = {}
#         for i in range(len(cols)):
#             record[cols[i].name] = row[i]
#         records.append(record)

#     year_options = {"year":[]}
#     year_list = []
#     i = 0
#     for record in records:
#         year = record["year"]
#         if (year not in year_list):
#             year_list.append(year)
#             i += 1
#     year_list.sort()
#     year_options["year"].append(year_list)
#     db_conn.close()
    
#     # render an index.html template and pass it the data you retrieved from the database
#     return jsonify(year_options)


@app.route("/api/tornado_data_state")
def api_state():
    # postgres://ouvitqtn:BZiZY_67DtjmVHAZ7EtEAu5kMmDuUySX@queenie.db.elephantsql.com:5432/ouvitqtn
    # db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
    db_conn = psycopg2.connect(host="localhost", database="tornado_db", user="postgres", password=f"{sqlpassword}", port="5432")
    db_cursor = db_conn.cursor()
    # write a statement that finds all the items in the db and sets it to a variable
    db_cursor.execute("SELECT * FROM tornado_db")
    tornado_table = db_cursor.fetchall()

    #list of dictionaries
    records = []
    for row in tornado_table:
        cols = db_cursor.description
        record = {}
        for i in range(len(cols)):
            record[cols[i].name] = row[i]
        records.append(record)

    state_options = {"state":[]}
    states = []
    for record in records:
        state = record["state"]

        if (state not in states):
            states.append(state)
            states.sort()
    state_options["state"].append(states)
    
    # https://gist.github.com/rogerallen/1583593
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
    state_names_dict = {"state_name":[], "abbr":[]}
    for abbr in states:
        state_names_dict["abbr"].append(abbr)
        state_names_dict["state_name"].append(abbrev_us_state[abbr])

    db_conn.close()

    # render an index.html template and pass it the data you retrieved from the database
    return jsonify(state_names_dict)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)