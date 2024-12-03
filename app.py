from flask import Flask, render_template, request, flash, redirect
import sqlite3
import pickle
import numpy as np
app = Flask(__name__)
import pickle
rf=pickle.load(open("rf.pkl","rb"))
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('fetal.html',name=name)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/fetalPage")
def fetalPage():
    return render_template('fetal.html')

@app.route("/lastpage", methods = ['POST', 'GET'])
def lastpage():
    if request.method == 'POST':
        serum = request.form['serum']
        if 0 <= int(serum) <= 20:
            res="Deficient"
        elif 21 <= int(serum) <= 29:
            res="Insufficient"
        else:
            res="Sufficient"
        return render_template('predict.html',ress=res)

@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        name = request.form['name']
        vo = request.form['age']
        v1 = request.form['Gender']
        v2 = request.form['MCV']
        v3 = request.form['feet']
        
        data = np.array([[vo, v1, v2, v3]])
        result = rf.predict(data)[0]
        v2=int(v2)

        if result==2:
            res='B12 Deficiency Detected'
            print(f"\n\n{res}\n\n")
            return render_template('fetal1.html',name=name, pred = result,status=res)
        elif result==3: 
            res='Anaemia Detected'
            print(f"\n\n{res}\n\n")
            return render_template('fetal1.html',name=name, pred = result,status=res)
        else:
            res='Normal'
            print(f"\n\n{res}\n\n")
            return render_template('fetal1.html',name=name,status=res,pred=result)
    return render_template('predict.html')

if __name__ == '__main__':
	app.run(debug = True)