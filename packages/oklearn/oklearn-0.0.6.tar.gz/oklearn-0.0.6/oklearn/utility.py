import time
from functools import wraps

def measure_execution_time(func):
    @wraps(func)  # 원래 함수의 메타데이터(예: 함수 이름, 문서 문자열 등)를 유지함
    def wrapper(*args, **kwargs):
        # 시작 시간 기록
        start_time = time.time()
        print(f"start {func.__name__}")
        # 함수 실행
        result = func(*args, **kwargs)
        print(f"end {func.__name__}")
        # 종료 시간 기록
        end_time = time.time()
        
        # 실행 시간 계산
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.1f} seconds")
        
        return result
    return wrapper
