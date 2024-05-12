import sqlite3


# Queries floor_name from rooms table
def query_floors():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT floor_name FROM rooms")
    floor_data = cursor.fetchall()
    floor_data = [str(val[0]) for val in floor_data]
    return floor_data


# Queries room_id an room_name from rooms based on value of floor_name
def query_rooms(floor_name):
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, room_name FROM rooms WHERE floor_name=?", (floor_name,))
    room_data = cursor.fetchall()
    return room_data


# Queries floor_name from rooms table based on value of room_id
def query_floor_name(room_id):
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT floor_name FROM rooms WHERE room_id=?", (room_id,))
    floor_name_data = cursor.fetchone()
    if floor_name_data:
        floor_name = floor_name_data[0]  # Extract the first element from the tuple
    else:
        floor_name = None
    cursor.close()
    conn.close()
    return floor_name


# Queries room_name from rooms table based on value of room_id
def query_room_name(room_id):
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_name FROM rooms WHERE room_id=?", (room_id,))
    room_name_data = cursor.fetchone()  # Use fetchone() to get a single row
    if room_name_data:
        room_name = room_name_data[0]  # Extract the first element from the tuple
    else:
        room_name = None
    cursor.close()
    conn.close()
    return room_name


# Queries device_name from rooms table based on value of room_id
def query_devices(room_id):
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT device_name FROM devices WHERE room_id=?", (room_id,))
    device_data = cursor.fetchall()
    device_data = [str(val[0]) for val in device_data]
    return device_data


# Queries fault_id, fault_type, fault_severity from faults table
def query_faults():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fault_id, fault_type, fault_severity FROM faults")
    fault_data = cursor.fetchall()
    return fault_data


# Queries all attributes from fault_log
def query_fault_log():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fault_log")
    fault_log_data = cursor.fetchall()
    return fault_log_data

# Queries all fault_type values and the frequency they occur in fault_log table.
def query_fault_type_freq():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fault_type, COUNT(*) FROM fault_log GROUP BY fault_type")
    fault_type_freq = cursor.fetchall()
    return fault_type_freq


# Queries all floor_name values and the frequency they occur in fault_log table.
def query_floor_freq():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT floor_name, COUNT(*) FROM fault_log GROUP BY floor_name")
    floor_freq = cursor.fetchall()
    return floor_freq


# Queries all room_name values and the frequency they occur in fault_log table.
def query_room_freq():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_name, COUNT(*) FROM fault_log GROUP BY room_name")
    room_freq = cursor.fetchall()
    return room_freq


# Queries username from users table
def query_user_data():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    username_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [username[0] for username in username_data]


# Queries role form users table based on value of variable username.
def query_user_role_data(username):
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=?", (username,))
    user_role_data = cursor.fetchone()  # Use fetchone() to get only one row
    conn.close()
    return user_role_data[0] if user_role_data else None  # Return role or None if no data found


# Queries all attributes from tasks table
def query_task_data():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    task_data = cursor.fetchall()
    return task_data


# Queries what month an entry occurred based on the month string value
def query_month_data():
    conn = sqlite3.connect('instance/Diss.db')
    cursor = conn.cursor()
    cursor.execute("""
            SELECT 
                CASE WHEN strftime('%m', log_date) ="01" Then "JAN" 
                WHEN strftime('%m', log_date) ="02" Then "FEB" 
                WHEN strftime('%m', log_date) ="03" THEN "MAR" 
                WHEN strftime('%m', log_date) ="04" THEN "APR" 
                WHEN strftime('%m', log_date) ="05" THEN "MAY" 
                WHEN strftime('%m', log_date) ="06" THEN "JUN" 
                WHEN strftime('%m', log_date) ="07" THEN "JUL" 
                WHEN strftime('%m', log_date) ="08" THEN "AUG" 
                WHEN strftime('%m', log_date) ="09" THEN "SEP" 
                WHEN strftime('%m', log_date) ="10" THEN "OCT" 
                WHEN strftime('%m', log_date) ="11" THEN "NOV" 
                WHEN strftime('%m', log_date) ="12" THEN "DEC" 
                END AS log_month,
                COUNT(*) AS entry_count
            FROM 
                fault_log
            GROUP BY 
                log_month
            ORDER BY 
                CASE 
                    WHEN strftime('%m', log_date) ="01" THEN 1 
                    WHEN strftime('%m', log_date) ="02" THEN 2 
                    WHEN strftime('%m', log_date) ="03" THEN 3 
                    WHEN strftime('%m', log_date) ="04" THEN 4 
                    WHEN strftime('%m', log_date) ="05" THEN 5 
                    WHEN strftime('%m', log_date) ="06" THEN 6 
                    WHEN strftime('%m', log_date) ="07" THEN 7 
                    WHEN strftime('%m', log_date) ="08" THEN 8 
                    WHEN strftime('%m', log_date) ="09" THEN 9 
                    ELSE CAST(strftime('%m', log_date) AS INTEGER) 
                END;
        """)
    month_data = cursor.fetchall()
    conn.close()
    return month_data
