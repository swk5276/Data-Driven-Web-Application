from flask import Flask, request, redirect, url_for 

import sqlite3
import os
app = Flask(__name__)
#DB 파일 경로 설정
Database = os.path.join(app.root_path, 'data.db')

def get_db_bus_stop_list(bus_number):
    #DB와 연결
    cursor = sqlite3.connect(Database).cursor()

    #sql 쿼리 실행 
    try:
        cursor.execute  (
        """
        SELECT b.bus_number, s.departure_first, s.departure_last, s.destination_first, s.destination_last, s.departure_time, s.arrival_time, s.stop_time, s.is_circular_route
        """
        (str(bus_number),))
        
        row = cursor.fetchone()
        bus_info = {
            'bus_number': row[0],
            'departure_first': row[1],
            'departure_last': row[2],
            'destination_first': row[3],
            'destination_last': row[4],
            'departure_time': row[5],
            'arrival_time': row[6],
        } if row else None
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        bus_info = None
    finally:
        cursor.close()
    return bus_info

def get_db_bus_stop_times(bus_number):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()



    
        