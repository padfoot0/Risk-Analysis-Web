from flask import Flask , render_template , request , make_response , session , redirect
from flask.wrappers import Response
app= Flask(__name__)
app.secret_key = "kaaeret"
# import getPredictions
from getPredictions import getPredictions
# import connection
from connection import finalAlgorithm
from connection import displayDatas
from connection import multipleCompany,loginDetails,registerDetail,allCompanySearched,selectNameOfUser
import pdfkit
import os
import pandas as pd

@app.route('/')
def home():
    if "user" in session:
        companyNames = allCompanySearched()
        length = len(companyNames)
        name = session["user"]
        return  render_template('index.html' ,userName = name , companyNo = length , company = companyNames)
    return render_template("login.html")

@app.route('/signup')
def signup():
    if "user" in session:
        companyNames = allCompanySearched()
        length = len(companyNames)
        name = session["user"]
        return  render_template('index.html' , userName = name , companyNo = length , company = companyNames)
    return render_template("signup.html")


@app.route('/' , methods = ['GET' , 'POST'])
def login():
    emId = request.form['empId']
    password = request.form['password']
    result = loginDetails(emId , password)
    if result == False:
        return "False"
    else:
        name = selectNameOfUser(emId)
        session["user"] = name[0][0] 
        companyNames = allCompanySearched()
        length = len(companyNames)
        return  render_template('index.html' ,userName = name[0][0] , companyNo = length , company = companyNames)




@app.route('/signup' , methods = ['GET' , 'POST' ])
def signupDetail():
    name = request.form['empName']
    empId = request.form['empId']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    if pass1 == pass2 :
        session["user"] = name
        registerDetail(name , empId , pass1)
        companyNames = allCompanySearched()
        length = len(companyNames)
        return  render_template('index.html',userName = name , companyNo = length , company = companyNames)
    else:
        return "both Password should be same"




@app.route('/search')
def search():
    if "user" in session:
        name = session["user"]
        return render_template("search.html" , userName = name)
    return redirect("/")


@app.route('/csv')
def csv():
    if "user" in session:
        name = session["user"]
        return render_template("csvfile.html" , userName = name)
    return redirect("/")


@app.route('/display')
def display():
    if "user" in session:
        name = session["user"]
        return render_template("display.html" , userName = name)
    return redirect("/")

@app.route('/dashbord')
def dashbord():
    if "user" in session:
        companyNames = allCompanySearched()
        name = session["user"]
        length = len(companyNames)
        return  render_template('index.html' ,userName = name , companyNo = length , company = companyNames)
    return redirect("/")


@app.route('/search', methods = ["GET", "POST"])
def CompanyName():
    if "user" in session:
        companyName = request.form["companyName"]
        print(companyName)
        finalAlgorithm(companyName)
        return "search complete"
    return redirect("/")

@app.route('/filecsv' , methods = ['GET' , 'POST'])
def csvFile():
    if "user" in session:
        companyNamesData = request.form['fileaccept']
        data = pd.read_csv(companyNamesData)
        if 'company' in data.columns:
            arr = data.to_numpy()
            print(data.head())
            print(arr)
            multipleCompany(arr)
            return "wha"
        else:
            return "wrong "
    return redirect("/")

@app.route('/display', methods = ["GET" , "POST"])
def displayFormate():
    if "user" in session:
        displayType = request.form["displayFormate"]
        companyName = request.form["companyName"]
        urldatas = displayDatas(companyName , displayType)
        rendered = render_template("dataDisplay.html" , lengthOfUrl = len(urldatas) , urls = urldatas)
        pdf = pdfkit.from_string(rendered ,False)
        response = make_response(pdf)
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']= 'inline; filename=output.pdf'
        return response
    return redirect("/")

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user" , None)
        return redirect("/")
    return redirect("/")


app.run(debug= True)