
from flask import Flask, render_template, request, redirect, url_for, session 

from flask_mysqldb import MySQL 

import MySQLdb.cursors 

import re 

  

  

app = Flask(__name__) 

app.secret_key = 'your secret key'

  

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'root'

app.config['MYSQL_DB'] = 'mits'

  

mysql = MySQL(app) 

if mysql:
    print("hi")
else:
    print("sorry")    

@app.route('/') 
def home():
    return render_template('home_page.html')


@app.route('/Tutor_signin', methods =['GET', 'POST'])
def login(): 

    msg = '' 

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 

        email = request.form['email'] 

        password = request.form['password'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM teacher WHERE username = % s AND password = % s', (email, password, )) 

        account = cursor.fetchone() 

        if account: 

            session['loggedin'] = True

            session['password'] = account['password'] 

            session['username'] = account['username'] 

            msg="user logged in"
            return render_template('Tutor_data.html', msg = msg) 
            

        else: 

            msg = 'Incorrect username / password !'

    return render_template('Tutor_signin.html', msg = msg) 

  
@app.route('/Tutor_data',methods =['GET', 'POST'])
def data():
    msg = '' 

    if request.method == 'POST' and 'name' in request.form and 'sid' in request.form and 'subject' in request.form and 'mark' in request.form and 'attendence' in request.form : 
        name = request.form['name'] 

        student_id = request.form['sid']

        subject = request.form['subject'] 

        mark = request.form['mark'] 

        attendence = request.form['attendence'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('INSERT INTO data (subject, mark, attendence, student_id , name)  VALUES (% s, % s, % s, % s,% s)',(subject, mark, attendence, student_id , name) )

        mysql.connection.commit() 

        msg = 'You have entered data successfully !'

        
        
        return redirect(url_for('show'))

   
@app.route('/show') 
def show():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute("SELECT * FROM data")
    user=cursor.fetchall()
    print(user)
    
    return render_template("show.html",user=user,headers=user[0].keys())
    #headers=user[0].keys() to get the headers also from the selected data range

@app.route('/logout') 

def logout(): 

    session.pop('loggedin', None) 

    session.pop('id', None) 

    session.pop('username', None) 

    return redirect(url_for('home')) 

  

@app.route('/Tutor_register', methods =['GET', 'POST']) 

def register(): 

    msg = '' 

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 

        username = request.form['username'] 

        password = request.form['password'] 

        email = request.form['email'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM teacher WHERE username = % s', (username, )) 

        account = cursor.fetchone() 

        if account: 

            msg = 'Account already exists !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 

            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', username): 

            msg = 'Username must contain only characters and numbers !'

        elif not username or not password or not email: 

            msg = 'Please fill out the form !'

        else: 

            cursor.execute('INSERT INTO teacher VALUES (NULL, % s, % s, % s)', (username, password, email, )) 

            mysql.connection.commit() 

            msg = 'You have successfully registered !'

    elif request.method == 'POST': 

        msg = 'Please fill out the form !'

    return render_template('Tutor_register.html', msg = msg) 
@app.route('/student_login', methods =['GET', 'POST'])
def student(): 

    msg = '' 

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form : 
        
        username = request.form['username'] 

        password = request.form['password'] 
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM student WHERE username = % s  AND password = % s', (username, password, )) 

        account = cursor.fetchone() 

        if account: 

            session['loggedin'] = True

            session['id'] = account['id'] 

            session['username'] = account['username'] 
            

            msg="user logged in"
            return redirect(url_for('studentdata')) 
            

        else: 

            msg = 'Incorrect username / password !'

    return render_template('student_login.html',msg=msg)
@app.route('/studentdata') 
def studentdata():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM data WHERE student_id = % s', (session['id'], )) 

        result = cursor.fetchall() 

        print(result)
        return render_template('studentdata.html',result=result,headers=result[0].keys())
        
        


if __name__ == "__main__":
    app.run()
