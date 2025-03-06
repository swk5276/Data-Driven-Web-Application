---

# **Incheon University Bus Information Management System**
## **📌 프로젝트 개요**
본 프로젝트는 **Flask Web Framework**와 **SQLite**를 활용하여 **인천대학교 자연과학대학 정류장 운행 정보**를 제공하는 웹 애플리케이션입니다.  
사용자 중심의 UI/UX 설계를 통해 **실시간 버스 도착 정보**, **CRUD 기능**, **검색 및 즐겨찾기 관리** 등 다양한 기능을 제공합니다.  
웹 프레임워크와 데이터베이스를 유기적으로 연결하여 **효율적이고 직관적인 사용자 경험**을 제공합니다.

![웹어플리케이션](https://swk5276-a9dzecfaa5bagzca.eastasia-01.azurewebsites.net)

![image](https://github.com/user-attachments/assets/819ac5df-328f-464e-8cb7-dc06cb055a87)

---

## **🛠️ 개발 환경**
- **프레임워크**: Flask Web Framework  
- **프로그래밍 언어**: Python  
- **데이터베이스**: SQLite  
- **데이터 출처**:  
  - [네이버 지도 버스 검색](https://map.naver.com/p/bus/bus-route/-/bus-station/152834?c=11.00,0,0,0,dh)  
  - [인천 버스 정보](https://bus.incheon.go.kr/bis/main.view)

---

## **✨ 주요 기능**

### **1. CRUD 기능**
- **데이터 추가 (Create)**: `bus_add.html`을 통해 새로운 버스 정보를 입력하고 데이터베이스에 저장.  
- **데이터 조회 (Read)**: `index.html`과 `bus_info.html`에서 버스 목록과 세부 정보를 직관적으로 확인.  
- **데이터 수정 (Update)**: `bus_edit.html`에서 입력된 데이터를 업데이트하고 데이터베이스와 동기화.  
- **데이터 삭제 (Delete)**: `index.html`에서 특정 버스를 삭제할 수 있는 버튼 제공.

### **2. 실시간 검색 기능**
- 사용자가 입력한 검색어에 따라 **버스 번호, 운행 경로, 배차 간격**, **첫차/막차 시간** 등을 검색 가능.  
- 결과는 **카드 형식**으로 표시하며, 검색 결과가 없는 경우 적절한 안내 메시지를 제공하여 사용자 경험을 개선.

### **3. 사용자 중심의 UI/UX**
- **컬러 코딩 및 레이아웃**: 가독성을 높이고 직관적인 사용자 경험 제공.  
- **호버 효과**: 버튼과 입력 필드에 적용된 시각적 피드백으로 작업 흐름을 원활하게 지원.  
- **반응형 디자인**: 다양한 화면 크기에서도 정보를 명확히 전달.

### **4. 버스 상세 정보**
- `bus_details.html`에서 특정 버스의 **운행 경로와 정류장 정보**를 타임라인 형식으로 제공.  
- 사용자는 세부 정보와 전체 목록 간의 **간편한 탐색**이 가능.

### **5. 즐겨찾기 기능**
- 자주 이용하는 버스를 즐겨찾기로 등록하고 메인 페이지에서 빠르게 확인 가능.

---

## **📂 데이터베이스 구조**

### **1. 버스 개별 데이터베이스**
- 각 버스 번호에 해당하는 **정류장 정보를 별도 데이터베이스**로 관리.
- 주요 테이블: `bus_stops`  
  - **id**: 정류장 고유 식별자  
  - **name**: 정류장 이름  
  - **stop_id**: 시스템 고유 ID  

### **2. 중앙 데이터베이스**
- **bus_data.db**: 전체 버스 정보를 관리하는 중앙 데이터베이스.  
  - **Bus_Info**: 버스 ID, 번호, 운행 지역 관리.  
  - **Bus_Schedule**: 배차 간격, 첫차/막차 시간, 운행 경로 관리.  

### **3. 정류장 통합 데이터베이스**
- **bus_stops.db**: 모든 정류장 정보를 통합 관리하여 데이터 일관성 유지.  

---

## **🌐 주요 웹 페이지**

| 페이지                | 주요 기능                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| **index.html**        | 메인 페이지. 버스 목록, 검색, 즐겨찾기, 추가/삭제/수정 기능 제공.        |
| **bus_add.html**      | 새 버스 추가. 버스

번호, 배차 간격, 첫차/막차 시간 등의 데이터를 입력하여 데이터베이스에 저장.       |
| **bus_details.html**  | 특정 버스의 운행 경로와 정류장 정보를 타임라인 형식으로 표시.             |
| **bus_edit.html**     | 기존 버스 정보를 수정하여 데이터베이스와 동기화.                          |
| **bus_info.html**     | 특정 버스의 운행 정보(배차 간격, 첫차/막차 시간, 경로)를 상세히 표시.     |
| **search.html**       | 검색어 기반으로 버스 정보를 카드 형식으로 제공. 검색 결과가 없을 경우 안내 메시지 표시. |

---

## **🚀 Git Commit Log**
### **팀 구성원 및 작업 내역**
#### **김성웅 (202102939)**
- `2024_11_14_1`: Flask 기반 웹 페이지 기본 구조 구현.
- `2024_11_15_2`: 검색, 정보 표시, DB 연동 구현 및 스타일링 추가.
- `2024_11_17_3`: 버스 관리 시스템 정보 삭제, 수정 기능 추가 및 DB 처리 코드 정비.
- `2024_11_18_4`: 버스 추가 기능 구현, 검색 및 삭제 로직 개선, 사용자 인터페이스 업데이트.
- `2024_11_19_5`: 버스 상세 정보 페이지 추가, 템플릿 및 DB 구조 정리.
- `2024_11_25_6`: 즐겨찾기 기능 추가 및 메인 페이지 데이터 정렬 개선.
- `2024_11_26_7`: UI 스타일 개선 및 검색 필드와 버튼 레이아웃 업데이트.
- `2024_12_02_8`: 검색어 처리 코드 리팩토링 및 메인 페이지 로직 개선.

---

## **🎯 프로젝트 주요 성과**
1. **직관적이고 사용자 친화적인 웹 애플리케이션 구축**: 검색, CRUD, 즐겨찾기 등의 기능을 통해 편리한 데이터 관리 및 탐색 가능.  
2. **효율적인 데이터베이스 설계**: 중앙 및 개별 데이터베이스를 통해 데이터 일관성과 접근성을 모두 확보.  
3. **실시간 데이터 제공**: 공공 API를 활용하여 실시간 버스 도착 정보를 정확히 제공.  
4. **협업과 코드 관리**: 체계적인 Git 커밋 로그와 역할 분담을 통해 안정적인 프로젝트 진행.  

---

### **2. 프로젝트 클론**
```bash
git clone https://github.com/your-repository/Bus-Management-System.git
cd Bus-Management-System
```

### **3. 애플리케이션 실행**
```bash
python app.py
```

### **4. 브라우저에서 접속**
- http://127.0.0.1:5000

---
