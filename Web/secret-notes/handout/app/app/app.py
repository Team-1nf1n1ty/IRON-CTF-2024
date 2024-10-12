from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import bcrypt 
from load_dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "your_secret_key"

app.config["MONGO_URI"] = os.getenv("MONGODB_URL") or "mongodb://localhost:27017/secretnotes"
mongo = PyMongo(app)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form["username"]})

        if existing_user is None:
            if len(request.form["password"]) < 8:
                flash("Use loong password....")
            else:
                hashpass = bcrypt.hashpw(
                    request.form["password"].encode("utf-8"), bcrypt.gensalt()
                )
                users.insert_one(
                    {
                        "username": request.form["username"],
                        "password": hashpass,
                        "name": request.form["name"][:31],
                    }
                )
                session["username"] = request.form["username"]
                return redirect(url_for("profile"))
        else:
            flash("Username already exists! Try logging in.")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({"username": request.form["username"]})

        if login_user:
            if bcrypt.checkpw(
                request.form["password"].encode("utf-8"), login_user["password"]
            ):
                session["username"] = request.form["username"]
                return redirect(url_for("profile"))

        flash("Invalid username/password combination")
        return redirect(url_for("login"))

    return render_template("login.html")
    

@app.route("/profile")
def profile():
    if "username" in session:
        login_user = mongo.db.users.find_one({"username": session["username"]})
        if login_user:
            return render_template(" profile.html", name=login_user["name"], username=login_user["username"])

        flash("Invalid username/password combination")
        return redirect(url_for("login"))

    flash("You need to log in first.")
    return redirect(url_for("login"))


@app.route("/create", methods=["GET", "POST"])
def create_notes():
    if request.method == "POST":
        if "username" in session:
            login_user = mongo.db.users.find_one({"username": session["username"]})
            if login_user:
                new_item = {
                    "title": request.form["title"],
                    "content": request.form["content"],
                }
                mongo.db.users.update_one(
                    {"username": session["username"]}, {"$push": {"contents": new_item}}
                )
                return render_template("success.html")
            
            flash("You need to log in first.")
            return redirect(url_for("login"))

    return render_template("create.html")


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "username" in session:
        login_user = mongo.db.users.find_one({"username": session["username"]})
        if login_user:
            if "contents" in login_user:
                return render_template("notes.html", notes=login_user["contents"])
            else:
                return redirect(url_for("create_notes"))
                
    flash("You need to log in first.")
    return redirect(url_for("login"))



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5000)
