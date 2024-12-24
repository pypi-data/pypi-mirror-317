from scraper_hj3415.krx import krx300
from scraper_hj3415.miscraper import run
from utils_hj3415 import utils
import argparse
import random
from db_hj3415 import mymongo


def nfs():
    from scraper_hj3415.nfscraper import run
    spiders = {
        'c101': run.c101,
        'c106': run.c106,
        'c103y': run.c103y,
        'c103q': run.c103q,
        'c104y': run.c104y,
        'c104q': run.c104q,
        'c108': run.c108,
        'all_spider': run.all_spider
    }

    parser = argparse.ArgumentParser(description="NF Scraper Command Line Interface")
    subparsers = parser.add_subparsers(dest='spider', help='사용할 스파이더를 선택하세요.', required=True)

    # 각 스파이더에 대해 서브 파서 설정
    for spider_name, spider_func in spiders.items():
        spider_parser = subparsers.add_parser(spider_name, help=f"{spider_name} 스파이더 실행")
        spider_parser.add_argument('targets', nargs='*', type=str, help="대상 종목 코드를 입력하세요. 'all'을 입력하면 전체 종목을 대상으로 합니다.")

    # 명령줄 인자 파싱
    args = parser.parse_args()

    selected_spider = spiders.get(args.spider)
    if not selected_spider:
        print(f"The spider should be in {list(spiders.keys())}")
        return

    # 전체 종목을 대상으로 할 경우 처리
    if len(args.targets) == 1 and args.targets[0] == 'all':
        all_codes = krx300.get_codes()
        random.shuffle(all_codes)
        selected_spider(*all_codes)  # 스파이더 실행
        mymongo.Logs.save('cli','INFO', f"run >> nfs {selected_spider.__name__} all / {len(all_codes)} codes")
    else:
        # 입력된 종목 코드 유효성 검사
        invalid_codes = [code for code in args.targets if not utils.is_6digit(code)]
        if invalid_codes:
            print(f"다음 종목 코드의 형식이 잘못되었습니다: {', '.join(invalid_codes)}")
            return
        selected_spider(*args.targets)  # 스파이더 실행
        mymongo.Logs.save('cli','INFO', f"run >> nfs {selected_spider.__name__} {args.targets}")

def mis():
    parser = argparse.ArgumentParser(description="Market Index Scraper")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # 'mi' 명령어 서브파서
    parser_mi = subparsers.add_parser('mi', help='오늘의 Market Index를 저장합니다.')

    # 'mihistory' 명령어 서브파서
    parser_mihistory = subparsers.add_parser('mihistory', help='과거 Market Index를 저장합니다.')
    parser_mihistory.add_argument('--years', type=int, default=3, help='저장할 과거 데이터의 연도 수 (기본값: 3년)')

    args = parser.parse_args()

    if args.command == 'mi':
        mymongo.Logs.save('cli','INFO', 'run >> mis mi')
        run.mi()
    elif args.command == 'mihistory':
        mymongo.Logs.save('cli','INFO', f'run >> mis mihistory --years {args.years}')
        run.mihistory(args.years)

def krx():
    parser = argparse.ArgumentParser(description="Krx300 Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # 'sync' 명령어 서브파서
    parser_sync = subparsers.add_parser('sync', help='몽고db와 krx300의 싱크를 맞춥니다.')

    args = parser.parse_args()

    if args.command == 'sync':
        mymongo.Logs.save('cli','INFO', 'run >> krx sync')
        krx300.sync_with_mongo()
