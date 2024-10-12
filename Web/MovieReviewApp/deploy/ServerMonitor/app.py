from flask import Flask, render_template, request, redirect, url_for, flash, session
import psutil
import os
import platform
import subprocess
import re
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(32)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD =  os.getenv('ADMIN_PASSWORD')
app.config['APPLICATION_ROOT'] = '/servermonitor'

@app.route('/servermonitor/')
def home():
    return render_template('index.html')

    
@app.route('/servermonitor/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"{username}::::{password}")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash(f"Invalid credentials. Please try again.")
    
    return render_template('login.html')

def ping_ip(ip, count):
    if re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', ip):
        try:
            result = subprocess.run(
                f"/usr/bin/ping -c {count} {ip}",
                shell=True,
                capture_output=True,  # Captures both stdout and stderr
                text=True              # Decodes output as string
            )
            if result.stderr:
                return result.stdout + result.stderr
            
            return result.stdout
        except subprocess.CalledProcessError as e:
            return str(e)

    else:
        return "Invalid ip address and count!"
    

@app.route('/servermonitor/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if 'logged_in' not in session:
        return redirect(url_for('admin'))
    ping_result = None
    if request.method == 'POST':
        ip = request.form.get('ip')
        count = request.form.get('count', 1)
        try:
            ping_result = ping_ip(ip, count)
        except ValueError:
            flash("Count must be a valid integer")
        except Exception as e:
            flash(f"An error occurred: {e}")

    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    total_memory = memory_info.total / (1024 ** 2) 
    available_memory = memory_info.available / (1024 ** 2) 
    return render_template('admin.html', ping_result=ping_result, memory_usage=memory_usage)

@app.route('/servermonitor/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
