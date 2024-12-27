import os
import time
import shutil

# 특정 경로의 파일을 삭제하는 함수
def remove_if_old(path: str, age_limit: float, is_dir: bool = False):
    item_age = time.time() - os.path.getctime(path)
    
    if item_age > age_limit:
        try:
            if is_dir:
                shutil.rmtree(path)
                print(f"폴더 삭제됨: {path}")
            else:
                os.remove(path)
                print(f"파일 삭제됨: {path}")
        except Exception as e:
            print(f"삭제 실패: {path}, 오류: {e}")

# 지정 시간  이상된 파일 및 폴더 삭제
def cleanup_stale_items(path: str, hours: int = 1):
    if not os.path.exists(path):
        print(f"경로가 존재하지 않습니다: {path}")
        return
    age_limit = hours * 60 * 60
    # 파일 및 폴더 순회
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            remove_if_old(os.path.join(root, file), age_limit)
        for dir in dirs:
            remove_if_old(os.path.join(root, dir), age_limit, is_dir=True)

