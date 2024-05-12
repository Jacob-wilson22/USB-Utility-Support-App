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
