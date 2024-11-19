# Flask 웹 프레임워크에서 사용하는 필수 모듈
# `render_template`는 HTML 템플릿 렌더링
# `request`는 클라이언트 요청 데이터를 처리
# `redirect`와 `url_for`는 URL 리다이렉트에 사용
from flask import Flask, render_template, request, redirect, url_for

# SQLite 데이터베이스와 상호작용하기 위한 모듈
import sqlite3
# 운영 체제 파일 경로 및 작업에 관련된 모듈
import os
# Flask 애플리케이션 객체를 생성
app = Flask(__name__)

# 데이터베이스 파일 경로 설정
# 주 데이터베이스 파일 경로를 `DATABASE`에 저장
# 각 버스 번호에 따른 데이터베이스 파일이 저장된 폴더 경로를 `DATABASE_FOLDER`에 저장
DATABASE = os.path.join(app.root_path, 'instance', 'bus_data.db')
DATABASE_FOLDER = os.path.join(app.root_path, 'databases')

# 데이터베이스에 특정 버스 번호에 따른 정류장 목록 가져오는 함수
def get_bus_stops_by_bus_number(bus_number):
    # 주 데이터베이스(`bus_data.db`)와 연결
    conn = sqlite3.connect(DATABASE) 
    cursor = conn.cursor()
    # 데이터베이스 쿼리를 실행하기 위한 커서를 생성

    # SQL 쿼리를 실행합니다.# SQL 쿼리를 실행하여 `Bus_Info`와 `Bus_Schedule` 테이블을 조인하고
    # 특정 버스 번호에 대한 정보를 검색합니다.
    # `bus_number`를 문자열로 변환하여 쿼리에 전달합니다.
    try:
        cursor.execute("""
            SELECT b.bus_number, s.departure_first, s.departure_last, 
                   s.interval_weekday, s.interval_weekend, s.route 
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            WHERE b.bus_number = ?
        """, (str(bus_number),))  
        
        # 쿼리 결과에서 첫 번째 행
        row = cursor.fetchone()
        # 결과가 존재하면 딕셔너리 형태로 변환하고, 그렇지 않으면 `None`을 반환
        bus_info = {
            'bus_number': row[0],
            'departure_first': row[1],
            'departure_last': row[2],
            'interval_weekday': row[3],
            'interval_weekend': row[4],
            'route': row[5]
        } if row else None
    
    # 데이터베이스 오류가 발생하면 에러 메시지를 출력
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        bus_info = None
    finally:
        # 데이터베이스 연결을 닫기
        conn.close()

    return bus_info
    # 버스 정보를 반환합니다.

# 버스 번호.db 파일에서 쿼리 실행 함수
def query_db_from_file(db_path, query, args=(), one=False):
    conn = sqlite3.connect(db_path)
    # 주어진 데이터베이스 파일(`db_path`)에 연결
    conn.row_factory = sqlite3.Row
    # 쿼리 결과를 딕셔너리 형태로 반환하도록 설정
    cur = conn.cursor()
    # 커서를 생성하여 쿼리를 실행

    cur.execute(query, args)
    # 주어진 쿼리(`query`)와 매개변수(`args`)를 실행
    rv = cur.fetchall()
    # 쿼리 결과
    conn.close()
    # 데이터베이스 연결을 닫기

    # 하나의 결과만 필요한 경우 첫 번째 결과를 반환하고, 그렇지 않으면 전체 결과를 반환합니다.
    return (rv[0] if rv else None) if one else rv


@app.route('/bus/<bus_number>/details')
def bus_details(bus_number):
    """
    특정 버스 번호의 정류장 목록을 가져와 렌더링합니다.
    """
    db_path = os.path.join(DATABASE_FOLDER, f"{bus_number}.db")
    # 해당 버스 번호의 데이터베이스 파일 경로를 생성합니다.

    if not os.path.exists(db_path):
        # 데이터베이스 파일이 존재하지 않는 경우, 빈 데이터를 렌더링합니다.
        return render_template('bus_details.html', bus_info=None, stops=[])

    stops = query_db_from_file(db_path, "SELECT id, name, stop_id FROM bus_stops ORDER BY id")
    # 정류장 데이터를 데이터베이스에서 가져옵니다.
    bus_info = {"bus_number": bus_number, "route": "Route not specified"}
    # 기본 버스 정보를 설정합니다.
    
    return render_template('bus_details.html', bus_info=bus_info, stops=stops)
    # 정류장 목록과 버스 정보를 렌더링하여 반환합니다.

