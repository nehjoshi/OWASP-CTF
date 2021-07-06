from flask import Flask, render_template
import sys
import pyrebase
import requests
from flask import Flask, redirect, url_for, request,session
from flask_session import Session
from getpass import getpass
import firebase_admin
from firebase_admin import credentials, firestore, db
from forms import *
cred_obj = firebase_admin.credentials.Certificate("owasp.json")
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':'https://wasp-ac756-default-rtdb.firebaseio.com/'})

ref = db.reference("/")
firebaseconf = {
    "apiKey": "AIzaSyCLjNxUYTlrlVCG3OCLAkImONvPE7aPoNY",
    "authDomain": "wasp-ac756.firebaseapp.com",
    "databaseURL": "https://wasp-ac756-default-rtdb.firebaseio.com",
    "projectId": "wasp-ac756",
    "storageBucket": "wasp-ac756.appspot.com",
    "messagingSenderId": "138623232531",
    "appId": "1:138623232531:web:5ecdcc96a535d965cdade6",
    "measurementId": "G-0YJ0Z99R6D"
}
firebase = pyrebase.initialize_app(firebaseconf)
auth = firebase.auth()
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY']="SECRET CANNOT BE REVEALED"
Session(app)

@app.route('/')
@app.route('/home')
def home_page():
    if "uname" in session:
        return redirect('/timer') 
    else: 
        return render_template('home.html',session=session)

@app.route('/register',methods=["GET","POST"])
def register():
    form = signup()
    flags={}
    if (request.method == 'POST'):
        username=request.form.get("uname")
        email=request.form.get("email")
        password=request.form.get("password")
        if(len(password)<6):
            flags["invalidpass"]=1
            return render_template('register.html', form=form,flag=flags)
        try:
            user=auth.create_user_with_email_and_password(email,password)
            auth.send_email_verification(user['idToken'])
            data={
                "username": username,
                "emailid": email,
                "Scores": 0
            }
            ref.push().set(data)
            flags["registered"]=1
            session["registered"]=1
            return redirect(url_for('.login'))
        except:
            flags["registered"]=0
    return render_template('register.html', form=form,flag=flags)

@app.route('/leaderboard')
def leaderboard():
    if "uname" in session:
        return render_template('leaderboard.html') 
    else:
        return redirect("./")

@app.route('/login',methods=["GET","POST"])
def login():
    flags={"verify":1,"credentials":0}
    form = loginf()
    if "loggedout" in flags:
        del flags["loggedout"]
    if "logged" and "email" and "uname" in session:
        flags["loggedout"]=True
        del session["logged"]
        del session["email"]
        del session["uname"]
    try:
        if(session["registered"]==1):
            flags["registered"]=1
            del session["registered"]
    except:
        flags["registered"]=0
    if (request.method == 'POST'):
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            if(auth.get_account_info(user["idToken"])["users"][0]["emailVerified"]==False):
                dataset=ref.get()
                for keys in dataset:
                    if(dataset[keys]["emailid"]==email):
                        session["logged"]=True
                        session["email"]=email
                        session["uname"]=dataset[keys]["username"]
                        break
                return redirect("./timer")
            else:
                auth.current_user = None
                flags["verify"]=0
        except:
            flags["credentials"]=1
            return render_template('login.html', form=form,flag=flags)
    return render_template('login.html', form=form,flag=flags)

@app.route('/challenge')
def challenge():
    if "uname" in session:
        return render_template('challenge.html') 
    else:
        return redirect("./") 

@app.route('/timer')
def timer():
    if "uname" in session:
        return render_template('timer.html') 
    else:
        return redirect("./")   

@app.route('/reset_password',methods=["GET","POST"])
def reset():
    form=password()
    data={"success":0,"wrongemail":0}
    if(request.method=='POST'):
        mail=request.form.get("email")
        try:
            auth.send_password_reset_email(mail)
            data["success"]=1
            return render_template('reset_password.html',value=data,form=form)
        except:
            data["wrongemail"]=1
            return render_template('reset_password.html',value=data,form=form)
    return render_template('reset_password.html',form=form,value=data)

@app.route('/email_verified')
def email_verified():
    return render_template('verified_email.html')

if __name__ == '__main__':
    app.run(debug=True)
