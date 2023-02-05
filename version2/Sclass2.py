import os
import psycopg2
from psycopg2 import OperationalError
from flask import render_template
from abc import ABCMeta,abstractstaticmethod


conn = psycopg2.connect(
        host="localhost",
        database="database",
        user='postgres',
        password='postgres')

"""
class Pet:
    def __init__(self,owner_name,pet_name,pet_type):
        self.owner_name=owner_name
        self.pet_name=pet_name
        self.pet_type=pet_type

"""

class DBConnection(metaclass=ABCMeta):
    conn=None
    curr=None
    def __init__(self):
        pass
    @abstractstaticmethod
    def conndb(self):
        """
        Implement in childclass
        """

    @abstractstaticmethod
    def create_table(self,tablename,f1,f2,f3):
        #self.curr.execute("DROP TABLE IF EXISTS "+ str(tablename))
       """
       Implement in childclass
       """

    @abstractstaticmethod
    def insert_db(self,tablename,f1,f2,f3):
        """
        Implement in childclass
        """

    @abstractstaticmethod
    def select_result(self,tablename,f1,f2,f3):
        """
        Implement in childclass
        """

    @abstractstaticmethod
    def delete_row(self,tablename,ids):
        """
        Implement in childclass
        """

    @abstractstaticmethod
    def fetchrec(self,tablename,ids):
        """
          Implement in childclass
        """

    @abstractstaticmethod
    def update(self,tablename,f1,f2,f3,ids):
        """
        Implement in childclass
        """

    @abstractstaticmethod
    def close(self):
        """
        Implement in childclass
        """

class DBConnectionSingleton(DBConnection):

    __instance = None

    @staticmethod
    def get_instance():
        if DBConnectionSingleton.__instance==None:
            DBConnectionSingleton("OwnerSingleton","name","pet_name","pet_type")
        return DBConnectionSingleton.__instance
        
    def __init__(self,tablename,f1,f2,f3):
        if DBConnectionSingleton.__instance!=None:
            raise Exception("Singleton can't be instantiated")
        else:
            self.tablename=tablename
            self.f1=f1
            self.f2=f2
            self.f3=f3
            DBConnection.__instance= self

    @staticmethod
    def conndb(self):
        self.conn=psycopg2.connect("dbname=flask_db user=postgres password=Finserv@2023")
        self.curr=self.conn.cursor()

    @staticmethod
    def create_table(self,tablename,f1,f2,f3):
        self.curr.execute("CREATE TABLE " + str(tablename) + "(oid serial PRIMARY KEY," + str(f1) + " varchar (150) NOT NULL," + str(f2) + " varchar (50) NOT NULL," + str(f3) + " varchar (50) NOT NULL," + " date_of_adoption date DEFAULT CURRENT_TIMESTAMP );")
        self.conn.commit()

    @staticmethod
    def insert_db(self,tablename,f1,f2,f3):
        try:
            self.curr.execute("insert into " + str(tablename) + " (name,pet_name,pet_type )" + "values(%s,%s,%s)",(str(f1),str(f2),str(f3)))
            self.conn.commit()
        except psycopg2.Error as e:
            return render_template('error.html',e=e)


    @staticmethod
    def select_result(self,tablename):
        try:
            self.curr.execute("Select * from " + str(tablename) + ";")
            students=self.curr.fetchall()
            return students
        #for student in students:
        #    print(student)
        except psycopg2.Error as e:
            return e
    
    @staticmethod
    def delete_row(self,tablename,ids):
        try:
            self.curr.execute('DELETE FROM '+str(tablename)+' Where oid = %s;',(ids,))
            self.conn.commit()
        except psycopg2.Error as e:
            return e

    @staticmethod
    def fetchrec(self,tablename,ids):
        try:
            self.curr.execute('SELECT FROM ' + str(tablename)+ ' Where oid = %s;',(ids,))
            self.conn.commit()
        except psycopg2.Error as e:
            return 

    @staticmethod
    def update(self,tablename,f1,f2,f3,ids):
        try:
            if (not f1.isdigit() and not f2.isdigit() and not f3.isdigit()):
                self.curr.execute("UPDATE "+str(tablename)+ " SET name = '" + str(f1) + "',pet_name = '" + str(f2) + "',pet_type = '" + str(f3) + "' WHERE oid = %s;",(ids,))
                self.conn.commit()
        except psycopg2.Error as e:
            return e

    @staticmethod
    def close(self):
        try:
            self.curr.close()
            self.conn.close()
        except psycopg2.Error as e:
            return e



    