#검색어에 따라 데이터베이스에서 버스목록 검색
def search_buses(query=None):
    conn = sqlite3.connect(DATABASE)
    # 주 데이터베이스에 연결합니다.
    cursor = conn.cursor()
    # 쿼리를 실행하기 위한 커서를 생성합니다.

    
    try:
        if query:
            # `query`를 기준으로 버스 번호나 경로를 검색합니다.
            cursor.execute("""
                SELECT DISTINCT b.bus_number, s.departure_first, s.departure_last, 
                                s.interval_weekday, s.interval_weekend, s.route
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
                WHERE CAST(b.bus_number AS TEXT) LIKE ? OR s.route LIKE ?
            """, ('%' + query + '%', '%' + query + '%'))  
        else:
            # 검색어가 없으면 전체 데이터를 가져옵니다.
            cursor.execute("""
                SELECT DISTINCT b.bus_number, s.departure_first, s.departure_last, 
                                s.interval_weekday, s.interval_weekend, s.route
                FROM Bus_Info AS b
                JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            """)
        buses = cursor.fetchall()
        # 검색 결과를 가져옵니다.

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # 데이터베이스 오류가 발생하면 에러 메시지를 출력합니다.
        buses = []
        # 오류 발생 시 빈 리스트를 반환합니다.

    finally:
        conn.close()
        # 데이터베이스 연결을 닫습니다.

    return buses
    # 검색된 버스 목록을 반환합니다.

#메인 페이지
@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)
    # 주 데이터베이스에 연결합니다.
    cursor = conn.cursor()
    # 데이터베이스 쿼리를 실행하기 위한 커서를 생성합니다.

    try:
        cursor.execute("""
            SELECT DISTINCT b.bus_number, s.route
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            ORDER BY b.bus_number ASC
        """)
        # 버스 정보와 경로를 가져오는 SQL 쿼리를 실행합니다.
        bus_list = [{"bus_number": row[0], "direction": row[1]} for row in cursor.fetchall()]
        # 쿼리 결과를 딕셔너리 형태로 변환하여 버스 목록을 저장합니다.

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # 데이터베이스 오류가 발생하면 메시지를 출력합니다.
        bus_list = []
        # 오류 발생 시 빈 목록을 반환합니다.

    finally:
        conn.close()
        # 데이터베이스 연결을 닫습니다.

    return render_template('index.html', bus_list=bus_list)
    # 메인 페이지를 렌더링하면서 버스 목록을 전달합니다.

#버스 정보 페이지
@app.route('/bus/<bus_number>')
def bus_info(bus_number):
    bus_info = get_bus_stops_by_bus_number(bus_number)
    # `get_bus_stops_by_bus_number` 함수를 호출하여 특정 버스 번호의 정보를 가져옵니다.
    return render_template('bus_info.html', bus_info=bus_info)
    # 버스 정보를 포함하여 페이지를 렌더링합니다.

#검색 결과 페이지
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '') 
    # GET 요청에서 검색어를 가져옵니다. 검색어가 없으면 빈 문자열을 기본값으로 설정합니다.
    search_results = search_buses(query)
    # 검색어를 기반으로 버스 목록을 검색합니다.
    return render_template('search.html', search_results=search_results, query=query)
    # 검색 결과와 검색어를 포함하여 검색 페이지를 렌더링합니다.

#버스 삭제 함수
@app.route('/delete-bus', methods=['POST'])
def delete_bus():
    bus_number = request.form.get('bus_number')
    # 삭제할 버스 번호를 POST 요청 데이터에서 가져옵니다.

    if bus_number:
        conn = sqlite3.connect(DATABASE)
        # 주 데이터베이스에 연결합니다.
        cursor = conn.cursor()
        # 데이터베이스 쿼리를 실행하기 위한 커서를 생성합니다.
        try:
            cursor.execute("DELETE FROM Bus_Info WHERE bus_number = ?", (bus_number,))
            # `Bus_Info` 테이블에서 특정 버스 번호를 삭제하는 SQL 쿼리를 실행합니다.
            conn.commit()
            # 변경 사항을 커밋하여 데이터베이스에 적용합니다.

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            # 데이터베이스 오류 발생 시 메시지를 출력합니다.

        finally:
            conn.close()
            # 데이터베이스 연결을 닫습니다.

    return redirect(url_for('home'))
    # 삭제 후 메인 페이지로 리다이렉트합니다.

#버스 정보 수정 페이지
@app.route('/edit-bus/<bus_number>', methods=['GET'])
def bus_edit(bus_number):
    conn = sqlite3.connect(DATABASE)
    # 주 데이터베이스에 연결합니다.
    cursor = conn.cursor()
    # 데이터베이스 쿼리를 실행하기 위한 커서를 생성합니다.

    try:
        cursor.execute("""
            SELECT b.bus_id, b.bus_number, s.route, s.interval_weekday, 
                   s.interval_weekend, s.departure_first, s.departure_last
            FROM Bus_Info AS b
            JOIN Bus_Schedule AS s ON b.bus_id = s.bus_id
            WHERE b.bus_number = ?
        """, (bus_number,))
        # 특정 버스 번호에 대한 정보를 검색하는 SQL 쿼리를 실행합니다.
        bus = cursor.fetchone()
        # 쿼리 결과를 가져옵니다.

        if not bus:
            return "Bus not found", 404
            # 결과가 없으면 404 오류를 반환합니다.

        bus_data = {
            'bus_id': bus[0],
            'bus_number': bus[1],
            'route': bus[2],
            'interval_weekday': bus[3],
            'interval_weekend': bus[4],
            'departure_first': bus[5],
            'departure_last': bus[6],
        }
        # 결과를 딕셔너리로 변환하여 저장합니다.

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # 데이터베이스 오류 발생 시 메시지를 출력합니다.
        return "Internal Server Error", 500

    finally:
        conn.close()
        # 데이터베이스 연결을 닫습니다.

    return render_template('bus_edit.html', bus=bus_data)
    # 수정 페이지를 렌더링하며 버스 정보를 전달합니다.

