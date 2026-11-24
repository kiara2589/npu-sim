import sys
from src.mode_input import run_mode_input
from src.mode_json import run_mode_json

def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    
    choice = input("선택 (1/2): ").strip()
    if choice == "1":
        run_mode_input()
    elif choice == "2":
        run_mode_json("data.json")
    else:
        print("잘못된 선택입니다. 프로그램을 종료합니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()