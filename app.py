from flask import Flask, render_template, request, redirect, url_for

import sqlite3 #SQLITE DB 작업을 위한 모듈 import
import os #파일 경로 작업을 위한 import

app = Flask(__name__) #FLASK app 객체 생성

# 데이터베이스 파일 경로 설정
DATABASE = os.path.join(app.root_path, 'instance', 'bus_data.db')

# 특정 버스 번호에 따른 정류장 목록 가져오는 함수
def get_bus_stops_by_bus_number(bus_number):
    conn = sqlite3.connect(DATABASE) #DB 연결 생성
    cursor = conn.cursor() #cursor 객체 생성
    
    try:
        # 특정 버스 번호의 정류장 정보
        cursor.execute("""
            SELECT b.bus_number, s.departure_first, s.departure_last, s.interval_weekday, s.interval_weekend, s.route 
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            WHERE b.bus_number = ?
        """, (bus_number,)) #특정 버스 번호의 정보를 bus_Info와 bus_schedule 테이블에서 join
        
        row = cursor.fetchone()#첫번째 결과
        bus_info = {
            'bus_number': row[0],
            'departure_first': row[1],
            'departure_last': row[2],
            'interval_weekday': row[3],
            'interval_weekend': row[4],
            'route': row[5]
        } if row else None #결과 존재 시 dictionary로 변환 없으면 반환

    except sqlite3.Error as e:
        print(f"Database error: {e}") # DB오류 발생 시 출력
        bus_info = None # 오류 발생 시 None 반환
    finally:
        conn.close() # DB 연결 연결 닫기
    
    return bus_info # 버스 정보 반환

# 검색어에 따른 버스 목록 가져오는 함수
def search_buses(query=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        if query:
            cursor.execute("""
                SELECT DISTINCT b.bus_number, s.departure_first, s.departure_last, 
                                s.interval_weekday, s.interval_weekend, s.route
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
                WHERE b.bus_number LIKE ? OR s.route LIKE ?
            """, ('%' + query + '%', '%' + query + '%'))
        else:
            cursor.execute("""
                SELECT DISTINCT b.bus_number, s.departure_first, s.departure_last, 
                                s.interval_weekday, s.interval_weekend, s.route
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            """)
        
        buses = cursor.fetchall()
        print("Fetched buses:", buses)  # 검색 결과 출력
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        buses = []
    finally:
        conn.close()
    
    return buses


# 메인 페이지
@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)  # 데이터베이스 연결
    cursor = conn.cursor()
    try:
        # 데이터베이스에서 버스 정보 가져오기
        cursor.execute("""
            SELECT DISTINCT b.bus_number, s.route
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            ORDER BY b.bus_number ASC
        """)
        bus_list = [{"bus_number": row[0], "direction": row[1]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        bus_list = []  # 오류 발생 시 빈 목록 반환
    finally:
        conn.close()  # 연결 닫기

    # 메인 페이지 템플릿 렌더링
    return render_template('index.html', bus_list=bus_list)





# 버스 정보 페이지
@app.route('/bus/<bus_number>')
def bus_info(bus_number):
    bus_info = get_bus_stops_by_bus_number(bus_number) #특성 버스 번호의 정보를 가져오기
    return render_template('bus_info.html', bus_info=bus_info) # 버스 정보 페이지 템플릿을 랜더링하여 정보 전달


# 검색 페이지
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '') # 검색어를 get 요청에서 가져옴
    search_results = search_buses(query) # 검색 결과를 가져옴
    return render_template('search.html', search_results=search_results, query=query) # 검색 결과 페이지 랜더링


# 버스 목록 삭제
@app.route('/delete-bus', methods=['POST'])
def delete_bus():
    bus_number = request.form.get('bus_number')  # 삭제할 버스 번호를 POST 요청에서 가져옴
    if bus_number:
        conn = sqlite3.connect(DATABASE)  # DB 연결 생성
        cursor = conn.cursor()  # cursor 객체 생성
        try:
            # 데이터베이스에서 해당 버스 번호 삭제
            cursor.execute("DELETE FROM Bus_Info WHERE bus_number = ?", (bus_number,))
            conn.commit()  # 변경 사항 commit
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # DB 오류 발생 시 출력
        finally:
            conn.close()  # DB 연결 닫기

    return redirect(url_for('home'))  # 메인 페이지로 redirect


# 버스 정보 수정 페이지
@app.route('/edit-bus/<bus_number>', methods=['GET'])
def edit_bus(bus_number):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        # Bus_Info와 Bus_Schedule 테이블 조인
        cursor.execute("""
            SELECT b.bus_id, b.bus_number, s.route, s.interval_weekday, s.interval_weekend, s.departure_first, s.departure_last
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            WHERE b.bus_number = ?
        """, (bus_number,))
        bus = cursor.fetchone()
        if not bus:
            return "Bus not found", 404
        bus_data = {
            'bus_id': bus[0],
            'bus_number': bus[1],
            'route': bus[2],
            'interval_weekday': bus[3],
            'interval_weekend': bus[4],
            'departure_first': bus[5],
            'departure_last': bus[6],
        }
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Internal Server Error", 500
    finally:
        conn.close()
    return render_template('edit_bus.html', bus=bus_data)


# 버스 정보 업데이트
@app.route('/update-bus', methods=['POST'])
def update_bus():
    bus_id = request.form.get('bus_id')  # 수정할 버스 ID 가져오기
    new_route = request.form.get('route')  # 새로운 경로 정보 가져오기
    new_interval_weekday = request.form.get('interval_weekday')  # 새로운 평일 배차 간격 정보 가져오기
    new_interval_weekend = request.form.get('interval_weekend')
    new_departure_first = request.form.get('departure_first')
    new_departure_last = request.form.get('departure_last')

    if bus_id:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Bus_Schedule
                SET route = ?, interval_weekday = ?, interval_weekend = ?, departure_first = ?, departure_last = ?
                WHERE bus_id = ?
            """, (new_route, new_interval_weekday, new_interval_weekend, new_departure_first, new_departure_last, bus_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return "Internal Server Error", 500
        finally:
            conn.close()

    return redirect(url_for('home'))


# 버스 목록 추가
@app.route('/add-bus', methods=['GET', 'POST'])
def add_bus():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        bus_number = request.form.get('bus_number')
        route = request.form.get('route')
        interval_weekday = request.form.get('interval_weekday')
        interval_weekend = request.form.get('interval_weekend')
        departure_first = request.form.get('departure_first')
        departure_last = request.form.get('departure_last')

        if bus_number and route:  # 필수 데이터 확인
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            try:
                # Bus_Info에 추가
                cursor.execute("INSERT INTO Bus_Info (bus_number) VALUES (?)", (bus_number,))
                bus_id = cursor.lastrowid  # 방금 추가된 Bus_Info의 ID 가져오기

                # Bus_Schedule에 추가
                cursor.execute("""
                    INSERT INTO Bus_Schedule (bus_id, route, interval_weekday, interval_weekend, departure_first, departure_last)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (bus_id, route, interval_weekday, interval_weekend, departure_first, departure_last))
                conn.commit()  # 데이터베이스에 변경사항 적용
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            finally:
                conn.close()

        return redirect(url_for('home'))  # 메인 페이지로 리다이렉트

    return render_template('add_bus.html')

# FlASK app 실행
if __name__ == '__main__':
    app.run(debug=True) #디버그 모드로 Flask app 실행
