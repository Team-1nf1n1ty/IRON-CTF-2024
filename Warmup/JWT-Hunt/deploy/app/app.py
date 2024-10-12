from flask import Flask, render_template, request, redirect, url_for, make_response, abort, send_from_directory
import jwt
import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Strong secret key divided into parts
SECRET_KEY_PARTS = [
    '6yH$#v9Wq3e&Zf8L',
    'pRt1%Y4nJ^aPk7Sd',
    '2C@mQjUwEbGoIhNy',
    '0T!BxlVz5uMKA#Yp'
]
SECRET_KEY = ''.join(SECRET_KEY_PARTS)

# Initialize the database with an admin user
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?)", 
              (generate_password_hash('admin'),))
    conn.commit()
    conn.close()

def clear_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()

init_db()

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Register: {username}:{password}")
        if username == 'admin':
            return "User already exists"
        
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "User already exists"
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login: {username}:{password}")
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[0], password) and username != 'admin':
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, SECRET_KEY, algorithm='HS256')
            
            # Clear the database after login
            clear_db()
            
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('token', token)
            resp.set_cookie('secret_key_part_2', SECRET_KEY_PARTS[1])
            return resp
        elif username == 'admin':
            return "Incorrect Password"
        else:
            return "Invalid credentials!"

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if data['username'] == 'admin':
            return redirect(url_for('admin'))
        return render_template('dashboard.html', username=data['username'])
    except jwt.ExpiredSignatureError:
        return "Token expired!"
    except jwt.InvalidTokenError:
        return "Invalid token!"

# Admin Route
@app.route('/admin')
def admin():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('not_admin'))
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if data['username'] == 'admin':
            return "Welcome admin, here's your flag : ironCTF{W0w_U_R34lly_Kn0w_4_L07_Ab0ut_JWT_3xp10r4710n!}"
        else:
            return redirect(url_for('not_admin'))
    except jwt.InvalidTokenError:
        return redirect(url_for('not_admin'))

# Not Admin Route
@app.route('/not_admin')
def not_admin():
    return render_template('not_admin.html')

# Secret Key Part 4 Route
@app.route('/secretkeypart4', methods=['GET', 'HEAD'])
def secretkeypart4():
    if request.method == 'HEAD':
        response = make_response("", 200)
        response.headers['Secret-Key-Part-4'] = SECRET_KEY_PARTS[3]
        return response
    return abort(400)

# robots.txt
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder,'robots.txt')

# Sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://example.com/</loc>
        <lastmod>2024-01-01</lastmod>
    </url>
    <url>
        <loc>http://example.com/register</loc>
        <lastmod>2024-01-01</lastmod>
    </url>
    <url>
        <loc>http://example.com/login</loc>
        <lastmod>2024-01-01</lastmod>
    </url>
    <url>
        <loc>http://example.com/dashboard</loc>
        <lastmod>2024-01-01</lastmod>
    </url>
    <!-- Third part of the secret key: 2C@mQjUwEbGoIhNy -->
</urlset>"""
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

if __name__ == '__main__':
    app.run(debug=True)
