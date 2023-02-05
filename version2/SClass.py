import os
import psycopg2
from psycopg2 import OperationalError
from flask import render_template
from conifg import info





class Pet:
    def __init__(self,owner_name,pet_name,pet_type):
        self.owner_name=owner_name
        self.pet_name=pet_name
        self.pet_type=pet_type

class DBConnector:
    conn=None
    curr=None
    def __init__(self):
        pass
    @classmethod
    def conndb(self):
        self.conn=psycopg2.connect(dbname=info['database'],
         user="postgres",
         password=info['password'])
        #self.curr=self.conn.cursor()
        return self.conn




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
    
class DBConnection:
    conn=None
    @classmethod
    def get_connection(self,new=False):
        if(new or not self.conn):
            db=DBConnector()
            self.conn=db.conndb()
        return self.conn
    @classmethod
    def create_table(self,tablename,f1,f2,f3):
        #self.curr.execute("DROP TABLE IF EXISTS "+ str(tablename))
        try:
            conn=self.get_connection()
            curr=conn.cursor()
        except:
            conn=self.get_connection(new=True)
            curr=conn.cursor()
        curr.execute("CREATE TABLE " + str(tablename) + "(oid serial PRIMARY KEY," + str(f1) + " varchar (150) NOT NULL," + str(f2) + " varchar (50) NOT NULL," + str(f3) + " varchar (50) NOT NULL," + " date_of_adoption date DEFAULT CURRENT_TIMESTAMP );")
        conn.commit()
        curr.close()



    @classmethod
    def insert_db(self,tablename,f1,f2,f3):
           try:
                conn=self.get_connection()
                curr=conn.cursor()
           except:
                conn=self.get_connection(new=True)
                curr=conn.cursor()
           curr.execute("insert into " + str(tablename) + " (owner_name,pet_name,pet_type )" + "values(%s,%s,%s)",(str(f1),str(f2),str(f3)))
           conn.commit()
           curr.close()


    @classmethod
    def select_result(self,tablename):
           try:
                conn=self.get_connection()
                curr=conn.cursor()
           except:
                conn=self.get_connection(new=True)
                curr=conn.cursor()
           conn.commit()
           curr.execute("Select * from " + str(tablename) + ";")
           students=curr.fetchall()
           return students
        #for student in students:
        #    print(student)

    @classmethod
    def delete_row(self,tablename,ids):
        try:
                conn=self.get_connection()
                curr=conn.cursor()
        except:
                conn=self.get_connection(new=True)
                curr=conn.cursor()
        curr.execute('DELETE FROM '+str(tablename)+' Where oid = %s;',(ids,))
        conn.commit()
        curr.close()
        
        


    @classmethod
    def update(self,tablename,f1,f2,f3,ids):
        try:
                conn=self.get_connection()
                curr=conn.cursor()
        except:
                conn=self.get_connection(new=True)
                curr=conn.cursor()
        if (not f1.isdigit() and not f2.isdigit() and not f3.isdigit()):
            curr.execute("UPDATE "+str(tablename)+ " SET owner_name = '" + str(f1) + "',pet_name = '" + str(f2) + "',pet_type = '" + str(f3) + "' WHERE oid = %s;",(ids,))
            conn.commit()
            curr.close()
        

"""
    @classmethod
    def close(self):
        try:
            self.curr.close()
            self.conn.close()
        except psycopg2.Error as e:
            return e
"""
#UPDATE COMPANY SET SALARY = 15000 WHERE ID = 3
