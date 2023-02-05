import os
import psycopg2
from flask import Flask, render_template,request,redirect,url_for
#from petshop_class_singleton import Pet,DBConnectionSingleton
from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SelectField,DateTimeField,TextAreaField,SubmitField,RadioField
from wtforms.validators import InputRequired, Length
from petshiosingletonnew import DBConnection
import logging





class EditForm(FlaskForm):
    name=StringField("What is the owner name? ")
    pet_name=StringField("What is the pet name?")
    pet_type=StringField("What is the type of pet?")
    submit=SubmitField('Submit Button')
    

app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'
logging.basicConfig(filename='demo.log',
level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user='postgres',
                            password='Finserv@2023')
    return conn
#When we connect to a remote server 2 more things are required that is port=5432 and ip address


db=DBConnection()

try:
    db.create_table('OwnerSingleton','name','pet_name','pet_type')
except Exception as e: 
    pass


@app.route('/')
def index():
    #owner2=db.create_table('ownerpet23','owner_name','pet_name','pet_breed')
    app.logger.info('Showing Owner Records')
    owner_details=db.select_result('OwnerSingleton')
    #cur.execute('SELECT * FROM owner;')
    #owner_details = cur.fetchall()
    #cur.close()
    try:
        return render_template('petshop1.html', owner_details=owner_details)
    except psycopg2.Error as error:
        return render_template('error.html',error)

"""
class Pet(FlaskForm):
    pet_types=[('Dog','Dog'),('Cat','Cat'),('Cow','Cow')]
    o_name=StringField('Name')
    pet_name=StringField('PetName')
    pet_type= SelectField('Type', choices=pet_types)
    dateofadoption=StringField('Date of Adoption')

cur.execute('INSERT INTO owner (name, pet_name, pet_type)'
            'VALUES (%s, %s, %s)',
            ('Aryamaan Pandey',
             'Tom',
             'Dog',
            )
            )

"""

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['owner_name']
        pet_name = request.form['pet_name']
        pet_type = request.form['pet_type']

        db.insert_db('OwnerSingleton',name,pet_name,pet_type)
        #It's important otherwise you won't be able to see the changes!
        app.logger.info('New Record Added!')
        return redirect(url_for('index'))
    return render_template('petshopcreate.html')
    """
    try:
        return render_template('petshopcreate.html')
    except psycopg2.Error as e:
        return render_template('error.html',e)
    """


@app.route('/delete/<int:ids>')
def delete(ids):
    #conn = get_db_connection()
    #curr = conn.cursor()
    t = (ids,)
    db.delete_row('OwnerSingleton',t)
    app.logger.info('Deleting Owner Records')
    #curr.execute('DELETE FROM owner WHERE oid = %s', (ids,))
    #conn.commit()
    #curr.close()
    #conn.close()
    return redirect(url_for('index'))


@app.route('/edit/<int:ids>',methods=["GET","POST"])
def edit(ids):
    #row=db.fetchrec('OwnerSingleton',ids)
    form=EditForm()
    if form.validate_on_submit():
        name=form.name.data
        pet_name=form.pet_name.data
        pet_type=form.pet_type.data
    if request.method=="POST":
        db.update('OwnerSingleton',name,pet_name,pet_type,ids)
        app.logger.info('Updating Owner Records')
        return redirect(url_for('index'))
    return render_template('editpetshop.html',form=form)

@app.route('/error')
def error():
    return render_template('error.html',error=error)
   



if __name__ == '__main__':
    app.run(debug=True,port=5000)
