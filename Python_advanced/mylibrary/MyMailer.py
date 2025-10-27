# -> 경로 정보를 취득하기 위한 모듈
import os
# -> 발송서버와 연동하기 위한 모듈
from smtplib import SMTP
# -> 본문 구성 기능
from email.mime.text import MIMEText
# -> 파일을 Multipart 형식으로 변환
from email.mime.application import MIMEApplication
# -> 파일을 본문에 추가하는 기능 제공
from email.mime.multipart import MIMEMultipart

#----------------------------------------
# 메일 발송 함수
#----------------------------------------
def sendMail(from_addr, to_addr, subject, content, files=[]):
    content_type = "plain"

    username="jnwoo97@gmail.com"

    password = "xkwb ptvt pmob tzip"

    # 구글 발송 서버 주소와 포트 (고정값)
    smtp = "smtp.gmail.com"
    port = 587

    # 네이버 발송 서버 주소와 포트 (고정값)
    # smtp = "smtp.naver.com"
    # port = 465

    # 메일 발송 정보를 저장하기 위한 객체
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 메일 제목
    msg['From'] = from_addr   # 보내는 사람
    msg['To'] = to_addr       # 받는 사람

    # 본문 설정 -> 메일의 내용과 형식 지정
    msg.attach(MIMEText(content, content_type))

    # 리스트 변수의 원소가 하나라도 존재할 경우 True
    if files:
        for file_item in files:
            if os.path.exists(file_item):
            # 바이너리(b) 형식으로 읽기(r)
                with open(file_item, 'rb') as f:
                    # 전체 경로에서 파일의 이름만 추출
                    basename = os.path.basename(file_item)
                    # 파일의 내용과 파일이름을 메일에 첨부할 형식으로 변환
                    part = MIMEApplication(f.read(), Name=basename)
                    # 파일첨부
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename
                    msg.attach(part)
                    print(basename, "(이)가 첨부되었습니다.")

    # 메일 서버 접속 및 발송
    mail = SMTP(smtp, port)
    mail.ehlo()         # 메일 서버 접속
    mail.starttls()     # TLS 설정
    mail.login(username, password)  # 로그인
    mail.sendmail(from_addr, to_addr, msg.as_string())  # 메일 보내기
    mail.quit()         # 접속 종료


if __name__ == "__main__":
    sendMail("jnwoo97@gmail.com","babujinwoo97@gmail.com",
             "메일 발송 모듈 테스트", "이것은 테스트 입니다.")
