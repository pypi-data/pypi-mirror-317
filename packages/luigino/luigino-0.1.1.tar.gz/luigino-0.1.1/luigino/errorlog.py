# 지정한 경로에 error.log 파일을 생성하고 에러 로그를 기록하는 모듈
import os
def write_log(path, message):
    """
    지정한 경로에 error.log 파일을 생성하고 에러 로그를 기록하는 함수
    :param path: 로그 파일을 생성할 경로
    :param message: 기록할 에러 메시지
    """
    with open(os.path.join(path, 'error.log'), 'a') as f:
        f.write(message + '\n')