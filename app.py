from flask import Flask, render_template
from config import sqlpassword
import psycopg2

app = Flask(__name__)

# f"postgresql://postgres:{sqlpassword}@localhost:5432/tornado_db"
# https://kb.objectrocket.com/postgresql/from-postgres-to-python-to-html-1033
db_conn = psycopg2.connect(database="tornado_db", user="postgres", password=f"{sqlpassword}", host="127.0.0.1", port="5432")
db_cursor = db_conn.cursor()

@app.route("/", methods=['post', 'get'])
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    db_cursor.execute("SELECT * FROM tornado_data")
    tornado_table = db_cursor.fetchall()

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", data=tornado_
@app.route("")

if __name__ == "__main__":
    app.run(debug=True)