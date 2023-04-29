from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return "register"

@app.route("/dashboard")
def dashboard():
    return "dashboard"

@app.route("/analysis")
def analysis():
    return "analysis"

app.run(debug=True)