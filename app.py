from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# 데이터베이스 파일 경로 설정
DATABASE = os.path.join(app.root_path, 'instance', 'bus_data.db')

# 특정 버스 번호에 따른 정류장 목록 가져오기
def get_bus_stops_by_bus_number(bus_number):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 특정 버스 번호의 정류장 정보 가져오기
        cursor.execute("""
            SELECT b.bus_number, s.departure_first, s.departure_last, s.interval_weekday, s.interval_weekend, s.route 
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            WHERE b.bus_number = ?
        """, (bus_number,))
        row = cursor.fetchone()
        bus_info = {
            'bus_number': row[0],
            'departure_first': row[1],
            'departure_last': row[2],
            'interval_weekday': row[3],
            'interval_weekend': row[4],
            'route': row[5]
        } if row else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        bus_info = None
    finally:
        conn.close()
    
    return bus_info

# 검색어에 따른 버스 목록 가져오기
def search_buses(query=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        if query:
            # 검색어가 버스 번호나 경로에 포함된 버스 정보 가져오기
            cursor.execute("""
                SELECT b.bus_number, s.departure_first, s.departure_last, s.interval_weekday, s.interval_weekend, s.route 
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
                WHERE b.bus_number LIKE ? OR s.route LIKE ?
            """, ('%' + query + '%', '%' + query + '%'))
        else:
            # 전체 버스 목록 가져오기
            cursor.execute("""
                SELECT b.bus_number, s.departure_first, s.departure_last, s.interval_weekday, s.interval_weekend, s.route 
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            """)
        
        buses = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        buses = []
    finally:
        conn.close()
    
    return buses

# 메인 페이지
@app.route('/')
def home():
    bus_list = [
        {"bus_number": "6", "direction": "셀트리온2공장 앞 방면"},
        {"bus_number": "8", "direction": "인천대정문 방면"},
        {"bus_number": "6-1", "direction": "알앤디써비스 방면"},
        {"bus_number": "3002", "direction": "인천대정문 방면"},
        {"bus_number": "8A", "direction": "인천대정문 방면"},
        {"bus_number": "1301", "direction": "미추홀공원 방면"},
    ]
    return render_template('index.html', bus_list=bus_list)

# 버스 정보 페이지
@app.route('/bus/<bus_number>')
def bus_info(bus_number):
    bus_info = get_bus_stops_by_bus_number(bus_number)
    return render_template('bus_info.html', bus_info=bus_info)

# 검색 페이지
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_results = search_buses(query)
    return render_template('search.html', search_results=search_results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
