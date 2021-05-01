from config import sqlpassword
from state_lookup import us_state_abbrev
from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2


########### CONNECT TO DATABASE #############
engine = create_engine(f"postgres://postgres:{sqlpassword}@localhost:5432/tornado_db")
# engine = create_engine(f"postgres://ouvitqtn:{sqlpassword}@queenie.db.elephantsql.com:5432/ouvitqtn")
Base = automap_base()
Base.prepare(engine, reflect=True)
tornado_tbl = Base.classes.tornado_db
loss_tbl = Base.classes.losses
#############################################

#----------------- Loading Image ----------------#
UPLOAD_FOLDER = '../static'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#----------------- Route to Index ----------------#
@app.route("/")
def index():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html")

#----------------- Load Image to Index ----------------#
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return path

#----------------- Route to Charts ----------------#
@app.route("/charts")
def charts():
    return render_template("charts.html")

#----------------- Route to Table ----------------#
@app.route("/tables")
def tables():
    return render_template("tables.html")

#----------------- Route to Heatmap ----------------#
@app.route("/map")
def HeatMap():
    return render_template("map.html")


#----------------- API for Line Charts (Jaquelyns Charts) ----------------#
@app.route("/api/tornado_data/<state>")
def api(state = 'all'):
    session = Session(engine)
    if state == "all":
        results = session.query(tornado_tbl.year, tornado_tbl.tornado_num, tornado_tbl.state, tornado_tbl.magnitude, tornado_tbl.injury, tornado_tbl.fatalities, tornado_tbl.loss,\
            tornado_tbl.latitude, tornado_tbl.longitude, tornado_tbl.miles_traveled, tornado_tbl.width_yards)
    else:
        results = session.query(tornado_tbl.year, tornado_tbl.tornado_num, tornado_tbl.state, tornado_tbl.magnitude, tornado_tbl.injury, tornado_tbl.fatalities, tornado_tbl.loss,\
            tornado_tbl.latitude, tornado_tbl.longitude, tornado_tbl.miles_traveled, tornado_tbl.width_yards).filter_by(state=state).all()
    
    all_data = []
    for result in results:
        all_data_dict = {}
        all_data_dict["year"] = result[0]
        all_data_dict["tornado_num"] = result[1]
        all_data_dict["state"] = result[2]
        all_data_dict["magnitude"]=result[3]
        all_data_dict["injuries"] = result[4]
        all_data_dict["fatalities"] = result[5]
        all_data_dict["loss"] = result[6]
        all_data_dict["latitude"] = result[7]
        all_data_dict["longitude"] = result[8]
        all_data_dict["miles_traveled"] = result[9]
        all_data_dict["width_years"] = result[10]
        all_data.append(all_data_dict)
    session.close()

    return jsonify(all_data)


#----------------- API for Line Chart (Nicks Chart) ----------------#
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

#----------------- API for Map and Table ----------------#
@app.route("/api/tornado_data")
def data():
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


@app.route("/api/monthly_data/<state>")
def months_data(state='all'):
    session = Session(engine)
    
    if state == "all":
        results = session.query(tornado_tbl.month, func.count(tornado_tbl.tornado_num))\
            .group_by(tornado_tbl.month).order_by(tornado_tbl.month.desc()).all()

    if state != 'all':
        results = session.query(tornado_tbl.month, func.count(tornado_tbl.tornado_num))\
            .group_by(tornado_tbl.month).order_by(tornado_tbl.month.desc())\
            .filter_by(state=state).all()

    months_summary = []
    for months, count_months in results:
        monthly_data_dict = {}
        monthly_data_dict["months"] = months
        monthly_data_dict["month_count"] = count_months
        months_summary.append(monthly_data_dict)
    session.close()

    return jsonify(months_summary)

#----------------- API for Bar Chart (Nicks Chart) ----------------#
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

@app.route("/api/tornado_data_state")
def api_state():
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
    print(abbrev_us_state)
    state_names_dict = {"state_name":[], "abbr":[]}
    for abbr in states:
        state_names_dict["abbr"].append(abbr)
        state_names_dict["state_name"].append(abbrev_us_state[abbr])

    db_conn.close()

    return jsonify(state_names_dict)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)