import os
from scrapy.crawler import CrawlerProcess
from scraper_hj3415.miscraper.mis.spiders.mi import MiSpider
from scraper_hj3415.miscraper.mis.spiders.mihistory import MIHistory
from webdriver_hj3415 import drivers
from decouple import Config, RepositoryEnv

# 환경변수를 이용해서 브라우저 결정
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
config = Config(RepositoryEnv(env_path))

headless = config('HEADLESS', cast=bool)
driver_version = config('DRIVER_VERSION', default=None)
browser = config('BROWSER', default='chrome')

# 세팅파일을 프로젝트의 settings.py를 사용하지 않고 직접 만들어서 사용하는 방법.
# 대신 nfs 모듈을 찾을수 있도록 sys에 경로를 추가해 줘야 한다.
import sys
# Scrapy 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

settings = {
'BOT_NAME': "mis",

'SPIDER_MODULES': ["mis.spiders"],
'NEWSPIDER_MODULE': "mis.spiders",

'ROBOTSTXT_OBEY': False,
'ITEM_PIPELINES': {
    "mis.pipelines.ValidationPipeline": 300,
    "mis.pipelines.RedisPipeline": 400,
    "mis.pipelines.MongoPipeline": 500,
},
'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
'FEED_EXPORT_ENCODING': "utf-8",

'LOG_ENABLED': True,
'LOG_LEVEL' : 'WARNING',
}


def mi():
    # Scrapy 설정 가져오기
    # settings = get_project_settings()
    # CrawlerProcess 인스턴스 생성
    process = CrawlerProcess(settings)
    # 스파이더 추가 및 실행
    process.crawl(MiSpider)
    process.start()  # 블로킹 호출, 스파이더가 완료될 때까지 기다림


def mihistory(years: int):
    webdriver = drivers.get(browser=browser, driver_version=driver_version, headless=headless)

    # Scrapy 설정 가져오기
    # settings = get_project_settings()
    # CrawlerProcess 인스턴스 생성
    process = CrawlerProcess(settings)
    # 스파이더 추가 및 실행
    process.crawl(MIHistory, webdriver=webdriver, years=years)
    process.start()  # 블로킹 호출, 스파이더가 완료될 때까지 기다림

    print('Retrieve webdriver...')
    webdriver.quit()



