def mac(pattern, filt):
    """
    외부 라이브러리 없이 이중 반복문으로 구현한 MAC (Multiply-Accumulate) 연산.
    위치별 곱셈 값을 모두 누적하여 반환.
    """
    total = 0.0
    n = len(pattern)
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total