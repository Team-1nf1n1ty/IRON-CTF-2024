from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from load_dotenv import load_dotenv
import os
from base64 import b64decode, b64encode
from uuid import uuid4

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "your_secret_key_here"
FLAG = os.getenv("FLAG") or "ironCTF{FAKE_FLAG_FOR_TESTING}"
INVITE_KEY = os.getenv("INVITE_KEY") or "SAMPLE_INVITE_KEY"
# MongoDB connection

mongo_url=os.getenv("MONGODB_URL") or 'mongodb://localhost:27017/'
client = MongoClient(mongo_url)
db = client['database']

# Users collection
users_collection = db['users']
portfolio_collection = db['portfolio']  
selections_collection = db['selection']

@app.after_request
def set_csp_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'none'; script-src 'self' ; style-src 'self' 'unsafe-inline' ; img-src *;"
    return response
    
# Routes
@app.route('/') 
def home():
    if 'user' in session:
        return redirect(url_for("profile"))
    return render_template('index.html', not_logged_in=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('profile'))
    not_logged_in=True
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        interview_code = request.form.get('interview_code')
        invite_key = request.form.get('invite_code')

        # Check if user with given email already exists
        if users_collection.find_one({'email': email}):
            return "User with this email already exists!"
        if len(password) < 8:
            return "Password should be atleast 8 characters."
        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Create a new user document
        user_data = {
            'name': name,
            'email': email,
            'hash_password': hashed_password,
        }

        # Add interview code if provided
        if interview_code and INVITE_KEY == invite_key :
            user_data['role'] = 'recruiter'
            user_data["interview_code"] = interview_code
        else:
            user_data['role'] = 'human'
            user_data["interview_code"] = "NONE"

        # Insert the user into the database
        users_collection.insert_one(user_data)

        return redirect(url_for('login'))

    return render_template('register.html', not_logged_in=not_logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('profile'))
    not_logged_in=True
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists in the database
        user = users_collection.find_one({'email': email})

        if user:
            # Check if the password is correct
            if check_password_hash(user['hash_password'], password):
                session['user'] = user['email']
                return redirect(url_for('profile'))

        return 'Invalid email or password'

    return render_template('login.html', not_logged_in=not_logged_in)

@app.route('/profile')
def profile():
    if 'user' in session:
        email = session['user']
        user = users_collection.find_one({'email': email})
        if user:
            portfolios = list(portfolio_collection.find({'email': email}))
            return render_template('profile.html', user=user, portfolios=portfolios)
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('login'))

@app.route('/profile/shortlisted')
def shortlisted():
    if 'user' in session:
        email = session['user']
        user = users_collection.find_one({'email': email})
        if user:
            offers = list(selections_collection.find({'email': email}))
            return render_template('shortlisted.html', user=user, offers=offers)
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('login'))


@app.route('/portfolio/create', methods=['GET', 'POST'])
def create_portfolio():
    if 'user' in session:
        email = session['user']
        user = users_collection.find_one({'email': email})
        if user and user.get('role') == 'human':
            if request.method == 'POST':
                session_email = session['user']
                user = users_collection.find_one({'email': session_email})
                if user:
                    title = request.form.get('title')
                    portfolio_content = request.form.get('portfolio_content')
                    portfolio_collection.insert_one({
                        'portfolio_id':uuid4().hex,
                        'email': session_email,
                        'title': title,
                        'portfolio_content': b64encode(portfolio_content.encode("utf-8")).decode("utf-8")
                    })
                    return redirect(url_for('profile'))
                else:
                    return "User not found"
            if 'user' in session:
                return render_template('create_portfolio.html')
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/portfolio/<portfolio_id>/view', methods=['GET', 'POST'])
def view_portfolio(portfolio_id):
    portfolio = list(portfolio_collection.find({'portfolio_id': portfolio_id}))
    if len(portfolio) >0:
        portfolio = portfolio[0]
        return render_template('view_portfolio.html', user=portfolio["email"], title=portfolio["title"], portfolio_content=portfolio["portfolio_content"] )

@app.route('/recruiter/select', methods=['POST'])
def select_human():
    print(session)
    if 'user' in session:
        try:
            user_email = b64decode(request.form["email"]).decode()
        except: 
            return "ERROR decoding email..."
        admin_user = users_collection.find_one({'email': session["user"]})
        if admin_user and admin_user['role'] == 'recruiter':
            if request.method == "POST":
                if request.form.get("remark") == "SELECT NOW!!":
                    selections_collection.insert_one({
                    'email': user_email,
                    'interview_link': FLAG
                    })
                else:
                    selections_collection.insert_one({
                    'email': user_email,
                    'interview_link': admin_user["interview_code"]
                    })
                return "Success"
        else:
            return "Access denied. Only recruiters can access this page."
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5050)
