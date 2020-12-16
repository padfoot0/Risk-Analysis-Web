from flask import Flask , render_template , request , make_response
from flask.helpers import send_file
from flask.wrappers import Response
import connection
from connection import registerDetail,loginDetails
app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/' , methods = ['GET' , 'POST'])
def login():
    emId = request.form['empId']
    password = request.form['password']
    result = loginDetails(emId , password)
    if result == False:
        return "False"
    else:
        return  render_template('main.html')

# @app.route('/register' , methods = ['GET' , 'POST'])
# def register():
#     name = request.form['name']
#     eId = request.form['eId']
#     password = request.form['password']
#     password1 = request.form['password1']
#     print(name , eId , password)
#     if password == password1:
#         registerDetail(name , eId , password)
#     else:
#         print("data inserted")



app.run(debug= True)