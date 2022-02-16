# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
import time
import os
from flask import Flask, render_template, request,flash, redirect,url_for
import pymysql
import mysql.connector
import pyotp
from flask_bootstrap import Bootstrap
from google.cloud import secretmanager
# from sonarqube import SonarCloudClient
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12).hex()
Bootstrap(app)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/guru/Downloads/e-cycling-329118-ff778c0c8fd5.json"
# db_user = "root"
# db_password = "cwadmin"
# db_name = "test"
# db_connection_name = "e-cycling-329118:us-central1:mysqlpoc"
client = secretmanager.SecretManagerServiceClient()

secret_id="db_user"
project_id="e-cycling-329118"
# h = SonarCloudClient(sonarcloud_url="https://sonarcloud.io", token='744616df98956cc31c6d39904ca93dc7671902d4')
 
print(client)
secret_db_user_name = f"projects/667306116120/secrets/db_user/versions/latest"
response_db_user = client.access_secret_version(request={"name": secret_db_user_name})
payload_db_user = response_db_user.payload.data.decode("UTF-8")
 
secret_db_password_name = f"projects/667306116120/secrets/db_password/versions/latest"
response_db_password = client.access_secret_version(request={"name": secret_db_password_name})
payload_db_password = response_db_password.payload.data.decode("UTF-8")
 
secret_db_name_name = f"projects/667306116120/secrets/db_name/versions/latest"
response_db_name = client.access_secret_version(request={"name": secret_db_name_name})
payload_db_name = response_db_name.payload.data.decode("UTF-8")
 
secret_db_connection_name_name = f"projects/667306116120/secrets/db_connection_name/versions/latest"
response_db_connection_name = client.access_secret_version(request={"name": secret_db_connection_name_name})
payload_db_connection_name = response_db_connection_name.payload.data.decode("UTF-8")

db_user = payload_db_user
db_password = payload_db_password
db_name = payload_db_name
db_connection_name = payload_db_connection_name
 
def open_connection():
   if os.environ.get('GAE_ENV') == 'standard':
       print("True")
       # If deployed, use the local socket interface for accessing Cloud SQL
       unix_socket = '/cloudsql/{}'.format(db_connection_name)
       cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
       return cnx
   else:
       # If running locally, use the TCP connections instead
       # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
       # so that your application can use 127.0.0.1:3306 to connect to your
       # Cloud SQL instance
       host = '127.0.0.1'	
       cnx = pymysql.connect(user=db_user, password=db_password,
                             host=host, db=db_name)
       return cnx

@app.route('/')
def login():
    """Return a friendly HTTP greeting."""
    conn=open_connection()
    cursor = conn.cursor()
    # Storing SQL Statements in a variable sql
    sql = "SELECT * FROM case_table"
    # Calling execute method
    cursor.execute(sql)
    # storing results in a result variable
    result = cursor.fetchall() # fetchall retrieves all records
    # Display the values
    print(result) 
    # Close the connection
    cursor.close()
    conn.close()
    return render_template("table.html",data=result)
   ## return render_template("login.html")
# def hello():
#     # """Return a friendly HTTP greeting."""
#     # return 'Hello Guru!!'
#     return render_template('index.html')

@app.route('/index')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template("index.html")

@app.route('/new_case')
def new_case():
    """Return a friendly HTTP greeting."""
    return render_template("new_case.html")

@app.route('/table')
def table():
    """Return a friendly HTTP greeting."""
    conn=open_connection()
    cursor = conn.cursor()
    # Storing SQL Statements in a variable sql
    sql = "SELECT * FROM case_table"
    # Calling execute method
    cursor.execute(sql)
    # storing results in a result variable
    result = cursor.fetchall() # fetchall retrieves all records
    # Display the values
    print(result) 
    # Close the connection
    cursor.close()
    conn.close()
    return render_template("table.html",data=result)
    # return render_template("table.html")
    # return render_template("index.html")

