## 파이썬 소스 코드

### 1. `src/matrix.py` (데이터 구조 및 유틸리티)
```python
def make_matrix(n, fill=0.0):
    """n x n 크기의 2차원 리스트 생성"""
    return [[float(fill) for _ in range(n)] for _ in range(n)]

def is_square(matrix, expected_n):
    """행/열 크기가 expected_n과 정확히 일치하는지 검증"""
    if not isinstance(matrix, list) or len(matrix) != expected_n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != expected_n:
            return False
    return True

def make_cross(n):
    """n x n 크기의 십자가(Cross) 패턴 생성"""
    mat = make_matrix(n, 0.0)
    mid = n // 2
    for i in range(n):
        mat[i][mid] = 1.0
        mat[mid][i] = 1.0
    return mat

def make_x(n):
    """n x n 크기의 X 패턴 생성"""
    mat = make_matrix(n, 0.0)
    for i in range(n):
        mat[i][i] = 1.0
        mat[i][n - 1 - i] = 1.0
    return mat