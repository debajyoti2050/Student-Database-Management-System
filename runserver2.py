from datetime import date
from flask.helpers import url_for
from flask import Flask, request, redirect, render_template
import sqlite3 as sql
import cx_Oracle as c
tday = date.today()
today = str(tday.day)+'-'+str(tday.month)+'-'+str(tday.year)



con = c.connect("c##scott/tiger@localhost/orcl21c")
print(con)


def insertOthers(*args):
    try:
        Query = f'''INSERT INTO OTHERS(GUARDIAN, PHONE, STUDENT_GMAIL)
                VALUES('{args[0]}', {args[1]}, '{args[2]}')'''
        #con3 = sql.connect("./database/data.db")
        cur3 = con.cursor()
        cur3.execute(Query)
        con.commit()
        return True, Query
    except Exception as e:
        print(e)
        return False, ''

def insertDetails(*args):
    try:
        age = int(tday.year) - int(args[1][0:4])
        gender = args[4]
        if gender == 'm': gender = "Male"
        elif gender == 'f': gender = "Female"
        else: gender = "Other"
        if args[2] == '':
            Query = f'''INSERT INTO STUDENT(NAME, DOA, AGE, PHONE, ADDRESS, GENDER)
                    VALUES('{args[0]}', '{today}', {age}, NULL, '{args[3]}', '{gender}')'''
        else:
            Query = f'''INSERT INTO STUDENT(NAME, DOA, AGE, PHONE, ADDRESS, GENDER)
                    VALUES('{args[0]}', '{today}', {age}, '{args[2]}', '{args[3]}', '{gender}')'''
        #con2 = sql.connect("./database/data.db")
        cur2 = con.cursor()
        cur2.execute(Query)
        con.commit()
        return True, Query
    except Exception as e:
        print(e)
        return False, ''



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return "<h1>Admin Page Under Maintenance!!!</h1>"

@app.route("/login", methods=['GET', 'POST'])
def login():
    return "<h1>Under Maintenance!!!</h1>"

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return "<h1>Under Maintenance!!!</h1>"

@app.route("/admission", methods=['GET', 'POST'])
def admission():
    return render_template("form.html")

@app.route("/form-submission", methods=['GET', 'POST'])
def submission():
    dob = request.form["dob"]
    name = request.form["name"]
    gname = request.form["gname"]
    gmail = request.form["gmail"]
    phone = request.form["phone"]
    gender = request.form["gender"]
    address = request.form["address"]
    gphone = int(request.form["gphone"])
    o = insertOthers(gname, gphone, gmail)
    d = insertDetails(name, dob, phone, address, gender)
    if (o[0] == True and d[0] == True):
        #con = sql.connect("./database/data.db")
        cur4 = con.cursor()
        cur4.execute(o[1])
        cur4.execute(d[1])
        con.commit()
    else:
        #con = sql.connect("./database/data.db")
        cur4 = con.cursor()
        con.rollback()
    return redirect(url_for("home"))

@app.route("/student-records", methods=['GET', 'POST'])
def table():
    #con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from student")
    #data = alldata
    rows = cur.fetchall(); 
    return render_template("table.html", student=rows, length=len(rows))

if __name__ == "__main__":
    app.run(debug=True, port=8000)