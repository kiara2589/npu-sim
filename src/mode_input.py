from src.mac import mac
from src.judge import judge
from src.perf import measure_mac_ms

def parse_number(token):
    try:
        val = float(token)
        return int(val) if val.is_integer() else val
    except ValueError:
        raise ValueError("숫자 변환 실패")

def read_matrix_from_console(name, n=3):
    print(f"\n{name} ({n}줄 입력, 공백 구분)")
    while True:
        rows = []
        valid = True
        for i in range(n):
            line = input(f"{i+1}행: ").strip()
            parts = line.split()
            if len(parts) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                valid = False
                break
            try:
                row_nums = [parse_number(p) for p in parts]
                rows.append(row_nums)
            except ValueError:
                print("입력 형식 오류: 유효한 숫자를 입력하세요.")
                valid = False
                break
        if valid:
            return rows

def run_mode_input():
    print("\n#----------------------------------#")
    print("# [1] 필터 입력 (3x3)")
    print("#----------------------------------#")
    filt_a = read_matrix_from_console("필터 A", 3)
    filt_b = read_matrix_from_console("필터 B", 3)
    
    print("\n#----------------------------------#")
    print("# [2] 패턴 입력 (3x3)")
    print("#----------------------------------#")
    pattern = read_matrix_from_console("패턴", 3)
    
    score_a = mac(pattern, filt_a)
    score_b = mac(pattern, filt_b)
    
    time_a = measure_mac_ms(pattern, filt_a)
    time_b = measure_mac_ms(pattern, filt_b)
    avg_time = (time_a + time_b) / 2.0
    
    verdict = judge(score_a, score_b, label_a="A", label_b="B")
    if verdict == "UNDECIDED":
        verdict_str = f"판정 불가 (|A-B| < 1e-9)"
    else:
        verdict_str = verdict

    print("\n#----------------------------------#")
    print("# [3] MAC 결과")
    print("#----------------------------------#")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time:.4f} ms")
    print(f"판정: {verdict_str}")