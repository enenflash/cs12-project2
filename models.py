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