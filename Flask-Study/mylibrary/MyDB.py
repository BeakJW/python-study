from sqlalchemy import create_engine

config = {
 'username': 'root', # 접속할 사용자 이름
 'password': '1234', # 접속할 사용자의 비밀번호
 'hostname': 'localhost', # 접속할 시스템 주소 (내 컴퓨터인 경우 localhost)
 'port': 9090, # 설치시 설정한 포트번호 (기본값: 3306)
 'database': 'myschool', # 사용할 데이터베이스 이름
 'charset': 'utf8mb4' # 한글 깨짐 방지 (데이터베이스의 설정과 동일하게 지정)
}

# 데이터베이스 접속 함수
def connect():
    global conn  # 함수 외부의 변수를 함수 안으로 끌고 들어옴

    con_str_tpl = "mariadb+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset={charset}"
    con_str = con_str_tpl.format(**config)
    engine = create_engine(con_str)
    conn = engine.connect()

    return conn

# 데이터베이스 접속 해제 함수
def disconnect():
    global conn  # 함수 외부의 변수를 함수 안으로 끌고 들어옴

    if conn != None:
        conn.close()


if __name__ == "__main__":
    connect()
    disconnect()