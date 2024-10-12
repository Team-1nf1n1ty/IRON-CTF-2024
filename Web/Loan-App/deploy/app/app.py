from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import os
import re
import uuid


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI') or 'mongodb://mongo:27017/loanApp'
app.secret_key = os.getenv('SECRET_KEY') or 'secretKey'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
FLAG = os.getenv('FLAG') or 'ironCTF{testing_flag}'

@app.route('/')
def index():
    if 'user_id' in session:
        loans = mongo.db.loan.find({'user_id': session['user_id']})
        return render_template('index.html', loans=loans)
    return redirect(url_for('login'))

def is_uuid_v4(uuid_str):
    uuid_v4_regex = re.compile(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)
    
    return bool(uuid_v4_regex.match(uuid_str))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not isinstance(username, str) or not isinstance(password, str):
            flash('Both username and password must be strings', 'danger')
            return redirect(url_for('register'))

        if not is_uuid_v4(username) or not is_uuid_v4(password):
            flash('Both username and password must be valid uuidV4', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.user.insert_one({'username': username, 'password': hashed_password})
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not isinstance(username, str) or not isinstance(password, str):
            flash('Both username and password must be strings', 'danger')
            return redirect(url_for('login'))

        if not is_uuid_v4(username) or not is_uuid_v4(password):
            flash('Both username and password must be valid UUIDs', 'danger')
            return redirect(url_for('login'))

        user = mongo.db.user.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/loan-request', methods=['POST'])
def loan_request():
    if 'user_id' in session:
        amount = request.form['amount']
        reason = request.form['reason']
        mongo.db.loan.insert_one({'user_id': session['user_id'], 'amount': amount, 'reason': reason, 'status': 'pending'})
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/admin/loan/<loan_id>', methods=['POST'])
def admin_approve_loan(loan_id):
    try:
        mongo.db.loan.update_one({'_id': ObjectId(loan_id)}, {'$set': {'status': 'approved', 'message': FLAG}})
        return 'OK', 200
    except:
        return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(port=5050)