@app.route('/case' ,methods=['POST'])
def case():
    """Return a friendly HTTP greeting."""
    conn=open_connection()
    cid = request.form.get("case_id")
    print(cid)
    cursor = conn.cursor()
    conn.begin()
    sql = "select * from case_table where case_id = %s"
    cursor.execute(sql,(cid[1:len(cid)-1]))
    result = cursor.fetchall()
    cursor.close()
    conn.close()  
    return render_template("indi_case.html",data=result)  
    # return render_template("case.html",data=result)
    # return render_template("index.html")
    

@app.route('/action_page', methods=['POST'])
def output():
    # """Return a friendly HTTP greeting."""
    # return 'Hello Guru!!'
    conn=open_connection()
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("firstname")
       # getting input with name = lname in HTML form
       case_id=str(time.time())[0:-8] 
       last_name = request.form.get("lastname") 
       email=request.form.get("email")
       subject = request.form.get("subject")
       data=[first_name,last_name,email,subject]
       # code to insert into the mysql table
       # Creation of a Cursor object
       cursor = conn.cursor()
       conn.begin() # initiate the transaction
       # Storing SQL Statements in a variable sql
       #sql = "INSERT INTO case_table VALUES (,'Tenesson','bt123@gmail.com','Hello bro!!')"
       sql="INSERT INTO case_table (case_id,firstname, lastname, email, case_details) VALUES (%s,%s,%s,%s,%s)"
       # Calling execute method
       cursor.execute(sql,(case_id, first_name, last_name, email, subject))
       # Update/Delete/Insert commands via execute won't be finalized until changes are committed
       conn.commit() # finalize the changes
       # Close the connection
       cursor.close()
       conn.close()
    return render_template("new_case.html")
    # return render_template('index.html')

@app.route('/display_page', methods=['GET'])
def display():
    # """Return a friendly HTTP greeting."""
    # return 'Hello Guru!!'
    # return render_template("form_return.html",data=data)
    conn=open_connection()
    cursor = conn.cursor()
    # Storing SQL Statements in a variable sql
    sql = "SELECT * FROM case_table"
    # Calling execute method
    cursor.execute(sql)
    # storing results in a result variable
    result = cursor.fetchall() # fetchall retrieves all records
    # Display the values
    print(result) 
    # Close the connection
    cursor.close()
    conn.close()
    return render_template("form_return.html",data=result) 

# @app.route("/login/")
# def login():
#     return render_template("login.html")

# login form route
@app.route("/", methods=["POST"])
def login_form():
    # demo creds
    creds = {"username": "john5678", "password": "guru1!"}

    # getting form data
    username = request.form.get("username")
    password = request.form.get("password")

    # authenticating submitted creds with demo creds
    if username == creds["username"] and password == creds["password"]:
        # inform users if creds are valid
        # flash("The credentials provided are valid", "success")
        # return redirect(url_for("login_2fa"))
        # print("water")
        conn=open_connection()
        cursor = conn.cursor()
        # Storing SQL Statements in a variable sql
        sql = "SELECT * FROM case_table"
        # Calling execute method
        cursor.execute(sql)
        # storing results in a result variable
        result = cursor.fetchall() # fetchall retrieves all records
        # Display the values
        print(result) 
        # Close the connection
        cursor.close()
        conn.close()
        
        return render_template("table.html",data=result)
    else:
        # inform users if creds are invalid
        flash("You have supplied invalid login credentials!", "danger")
        return render_template("login.html")   

# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    # secret = pyotp.random_base32()
    secret="XHBS3AYB4ZIOWIHVAIM7MSFM542BDHKX"
    return render_template("login_2fa.html", secret=secret)

# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        conn=open_connection()
        cursor = conn.cursor()
        # Storing SQL Statements in a variable sql
        sql = "SELECT * FROM case_table"
        # Calling execute method
        cursor.execute(sql)
        # storing results in a result variable
        result = cursor.fetchall() # fetchall retrieves all records
        # Display the values
        print(result) 
        # Close the connection
        cursor.close()
        conn.close()
        return render_template("table.html",data=result)
        
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
