import sqlite3

connection=sqlite3.connect('student.db')
#create a cursor object to insert record, create table
cursor=connection.cursor()
## create the table
table_info="""
CREATE TABLE STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25));
"""
cursor.execute(table_info)
#insert records
cursor.execute("INSERT INTO STUDENT VALUES('MOUNIKA','TENTH','A')")
cursor.execute("INSERT INTO STUDENT VALUES('ANUSHA','NINTH','B')") 
cursor.execute("INSERT INTO STUDENT VALUES('SOWMYA','EIGHTH','C')")
cursor.execute("INSERT INTO STUDENT VALUES('KAVYA','SEVENTH','A')")
cursor.execute("INSERT INTO STUDENT VALUES('LAKSHMI','SIXTH','B')")


#display the records
print("STUDENT RECORDS:")
cursor.execute("SELECT * FROM STUDENT")
for row in cursor.fetchall():
    print(row)

connection.commit()
connection.close()