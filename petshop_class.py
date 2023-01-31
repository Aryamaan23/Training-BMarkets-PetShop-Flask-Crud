import os
import psycopg2
from psycopg2 import OperationalError
from flask import render_template

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='postgres',
        password='postgres')

class Pet:
    def __init__(self,owner_name,pet_name,pet_type):
        self.owner_name=owner_name
        self.pet_name=pet_name
        self.pet_type=pet_type

class DBConnection:
    conn=None
    curr=None
    def __init__(self):
        pass
    @classmethod
    def conndb(self):
        self.conn=psycopg2.connect("dbname=flask_db user=postgres password=postgres")
        self.curr=self.conn.cursor()



    """


cur.execute('CREATE TABLE owner (oid serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'pet_name varchar (50) NOT NULL,'
                                 'pet_type varchar (50) NOT NULL,'
                                 'date_of_adoption date DEFAULT CURRENT_TIMESTAMP);'
                                 )
    
    
    """

    """
 cur.execute('INSERT INTO owner (name,pet_name,pet_type)'
                    'VALUES (%s, %s, %s)',
                    (name, pet_name, pet_type))
    """

    @classmethod
    def create_table(self,tablename,f1,f2,f3):
        #self.curr.execute("DROP TABLE IF EXISTS "+ str(tablename))
        try:
            self.curr.execute("CREATE TABLE " + str(tablename) + "(oid serial PRIMARY KEY," + str(f1) + " varchar (150) NOT NULL," + str(f2) + " varchar (50) NOT NULL," + str(f3) + " varchar (50) NOT NULL," + " date_of_adoption date DEFAULT CURRENT_TIMESTAMP );")
            self.conn.commit()
        except OperationalError as e:
            None


    @classmethod
    def insert_db(self,tablename,f1,f2,f3):
        try:
            self.curr.execute("insert into " + str(tablename) + " (name,pet_name,pet_type )" + "values(%s,%s,%s)",(str(f1),str(f2),str(f3)))
            self.conn.commit()
        except psycopg2.Error as e:
            return render_template('error.html',e=e)

    @classmethod
    def select_result(self,tablename):
        try:
            self.curr.execute("Select * from " + str(tablename) + ";")
            students=self.curr.fetchall()
            return students
        #for student in students:
        #    print(student)
        except psycopg2.Error as e:
            return e

    @classmethod
    def delete_row(self,tablename,ids):
        try:
            self.curr.execute('DELETE FROM '+str(tablename)+' Where oid = %s;',(ids,))
            self.conn.commit()
        except psycopg2.Error as e:
            return e
        

    @classmethod
    def fetchrec(self,tablename,ids):
        try:
            self.curr.execute('SELECT FROM ' + str(tablename)+ ' Where oid = %s;',(ids,))
            self.conn.commit()
        except psycopg2.Error as e:
            return 

    @classmethod
    def update(self,tablename,f1,f2,f3,ids):
        try:
            if (not f1.isdigit() and not f2.isdigit() and not f3.isdigit()):
                self.curr.execute("UPDATE "+str(tablename)+ " SET name = '" + str(f1) + "',pet_name = '" + str(f2) + "',pet_type = '" + str(f3) + "' WHERE oid = %s;",(ids,))
                self.conn.commit()
        except psycopg2.Error as e:
            return e


    @classmethod
    def close(self):
        try:
            self.curr.close()
            self.conn.close()
        except psycopg2.Error as e:
            return e

#UPDATE COMPANY SET SALARY = 15000 WHERE ID = 3
