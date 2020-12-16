from flask import Flask , render_template , request , make_response
from flask.wrappers import Response
app= Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

app.run(debug= True)