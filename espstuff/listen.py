import serial
import sqlite3
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200
DB_FILE = 'sensor_data.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS readings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temp REAL,
        humid REAL
    )'''
)
conn.commit()

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Listening on {SERIAL_PORT}")

except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            raw_line = ser.readline().decode('utf-8').strip()

            if raw_line:
                print(f"Raw Data: {raw_line}")

                try:
                    temp_str, hum_str = raw_line.split(',')
                    temp = float(temp_str)
                    humid = float(hum_str)

                    cursor.execute(
                        "INSERT INTO readings (temp, humid) VALUES(?, ?)"
                        ,(temp, humid)
                    )
                    conn.commit()
                    print(f"Successfully stored: Temp={temp}°C, Hum={humid}%")
                    
                except ValueError:
                    print(f"Malformed data received, skipping: {raw_line}")

except KeyboardInterrupt:
    print("\nStopping script...")
finally:
    ser.close()
    conn.close()
    print("Serial port and database connections closed.")