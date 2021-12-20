'''
CREATE OR REPLACE TRIGGER dept_bir 
BEFORE INSERT ON student_Info
FOR EACH ROW

BEGIN
  SELECT dept_seq.NEXTVAL
  INTO   :new.id
  FROM   dual;
END;
/
CREATE SEQUENCE dept_seq START WITH 1;
'''
from flask import *
#import sqlite3
import cx_Oracle as c
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord",methods = ["POST","GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            address = request.form["address"]
            sql = ('insert into Student_Info(name, email, gender, contact, dob, address)'
                  'values(:name,:email,:gender,:contact,:dob,:address)')
            with c.connect("c##scott/tiger@localhost/orcl") as connection:
                cursor = connection.cursor()
                print(cursor)
                cursor.execute(sql,[name,email,gender,contact,dob,address])
                print('sql run')
                connection.commit()
                msg = "Student details successfully Added"
                print(msg)
        except Exception as e:
            print('sorry....',e)
            connection.rollback()
            msg = "We can not add Student detials to the database"
        finally:
            return render_template("success_record.html",msg = msg)
            connection.close()



@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")



@app.route("/student_info")
def student_info():
    connection = c.connect("c##scott/tiger@localhost/orcl")
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Student_Info")
    rows = cursor.fetchall()
    print(type(rows))
    return render_template("student_info.html",rows = rows)



@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with c.connect("c##scott/tiger@localhost/orcl") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where id=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:

            cursor.execute("delete from Student_Info where id = ?",(id,))
            msg = "Student detial successfully deleted"
            return render_template("delete_record.html", msg=msg)

        else:
            msg = "can't be deleted"
            return render_template("delete_record.html", msg=msg)

        
        
if __name__ == "__main__":
    app.run(debug = True)  
