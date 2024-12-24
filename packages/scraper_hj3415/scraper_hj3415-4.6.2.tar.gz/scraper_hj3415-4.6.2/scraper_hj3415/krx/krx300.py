import os
import time
import shutil
from typing import Optional, List
import pandas as pd
import sqlite3

import requests
from datetime import datetime, timedelta
from scraper_hj3415.nfscraper import run as nfs_run

import logging
from utils_hj3415 import helpers
scraper_logger = helpers.setup_logger('scraper_logger', logging.WARNING)

sqlite_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'krx.db')
table_name = 'krx300'

def find_valid_url() -> str:
    delta=0
    while True:
        date = datetime.now() - timedelta(days=delta)
        date_str = date.strftime('%Y%m%d')
        url = f'https://www.samsungfund.com/excel_pdf.do?fId=2ETFA4&gijunYMD={date_str}'
        response = requests.get(url)
        time.sleep(3)
        if response.headers.get('Content-Length','0') != '0':
            print('삼성자산운용 krx300 엑셀다운 url : ', url)
            return url
        else:
            scraper_logger.warning(f'https://www.samsungfund.com/excel_pdf.do?fId=2ETFA4&gijunYMD={date_str} - 엑셀파일 다운에러')
            delta += 1

def download_exel() -> Optional[str]:
    TEMP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp')

    # 임시폴더 정리
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    print(f"임시폴더 초기화 완료: {TEMP_DIR}")

    url = find_valid_url()
    response = requests.get(url)

    SAVE_PATH = os.path.join(TEMP_DIR, f'{url[-8:]}.xls')

    # 정상 응답인지 확인
    if response.status_code == 200:
        # 바이너리 모드('wb')로 파일 쓰기
        with open(SAVE_PATH, 'wb') as f:
            f.write(response.content)
        print(f"파일 다운로드 완료: {SAVE_PATH}")
        return SAVE_PATH
    else:
        print(f"다운로드 실패: 상태코드 {response.status_code}")
        return None

def make_db(excel_path: str):
    # 1. 엑셀 파일 읽기
    try:
        df = pd.read_excel(excel_path, usecols='B:I', skiprows=3)  # 첫 번째 시트를 읽음
    except Exception as e:
        print(f"엑셀 파일 읽기 실패: {e}")
        return

    # 2. SQLite 데이터베이스 연결
    try:
        conn = sqlite3.connect(sqlite_path)  # 데이터베이스 파일 생성/연결
        print(f"SQLite 데이터베이스 생성/연결 성공: {sqlite_path}")
    except Exception as e:
        print(f"SQLite 연결 실패: {e}")
        return

    # 3. 데이터베이스 테이블로 데이터 삽입
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)  # 데이터 삽입
        print(f"데이터가 테이블 '{table_name}'에 성공적으로 삽입되었습니다.")
    except Exception as e:
        print(f"데이터 삽입 실패: {e}")
    finally:
        conn.close()  # 연결 종료
        print("SQLite 연결 종료.")

def get_codes() -> list:
    if not os.path.exists(sqlite_path):
        scraper_logger.warning(f"{sqlite_path} 파일이 존재하지 않아 새로 생성합니다.")
        excel_path = download_exel()
        make_db(excel_path)
    with sqlite3.connect(sqlite_path) as conn:
        # 종목코드를 가져오는 쿼리
        query = f"SELECT 종목코드 FROM {table_name} WHERE 종목코드 LIKE '______'"
        codes = pd.read_sql(query, conn)['종목코드'].tolist()
    return codes

def get_code_names() -> List[list]:
    if not os.path.exists(sqlite_path):
        scraper_logger.warning(f"{sqlite_path} 파일이 존재하지 않아 새로 생성합니다.")
        excel_path = download_exel()
        make_db(excel_path)
    with sqlite3.connect(sqlite_path) as conn:
        # 종목코드와 종목명을 가져오는 쿼리
        query = f"SELECT 종목코드, 종목명 FROM {table_name} WHERE 종목코드 LIKE '______'"
        code_names = pd.read_sql(query, conn).values.tolist()
    return code_names

# 종목명으로 종목코드를 찾는 함수
def get_name(code: str):
    for code_sql, name_sql in get_code_names():
        if code == code_sql:
            return name_sql
    return None  # 종목명을 찾지 못한 경우 None 반환

def sync_with_mongo():
    # krx300 sqlite3 리프레시
    make_db(download_exel())

    from db_hj3415 import mymongo
    in_mongo_codes = mymongo.Corps.list_all_codes()
    in_sqlite_codes = get_codes()
    scraper_logger.info(f"In mongodb: {len(in_mongo_codes)} - {in_mongo_codes}")
    scraper_logger.info(f"In sqlite3: {len(in_sqlite_codes)} - {in_sqlite_codes}")

    del_difference = list(set(in_mongo_codes) - set(in_sqlite_codes))
    add_difference = list(set(in_sqlite_codes) - set( in_mongo_codes))

    if len(add_difference) == 0 and len(del_difference) == 0:
        print(f"mongodb와 krx300의 sync는 일치합니다.(총 {len(in_mongo_codes)} 종목)")
    else:
        print(f"mongodb에서 삭제될 코드: {len(del_difference)} - {del_difference}")
        print(f"mongodb에 추가될 코드: {len(add_difference)} - {add_difference}")

        # 몽고디비에서 불필요한 종목 삭제하고 서버에 기록.
        for code in del_difference:
            mymongo.Logs.save('mongo', 'INFO', f'{code}/{mymongo.Corps.get_name(code)}를 삭제')
            mymongo.Corps.drop_code(code)

        # 몽고디비에 새로운 종목 추가하고 서버에 기록.
        if len(add_difference) != 0:
            nfs_run.all_spider(*add_difference)
            for code in add_difference:
                mymongo.Logs.save('mongo', 'INFO', f'{code}/{get_name(code)}을 추가')
