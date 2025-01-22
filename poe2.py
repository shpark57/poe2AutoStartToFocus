import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pywinauto import Application
import sys
import pygetwindow as gw
import shutil
import atexit

# 1. Selenium으로 웹 페이지 접속 및 kgPoe.launch('poe2') 실행
def launch_game():
    # Chrome 드라이버 설정
    chrome_options = Options()
    chrome_options.add_argument(r"user-data-dir=C:\poe2_cache")  # Chrome 프로필 경로 설정

    # 드라이버 시작
    driver = webdriver.Chrome(options=chrome_options)

    # 페이지 열기
    driver.get("https://pathofexile2.game.daum.net/start/poe2")
    driver.maximize_window()

    # kgPoe.launch('poe2') 실행
    driver.execute_script("kgPoe.launch('poe2');")
    print("kgPoe.launch('poe2') 실행됨.")

    # 게임 실행될 때까지 기다리기
    wait_for_game()

    # 게임 창에 포커스 이동 및 클릭
    focus_game_window()

    # Selenium 드라이버 종료
    driver.quit()

# 2. 게임 실행 후 PathOfExile_KG.exe 실행 대기
def wait_for_game():
    print("게임 실행 대기 중...")
    while True:
        try:
            output = subprocess.check_output('tasklist', shell=True, universal_newlines=True)
            if 'PathOfExile_KG.exe' in output:
                print("게임 실행됨")
                break
        except subprocess.CalledProcessError as e:
            print(f"프로세스 확인 중 오류 발생: {e}")
        time.sleep(3)

# 3. 두 번째 'Path of Exile 2' 게임 창에 포커스 이동
def focus_game_window():
    try:
        app = Application(backend="uia").connect(path="PathOfExile_KG.exe")
        time.sleep(5)  # 첫 번째 창이 나타나기까지 기다림
        # pywinauto로 실행된 게임 창에 연결
        # 게임 창이 올바르게 로드될 때까지 대기
        print("게임 창 로딩 중...")
        # 첫 번째 창이 사라지고, 두 번째 'Path of Exile 2' 창을 찾을 때까지 대기
        for _ in range(10):  # 최대 10번 반복하여 창을 확인
            windows = gw.getWindowsWithTitle("Path of Exile 2")  # 제목에 특정 문자열이 포함된 창만 가져옴
            if windows:  # 창이 존재하면
                game_window = windows[0]  # 첫 번째 창 선택
                break
            time.sleep(1)  # 1초 간격으로 다시 시도

        game_window.activate()  # 게임 창 활성화

    except Exception as e:
        print(f"게임 창을 찾는 데 실패했습니다: {e}")

# 4. 프로그램 종료 시 임시 디렉토리 정리
def cleanup_temp_directory():
    if hasattr(sys, '_MEIPASS'):
        try:
            temp_dir = sys._MEIPASS
            print(f"임시 디렉토리 삭제: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"임시 디렉토리 삭제 실패: {e}")

# atexit 모듈로 종료 시점에 임시 디렉토리 삭제 설정
atexit.register(cleanup_temp_directory)

# 실행 순서
def main():
    launch_game()

if __name__ == "__main__":
    main()
