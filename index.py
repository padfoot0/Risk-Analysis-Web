from flask import Flask , render_template , request , make_response
from flask.wrappers import Response
app= Flask(__name__)
import getPredictions
from getPredictions import getPredictions
import connection
from connection import finalAlgorithm
from connection import displayDatas
from connection import multipleCompany
import pdfkit
import os
import pandas as pd

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/', methods=["GET","POST"])
def searchFormate():
     type = request.form["getValue"]
     print(type)
     if type == "single":
         return render_template("index.html")
     elif type == "csv":
         return render_template("takeInputCsvFile.html")
     elif type == "display":
         return  render_template("displaydata.html")
     else:
         return "Select right Input"

@app.route('/single', methods = ["GET", "POST"])
def CompanyName():
    companyName = request.form["companyName"]
    print(companyName)
    finalAlgorithm(companyName)
    return companyName

@app.route('/filecsv' , methods = ['GET' , 'POST'])
def csvFile():
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

@app.route('/display')
def displayData():
    return render_template("displayData.html")

@app.route('/display', methods = ["GET" , "POST"])
def displayFormate():
    displayType = request.form["displayFormate"]
    companyName = request.form["companyName"]
    urldatas = displayDatas(companyName , displayType)
    print(len(urldatas))
    rendered = render_template("dataDisplay.html" , lengthOfUrl = len(urldatas) , urls = urldatas)
    pdf = pdfkit.from_string(rendered ,False)
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']= 'inline; filename=output.pdf'
    return response


app.run(debug= True)