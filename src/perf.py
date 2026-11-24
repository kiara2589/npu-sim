import time
from src.mac import mac

REPEAT_COUNT = 10

def measure_mac_ms(pattern, filt, repeat=REPEAT_COUNT):
    """
    I/O를 제외하고 mac() 연산 함수 호출 구간만 시간 측정.
    repeat 횟수만큼 반복 수행 후 평균 실행 시간(ms) 반환.
    """
    start_time = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filt)
    end_time = time.perf_counter()
    
    elapsed_total_sec = end_time - start_time
    avg_ms = (elapsed_total_sec / repeat) * 1000.0
    return avg_ms