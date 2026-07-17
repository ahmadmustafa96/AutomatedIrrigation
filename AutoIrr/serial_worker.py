import os
import serial
import sqlite3
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200

def serial_reader_worker(db_path):
    print(f"[Serial Worker] Connecting to ESP32 on {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("[Serial Worker] Connected and listening...")
        while True:
            if ser.in_waiting > 0:
                raw_line = ser.readline().decode('utf-8').strip()
                if raw_line:
                    try:
                        temp_str, mois_str = raw_line.split(',')
                        temperature = float(temp_str)
                        moisture = float(mois_str)
                        
                        conn = sqlite3.connect(db_path, timeout=10)
                        conn.execute('PRAGMA journal_mode=WAL;')
                        cursor = conn.cursor()

                        cursor.execute("SELECT irrigation_status, selected_crop FROM settings WHERE id = 1")
                        settings = cursor.fetchone()
                        irrigation_status = settings[0] if settings else 0
                        selected_crop = settings[1] if settings else 'wheat'

                        cursor.execute(
                            """INSERT INTO readings (temperature, moisture, irrigation, crop) 
                               VALUES (?, ?, ?, ?)""", 
                            (temperature, moisture, irrigation_status, selected_crop)
                        )

                        conn.commit()
                        conn.close()
                        print(f"[Logged] Temp: {temperature}°C | Mois: {moisture}% | Irrigation: {irrigation_status} | Crop: {selected_crop}")
                        time.sleep(1)
                    except ValueError:
                        print(f"[Serial Warning] Parsing issue with line: {raw_line}")
            time.sleep(1)
    except Exception as e:
        print(f"[Serial Error] Lost connection: {e}. Retrying in 10 seconds...")
        time.sleep(10)
        serial_reader_worker(db_path)