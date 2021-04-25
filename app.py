from config import sqlpassword
import psycopg2
from state_lookup import us_state_abbrev
from flask import Flask, jsonify
from flask import render_template

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


@app.route("/api/tornado_data")
def api():
    # postgres://ouvitqtn:BZiZY_67DtjmVHAZ7EtEAu5kMmDuUySX@queenie.db.elephantsql.com:5432/ouvitqtn
    db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
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
    db_conn.close()
    
    # render an index.html template and pass it the data you retrieved from the database
    return jsonify(records)

@app.route("/api/tornado_data_years")
def api_year():
    # postgres://ouvitqtn:BZiZY_67DtjmVHAZ7EtEAu5kMmDuUySX@queenie.db.elephantsql.com:5432/ouvitqtn
    db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
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

    year_options = {"year":[]}
    year_list = []
    i = 0
    for record in records:
        year = record["year"]
        if (year not in year_list):
            year_list.append(year)
            i += 1
    year_list.sort()
    year_options["year"].append(year_list)
    db_conn.close()
    
    # render an index.html template and pass it the data you retrieved from the database
    return jsonify(year_options)



@app.route("/api/tornado_data_state")
def api_state():
    # postgres://ouvitqtn:BZiZY_67DtjmVHAZ7EtEAu5kMmDuUySX@queenie.db.elephantsql.com:5432/ouvitqtn
    db_conn = psycopg2.connect(database="ouvitqtn", user="ouvitqtn", password=f"{sqlpassword}", host="queenie.db.elephantsql.com", port="5432")
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
    app.run(debug=True)