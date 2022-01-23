from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from model import Investment
import importlib
import algorithm
from algorithm import investmentClassifier, topFive, getSuggestions, bad_parameters, good_parameters

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Global Variables
users = {'abc':'abc'}

#Login Main Page
@app.route("/")
@app.route("/login")
#@app.route("/login/<registerFault>/<loginFault>/<registerSuccess>")
def index():
    session['username'] = None
    return render_template("frontPage.html", registerFault=0, loginFault=0, registerSuccess=0, ranking=topFive())

#Check Login and Book Overview
@app.route("/main", methods=["POST", "GET"]) 
def main():
    global users
    if request.method == 'GET' and session['username'] is None:
        return redirect(url_for('index'))
    session['isError']= "False"
    session['referrer'] = "/main"
    if (session['username'] is None):
        session['username'] = request.form.get("username")
        password = request.form.get("password")
        if session['username'] not in users.keys() or users[session['username']] != password:
            session['username'] = None
            return render_template("frontPage.html", registerFault=0, loginFault=1, registerSuccess=0, ranking=topFive()) 
    return redirect(url_for('secondPage'))

#Registration Verification Page
@app.route("/verify", methods=["POST", "GET"])
def verify():
        global users
        if request.method == 'GET' and session['username'] is None:
            return redirect(url_for('index'))
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users.keys():
            return render_template("frontPage.html", registerFault=1, loginFault=0, registerSuccess=0, ranking=topFive())
        else:
            users[username] = password
            return render_template("frontPage.html", registerFault=0, loginFault=0, registerSuccess=1, ranking=topFive())

#Second Information Page
@app.route("/info", methods=["GET"])
def secondPage():
    if (session['username'] is None):
        return redirect(url_for('index'))
    return render_template("secondPage.html", username=str(session['username']))

@app.route("/info/score", methods=["POST","GET"])
def score():
    global regressors
    if (session['username'] is None):
        return redirect(url_for('index'))
    if request.method == 'GET':
        return redirect(url_for('secondPage'))
    name = request.form.get("company_name").upper()
    country = request.form.get("country").title()
    env_cost = request.form.get("env_cost")
    working_cap = request.form.get("working_cap") if request.form.get("working_cap") != '' else 0
    fish_prod_cap = request.form.get("fish_prod_cap") if request.form.get("fish_prod_cap") != '' else 0
    crop_prod_cap = request.form.get("crop_prod_cap") if request.form.get("crop_prod_cap") != '' else 0
    meat_prod_cap = request.form.get("meat_prod_cap") if request.form.get("meat_prod_cap") != '' else 0
    biodiversity = request.form.get("biodiversity") if request.form.get("biodiversity") != '' else 0
    abiotic_res = request.form.get("abiotic_res") if request.form.get("abiotic_res") != '' else 0
    water_prod_cap = request.form.get("water_prod_cap") if request.form.get("water_prod_cap") != '' else 0
    wood_prod_cap = request.form.get("wood_prod_cap") if request.form.get("wood_prod_cap") != '' else 0
    investment = Investment(name,country,env_cost,working_cap,fish_prod_cap,crop_prod_cap,meat_prod_cap,
                        biodiversity,abiotic_res,water_prod_cap,wood_prod_cap)
    importlib.reload(algorithm)
    tier = investmentClassifier(investment)
    suggestions = getSuggestions(tier)
    good_points = good_parameters(investment)
    good_points = [] if good_points is None else good_points
    bad_points = bad_parameters(investment)
    bad_points = [] if bad_points is None else bad_points
    return render_template("score.html", username=str(session['username']), tier=tier, suggestions=suggestions
                            ,good_points=good_points, bad_points=bad_points, name=name)
