import sqlite3


# Queries floor_name from rooms table
def query_floors():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT floor_name FROM rooms")
    floor_data = cursor.fetchall()
    floor_data = [str(val[0]) for val in floor_data]
    return floor_data