import sys
import os
import time
import zipfile
import glob
from selenium.webdriver.common.keys import Keys

from logger import setup_custom_logger
from chromedriver import generate_chrome
from xlsxhandler import get_dir_update_info

logger = setup_custom_logger('main.py')
logger.debug('Run crawler!!!!')
PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/download'

driver_path = f'{PROJECT_DIR}/lib/webDriver/'
platform = sys.platform
if platform == 'darwin':
    logger.debug('System platform : Darwin')
    driver_path += 'chromedriverMac'
elif platform == 'linux':
    logger.debug('System platform : Linux')
    driver_path += 'chromedriverLinux'
elif platform == 'win32':
    logger.debug('System platform : Window')
    driver_path += 'chromedriverWindow'
else:
    logger.error(f'[{sys.platform}] not supported. Check your system platform.')
    raise Exception()

# 크롬 드라이버 인스턴스 생성    
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)

# 페이지 요청
url = 'https://github.com/login'
chrome.get(url)
time.sleep(3)

# 깃허브 로그인
login_page = chrome.page_source

elm = chrome.find_element_by_id('login_field')
elm.send_keys('깃허브 아이디')
elm = chrome.find_element_by_id('password')
elm.send_keys('깃허브 비밀번호')
elm.send_keys(Keys.RETURN)

time.sleep(5)

# 페이지 이동
url = 'https://github.com/dc7303/pycrawler-exam-dummy-data'
chrome.get(url)
time.sleep(5)

# 다운로드 토글 오픈
elm = chrome.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/div[3]/details[2]/summary')
elm.click()

# 다운로드 버튼
elm = chrome.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div/div[3]/details[2]/div/div/div[1]/div[3]/a[2]')
elm.click()
time.sleep(5)

# ZIP 파일 존재여부 확인 후 압축 풀기
repo_name = 'pycrawler-exam-dummy-data-master'
zip_file_path = f'{DOWNLOAD_DIR}/{repo_name}.zip'
if os.path.isfile(zip_file_path):
    z = zipfile.ZipFile(zip_file_path)
    z.extractall(DOWNLOAD_DIR)
    z.close()
    os.remove(zip_file_path)

# 압축 해제한 파일 디렉토리 경로 선언
before_dir_path = f'{DOWNLOAD_DIR}/{repo_name}/before'
after_dir_path = f'{DOWNLOAD_DIR}/{repo_name}/after'

# 파일 경로 리스트 조회
before_xlsx_list = [f for f in glob.glob(f'{before_dir_path}/*.xlsx')]
after_xlsx_list = [f for f in glob.glob(f'{after_dir_path}/*.xlsx')]

# 파일 삭제, 추가 정보 비교 분석
deleted_file_list, new_file_list = get_dir_update_info(before_xlsx_list, after_xlsx_list)

# 파일 비교 분석 후 가져오기
