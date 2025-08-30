import socket
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

from flask import Flask, render_template, redirect, request, url_for
from models import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
	return render_template('home.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    return render_template('create_account.html')

if __name__ == "__main__":
    use_ip = input("Use private IP (Y/N): ")
    ip = get_local_ip() if use_ip=="Y" else "127.0.0.1"
    print(ip)
    app.run(host=ip, port=1234, debug=True)