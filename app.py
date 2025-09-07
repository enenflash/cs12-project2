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
	return render_template('main_page.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        email=request.form["email"]
        first_name=request.form["first-name"]
        last_name=request.form["last-name"]
        password=request.form["password"]
        if email=="" or first_name=="" or last_name=="" or password=="":
            return render_template("create_account.html", message="All fields required.")
        volunteers = get_volunteers()
        if email in [volunteer["Email"] for volunteer in volunteers]:
            return render_template("create_account.html", message="Email already has an account.")
        if password != request.form["confirm-password"]:
            return render_template("create_account.html", message="Passwords do not match.")
        add_volunteer(first_name, last_name, email, password)
        session["UID"] = get_volunteers(f'Email="{email}"')[0]["ID"]
        return redirect(url_for("dashboard"))
    return render_template('create_account.html')

# ---------------------------------------------------------------------------- #
#                                   USER VIEW                                  #
# ---------------------------------------------------------------------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not email_valid(email):
            return render_template("login.html", message="Email not in database.")
        if not login_valid(email, password):
            return render_template("login.html", message="Incorrect password.")
        volunteer = get_volunteers(f'Email="{email}"')[0]
        session["UID"] = volunteer["ID"]
        session["Admin"] = volunteer["Admin"]
        return redirect(url_for("dashboard"))
    return render_template('login.html', message="")

@app.route('/account-details', methods=['GET', 'POST'])
def account_details():
    if "UID" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        alter_account_details(session["UID"], first_name=request.form["first-name"], last_name=request.form["last-name"], password=request.form["password"])
        volunteer = get_volunteers(f"ID={session['UID']}")[0]
        return render_template("account_details.html", volunteer=volunteer, message="Success")
    volunteer = get_volunteers(f"ID={session['UID']}")[0]
    return render_template('account_details.html', volunteer=volunteer, message="")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "UID" not in session:
        return redirect(url_for("login"))
    opportunities = get_taken_opportunities(f"VO.VolunteerID={session['UID']}")
    return render_template('dashboard.html', opportunities=opportunities)

@app.route('/volunteering', methods=['GET', 'POST'])
def volunteering():
    available_opportunities = get_available_opportunities()
    return render_template("volunteering.html", opportunities=available_opportunities)

@app.route('/events', methods=['GET', 'POST'])
def events():
    events = get_events()
    return render_template('events.html', events=events)

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == "POST":
        return render_template("event.html", event=event, perms=perms, message="Coming soon.")
        event_id = request.form["EventID"]
        event = get_events(f"Event.ID={event_id}")[0]
        perms = session["Admin"] if "Admin" in session else False
        if not perms:
            return render_template("event.html", event=event, perms=perms, message="You do not have permissions to edit events.")
        if request.form.get("delete"):
            delete_event(event_id)
            return redirect(url_for("events"))
        return render_template("event.html", event=event, perms=perms, message="Editing events coming soon.")
    
    event_id = request.args.get('id', default="-1")
    if event_id == "-1":
        return redirect(url_for("events"))
    event = get_events(f"Event.ID={event_id}")[0]
    perms = session["Admin"] if "Admin" in session else False
    return render_template("event.html", event=event, perms=perms, message="")

@app.route('/organisations', methods=['GET', 'POST'])
def organisations():
    organisations = get_organistaions()
    return render_template('organisations.html', organisations=organisations)

# ---------------------------------------------------------------------------- #
#                               ORGANISATION VIEW                              #
# ---------------------------------------------------------------------------- #

@app.route('/org-login', methods=['GET', 'POST'])
def org_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not org_email_valid(email):
            return render_template("organisation/org_login.html", message="Organisation email not in database.")
        if not org_login_valid(email, password):
            return render_template("organisation/org_login.html", message="Incorrect password.")
        organisation = get_organistaions(f'Email="{email}"')[0]
        session["OID"] = organisation["ID"]
        return redirect(url_for("org_dashboard"))
    return render_template('organisation/org_login.html', message="")

@app.route('/org-dashboard', methods=['GET', 'POST'])
def org_dashboard():
    if "OID" not in session:
        return redirect(url_for("org_login"))
    return render_template('organisation/org_dashboard.html')

@app.route('/org-events', methods=['GET', 'POST'])
def org_events():
    events = get_events()
    return render_template('organisation/org_events.html', events=events)

@app.route('/org-volunteers', methods=['GET', 'POST'])
def org_volunteers():
    skills = get_skills()
    volunteers = get_volunteers()

    if request.method == "POST":
        query = request.form["search"]
        skill = request.form["skill-id"]
        volunteers_involved = request.form.get('volunteers-involved')
        if query != "":
            volunteers = filter_volunteers_by_query(volunteers, query)
        if skill != "-":
            volunteers = filter_volunteers_by_skill(volunteers, skill)
        if volunteers_involved:
            if "OID" not in session:
                return redirect(url_for("org_login"))
            volunteers = filter_volunteers_by_involved(volunteers, session["OID"])
        return render_template('organisation/org_volunteers.html', volunteers=volunteers, skills=skills)

    return render_template('organisation/org_volunteers.html', volunteers=volunteers, skills=skills)

if __name__ == "__main__":
    use_ip = input("Use private IP (Y/N): ")
    ip = get_local_ip() if use_ip=="Y" else "127.0.0.1"
    print(ip)
    app.run(host=ip, port=1234, debug=True)