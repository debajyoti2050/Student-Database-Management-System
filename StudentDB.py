import cx_Oracle as c
connection = c.connect("c##scott/tiger@localhost/ORCL21C")
print("Database opened successfully")
cursor = connection.cursor()
#delete
#cursor.execute('''DROP TABLE Student_Info;''')
cursor.execute("create table Student_Info (id number PRIMARY KEY , name varchar2(22) NOT NULL, email varchar2(22) UNIQUE NOT NULL, gender varchar2(22) NOT NULL, contact varchar2(22) UNIQUE NOT NULL, dob varchar2(22) NOT NULL, address varchar2(22) NOT NULL)")
print("Table created successfully")
connection.close()   

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
