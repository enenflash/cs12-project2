import sqlite3
DB_PATH = "community_connect.db"

MONTHS = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "June",
    "07": "July", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}
DATES = { "1": "st", "2": "nd", "3": "rd" }

# ---------------------------------------------------------------------------- #

def format_day(day:str) -> str:
    if day[1] not in DATES or day[0] == "1":
        return (day if day[0] != "0" else day[1]) + "th"
    return (day if day[0] != "0" else day[1]) + DATES[day[1]]

def format_date(date:str) -> str:
    # YYYY:mm::dd
    month = date[5:7] if date[5:7] not in MONTHS else MONTHS[date[5:7]]
    day = date[8:10]
    return f"{day}/{month}/{date[:4]}"

def format_time(time:str) -> str:
    if time == None:
        return time
    # HH:MM:SS
    hours = int(time[:2])
    minutes = time[3:5]
    ampm = "AM"
    if hours > 12:
        hours -= 12
        ampm = "PM"
    return f"{hours}:{minutes} {ampm}"

# ---------------------------------------------------------------------------- #

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_table(command:str) -> list:
    with get_db() as conn:
        cursor = conn.cursor()
        result = cursor.execute(command).fetchall()
        return result

def get_row(command:str) -> sqlite3.Row:
    with get_db() as conn:
        cursor = conn.cursor()
        result = cursor.execute(command).fetchone()
        return result

def run_command(command:str) -> None:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()

# ---------------------------------- SELECT ---------------------------------- #

def get_volunteers() -> list:
    command = f"""
        SELECT * FROM Volunteer;
    """
    return get_table(command)

def get_organistaions(where:str="TRUE") -> list:
    command = f"""
        SELECT * FROM Organisation WHERE {where};
    """
    return get_table(command)

def get_event_types_for_event(event_id:int) -> list:
    command = f"""
        SELECT EventType.Name FROM EventTypeJunction 
        INNER JOIN EventType ON EventTypeJunction.TypeID=EventType.ID
        WHERE EventTypeJunction.EventID={event_id};
    """
    event_types = get_table(command)
    return [et["Name"] for et in event_types]

def get_events(where:str="TRUE") -> list:
    command = f"""
        SELECT * FROM Event 
        INNER JOIN Organisation ON Event.OrganisationID=Organisation.ID
        INNER JOIN Location ON Event.LocationID=Location.ID
        WHERE {where};
    """
    events:list[dict] = get_table(command)
    for i in range(len(events)):
        events[i] = dict(events[i])
        events[i]["type"] = get_event_types_for_event(events[i]["ID"])
    return events

# ---------------------------------- MODIFY ---------------------------------- #

def alter_account_details(id:int, first_name:str=None, last_name:str=None, password:str=None):
    # TODO Check password security/Validate length
    command = f"""
        SELECT * FROM Volunteer WHERE ID={id};
    """
    volunteer_info = get_row(command)
    if first_name == None:
        first_name = volunteer_info["FirstName"]
    if last_name == None:
        last_name = volunteer_info["LastName"]
    if password == None:
        password = volunteer_info["password"]
    command = f"""
        UPDATE Volunteer SET FirstName="{first_name}", LastName="{last_name}", Password="{password}" WHERE ID={id};
    """
    run_command(command)

# ------------------------------------ ADD ----------------------------------- #

def add_volunteer(first_name:str, last_name:str, email:str, password:str):
    command = f"""
        INSERT INTO Volunteer (FirstName, LastName, Email, Password) VALUES
        ("{first_name}", "{last_name}", "{email}", "{password}");
    """
    run_command(command)

def add_organisation(name:str):
    command = f"""
        INSERT INTO Organistaion (Name) VALUES ("{name}");
    """
    run_command(command)

# TODO Add event function

# -------------------------------- CHECK VALID ------------------------------- #

def email_valid(email:str) -> bool:
    volunteers:list = get_volunteers()
    if email in [row["Email"] for row in volunteers]:
        return True
    return False

def password_valid(password:str) -> bool:
    volunteers:list = get_volunteers()
    if password in [row["Password"] for row in volunteers]:
        return True
    return False