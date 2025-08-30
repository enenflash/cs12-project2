from flask import Flask, session, render_template, redirect, request, url_for
from models import *
import socket, secrets

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/', methods=['GET', 'POST'])
def main_page():
	return render_template('home.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    return render_template('create_account.html')

@app.route('/account-details', methods=['GET', 'POST'])
def account_details():
    return render_template('account_details.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/events', methods=['GET', 'POST'])
def events():
    return render_template('events.html')

@app.route('/organisations', methods=['GET', 'POST'])
def organisations():
    return render_template('organisations.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if not email_valid(request.form['email']):
            return render_template("login.html", message="Email not in database.")
        if not password_valid(request.form['password']):
            return render_template("login.html", message="Incorrect password.")
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for("home"))
    return render_template('login.html', message="")

if __name__ == "__main__":
    use_ip = input("Use private IP (Y/N): ")
    ip = get_local_ip() if use_ip=="Y" else "127.0.0.1"
    print(ip)
    app.run(host=ip, port=1234, debug=True)