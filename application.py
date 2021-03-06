import os

from flask import Flask, session, render_template, request, url_for, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd



app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/') #obtenemos un objeto llamado app
def index():
    return render_template('index.html')


@app.route('/login',methods = ['POST', 'GET'])
def login():
 # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/register',methods = ['POST', 'GET'])
def register():

    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            raise RuntimeError("Must provide Name", 400)
        
        if not request.form.get("Last Name"):
                raise RuntimeError ("Must provide Last Name", 400)
        
        if not request.form.get("Email"):
                raise RuntimeError ("Must provide Email", 400)

        if not request.form.get("password"):
            raise RuntimeError ("Must provide password", 400)

        if not request.form.get("confirmation"):
            raise RuntimeError ("Must provide confirmation", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            raise RuntimeError ("password doesn't match", 400)

        if len(db.execute("SELECT * FROM users WHERE username= :username", username=request.form.get("username"))) != 0:
            raise RuntimeError ("username taken :D", 400)

        password = generate_password_hash(request.form.get("password"))

        newUser = db.execute("INSERT INTO users(username, hash) VALUES(:user, :passw) ",
                             user=request.form.get("username"), passw=password)

        flash("Registered!")

        return redirect("/")
    else:
        return render_template("register.html")


@app.route('/Results')
def Results():
    
    return render_template('results.html')


    

if __name__ == '__main__': #con este archivo que hace el metodo de ejecucion
    app.run(debug=True)