#수정 데이터 데이터베이스에 적용
@app.route('/update-bus', methods=['POST'])
def update_bus():
    bus_id = request.form.get('bus_id')
    # 수정할 버스 ID를 POST 요청 데이터에서 가져옵니다.
    new_route = request.form.get('route')
    # 수정할 경로 정보를 가져옵니다.
    new_interval_weekday = request.form.get('interval_weekday')
    # 수정할 평일 배차 간격을 가져옵니다.
    new_interval_weekend = request.form.get('interval_weekend')
    # 수정할 주말 배차 간격을 가져옵니다.
    new_departure_first = request.form.get('departure_first')
    # 수정할 첫차 시간을 가져옵니다.
    new_departure_last = request.form.get('departure_last')
    # 수정할 막차 시간을 가져옵니다.

    if bus_id:
        conn = sqlite3.connect(DATABASE)
        # 주 데이터베이스에 연결합니다.
        cursor = conn.cursor()
        # 데이터베이스 쿼리를 실행하기 위한 커서를 생성합니다.

        try:
            cursor.execute("""
                UPDATE Bus_Schedule
                SET route = ?, interval_weekday = ?, interval_weekend = ?, 
                    departure_first = ?, departure_last = ?
                WHERE bus_id = ?
            """, (new_route, new_interval_weekday, new_interval_weekend, 
                  new_departure_first, new_departure_last, bus_id))
            # Bus_Schedule 테이블에서 특정 버스의 정보를 업데이트하는 SQL 쿼리를 실행합니다.
            conn.commit()
            # 변경 사항을 커밋하여 데이터베이스에 적용합니다.

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            # 데이터베이스 오류 발생 시 메시지를 출력합니다.
            return "Internal Server Error", 500

        finally:
            conn.close()
            # 데이터베이스 연결을 닫습니다.

    return redirect(url_for('home'))
    # 업데이트 후 메인 페이지로 리다이렉트합니다.

#새로운 버스 목록에 추가
@app.route('/add-bus', methods=['GET', 'POST'])
def add_bus():
    if request.method == 'POST':
        bus_number = request.form.get('bus_number')
        # 추가할 버스 번호를 POST 요청 데이터에서 가져옵니다.
        route = request.form.get('route')
        # 추가할 경로 정보를 가져옵니다.
        interval_weekday = request.form.get('interval_weekday')
        # 추가할 평일 배차 간격을 가져옵니다.
        interval_weekend = request.form.get('interval_weekend')
        # 추가할 주말 배차 간격을 가져옵니다.
        departure_first = request.form.get('departure_first')
        # 추가할 첫차 시간을 가져옵니다.
        departure_last = request.form.get('departure_last')
        # 추가할 막차 시간을 가져옵니다.

        if bus_number and route:
            # 필수 데이터가 존재하는 경우 실행합니다.
            conn = sqlite3.connect(DATABASE)
            # 주 데이터베이스에 연결합니다.
            cursor = conn.cursor()
            # 데이터베이스 쿼리를 실행하기 위한 커서를 생성합니다.

            try:
                cursor.execute("INSERT INTO Bus_Info (bus_number) VALUES (?)", (bus_number,))
                # Bus_Info 테이블에 새 버스를 추가하는 SQL 쿼리를 실행합니다.
                bus_id = cursor.lastrowid
                # 새로 추가된 버스 ID를 가져옵니다.

                cursor.execute("""
                    INSERT INTO Bus_Schedule (bus_id, route, interval_weekday, 
                                              interval_weekend, departure_first, departure_last)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (bus_id, route, interval_weekday, interval_weekend, departure_first, departure_last))
                # Bus_Schedule 테이블에 상세 정보를 추가합니다.
                conn.commit()
                # 데이터베이스 변경 사항을 저장합니다.

            except sqlite3.Error as e:
                print(f"Database error: {e}")
                # 데이터베이스 오류 발생 시 메시지를 출력합니다.

            finally:
                conn.close()
                # 데이터베이스 연결을 닫습니다.

        return redirect(url_for('home'))
        # 추가 후 메인 페이지로 리다이렉트합니다.

    return render_template('bus_add.html')
    # GET 요청 시 버스 추가 페이지를 렌더링합니다.


if __name__ == '__main__':
    app.run(debug=True)
    # 디버그 모드로 Flask 애플리케이션을 실행합니다.
