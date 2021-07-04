from flask import Flask, render_template
import pyrebase
import requests
from flask import Flask, redirect, url_for, request,session
from getpass import getpass
import firebase_admin
from firebase_admin import credentials, firestore, db
from forms import signup,loginf
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
app.config['SECRET_KEY']="OKAY"

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register():
    form = signup()
    return render_template('register.html', form=form)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/login')
def login():
    form = loginf()
    return render_template('login.html', form=form)

@app.route('/auth',methods=["GET","POST"])
def authentication():
    form = signup()
    if (request.method == 'POST'):
        username=request.form.get("uname")
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.create_user_with_email_and_password(email,password)
            auth.send_email_verification(user['idToken'])
            data={
                "username": username,
                "emailid": email
            }
            ref.push().set(data)
            print(user)
            return redirect("./login")
        except:
            print("Email already exists")
            return redirect("./register")


@app.route('/userauth',methods=["GET","POST"])
def userauth():
    form = login()
    if (request.method == 'POST'):
        #username=request.form.get("uname")
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            if(auth.get_account_info(user["idToken"])["users"][0]["emailVerified"]==True):
                return redirect("./")
            else:
                #print(auth.get_account_info(user["idToken"]))
                auth.current_user = None
                #print(auth.get_account_info(user["idToken"]))
                print("Please verify the email")
                return redirect("./register")
        except:
            print("Wrong user credentials")
            return redirect("./login")

@app.route('/challenge')
def challenge(username="Nehjoshi_123"):
    return render_template('challenge.html', username=username)

@app.route('/reset_password')
def reset():
    #Reset Password using Email here
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run()