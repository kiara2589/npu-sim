import json
import os
from src.mac import mac
from src.judge import judge, normalize_label
from src.perf import measure_mac_ms
from src.matrix import is_square, make_cross, make_x

def parse_size_from_key(key):
    parts = key.split("_")
    if len(parts) >= 2 and parts[0] == "size":
        try:
            return int(parts[1])
        except ValueError:
            return None
    return None

def run_mode_json(file_path="data.json"):
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일을 찾을 수 없습니다.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"오류: JSON 파일 로드 실패 ({e})")
        return

    raw_filters = data.get("filters", {})
    raw_patterns = data.get("patterns", {})

    print("\n#----------------------------------#")
    print("# [1] 필터 로드")
    print("#----------------------------------#")
    filters = {}
    for size_key, filt_dict in raw_filters.items():
        n = parse_size_from_key(size_key)
        if n is None:
            continue
        
        parsed_subfilters = {}
        for fk, fval in filt_dict.items():
            norm_fk = normalize_label(fk)
            if norm_fk and is_square(fval, n):
                parsed_subfilters[norm_fk] = fval
        
        if "Cross" in parsed_subfilters and "X" in parsed_subfilters:
            filters[n] = parsed_subfilters
            print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")

    print("\n#----------------------------------#")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#----------------------------------#")
    
    total_count = 0
    pass_count = 0
    fail_count = 0
    fail_cases = []
    
    measured_sizes = set()
    size_perf_records = {}

    for pat_key, pat_info in raw_patterns.items():
        total_count += 1
        n = parse_size_from_key(pat_key)
        
        if n is None or n not in filters:
            fail_count += 1
            reason = f"필터 스키마 미지원 크기 (N={n})"
            fail_cases.append((pat_key, reason, "데이터/스키마"))
            print(f"{pat_key} --- [FAIL] ({reason})")
            continue
            
        pat_input = pat_info.get("input")
        raw_expected = pat_info.get("expected")
        expected_label = normalize_label(raw_expected)
        
        if not is_square(pat_input, n):
            fail_count += 1
            reason = f"패턴 배열 크기 불일치 (기대: {n}x{n})"
            fail_cases.append((pat_key, reason, "데이터/스키마"))
            print(f"{pat_key} --- [FAIL] ({reason})")
            continue

        cross_filt = filters[n]["Cross"]
        x_filt = filters[n]["X"]
        
        score_cross = mac(pat_input, cross_filt)
        score_x = mac(pat_input, x_filt)
        
        verdict = judge(score_cross, score_x, label_a="Cross", label_b="X")
        
        is_pass = (verdict == expected_label)
        status_str = "PASS" if is_pass else "FAIL"
        
        if is_pass:
            pass_count += 1
        else:
            fail_count += 1
            if verdict == "UNDECIDED":
                reason = f"동점(UNDECIDED) 처리 규칙 적용 (Cross={score_cross}, X={score_x})"
                category = "수치 비교"
            else:
                reason = f"판정 불일치 (판정: {verdict}, expected: {expected_label})"
                category = "로직"
            fail_cases.append((pat_key, reason, category))

        print(f"{pat_key} ---")
        print(f"  Cross 점수: {score_cross}")
        print(f"  X 점수    : {score_x}")
        print(f"  판정      : {verdict} | expected: {expected_label} | {status_str}")
        
        if n not in measured_sizes:
            measured_sizes.add(n)
            t_cross = measure_mac_ms(pat_input, cross_filt)
            t_x = measure_mac_ms(pat_input, x_filt)
            size_perf_records[n] = (t_cross + t_x) / 2.0

    print("\n#----------------------------------#")
    print("# [3] 성능 분석 (평균 10회 측정)")
    print("#----------------------------------#")
    
    all_sizes_to_report = sorted(list(set([3] + list(filters.keys()))))
    print(f"{'크기(NxN)':<12} | {'평균 시간(ms)':<15} | {'연산 횟수(N²)':<12}")
    print("-" * 46)
    
    for s in all_sizes_to_report:
        if s == 3 and 3 not in size_perf_records:
            sample_p = make_cross(3)
            sample_f = make_cross(3)
            avg_t = measure_mac_ms(sample_p, sample_f)
        else:
            avg_t = size_perf_records.get(s, 0.0)
        
        op_count = s * s
        print(f"{f'{s}x{s}':<12} | {avg_t:<15.4f} | {op_count:<12}")

    print("\n#----------------------------------#")
    print("# [4] 결과 요약")
    print("#----------------------------------#")
    print(f"총 테스트: {total_count}개")
    print(f"통과     : {pass_count}개")
    print(f"실패     : {fail_count}개")
    
    if fail_cases:
        print("\n실패 케이스 목록:")
        for pk, rsn, cat in fail_cases:
            print(f" - {pk} [{cat}]: {rsn}")
    else:
        print("\n실패 케이스가 없습니다 (ALL PASS).")