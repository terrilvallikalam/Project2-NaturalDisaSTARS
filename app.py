from config import sqlpassword
import psycopg2
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
    # f"postgresql://postgres:{sqlpassword}@localhost:5432/tornado_db"
    # https://kb.objectrocket.com/postgresql/from-postgres-to-python-to-html-1033
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

    #print(records)

if __name__ == "__main__":
    app.run(debug=True)