# 지정한 경로에 error.log 파일을 생성하고 에러 로그를 기록하는 모듈
import os
from .common_task import CommonLuigiTask
from functools import wraps

def handle_exceptions(func):
    @wraps(func)
    def wrapper(self:CommonLuigiTask, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            write_log(self.output_dir(), f"{self.__class__.__name__}: {e}")
            print(f"Error: {e}")
            raise e
    return wrapper

def write_log(path, message):
    """
    지정한 경로에 error.log 파일을 생성하고 에러 로그를 기록하는 함수
    :param path: 로그 파일을 생성할 경로
    :param message: 기록할 에러 메시지
    """
    with open(os.path.join(path, 'error.log'), 'a') as f:
        f.write(message + '\n')