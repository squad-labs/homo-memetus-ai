from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  
import time
import logging
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

def setup_chrome_options():
  chrome_options = Options()
  download_dir = "/Users/supersquad/Resisterboy/supersquad/meme-ai/"  # 원하는 다운로드 경로

  chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # 다운로드 경로 설정
    "download.prompt_for_download": False,       # 다운로드 대화상자 비활성화
    "download.directory_upgrade": True,          # 경로 업그레이드 활성화
    "safebrowsing.enabled": True                 # 안전 다운로드 활성화
  })

# ChromeOptions 설정
  chrome_options.add_argument('--start-maximized')
  return chrome_options

def create_driver():
  logger.info('Create ChromeDriver, Configure ChromeOptions...')
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=setup_chrome_options())
  return driver

def capture_full_page_screenshot(driver, queries):
  time.sleep(20)
  driver.save_screenshot('screenshot.png')

  for query in queries:
    element = driver.find_element(By.CSS_SELECTOR, query['element_query'])
    location = element.location  
    size = element.size  

    device_pixel_ratio = driver.execute_script("return window.devicePixelRatio;")

    x = int(location['x'] * device_pixel_ratio)
    y = int(location['y'] * device_pixel_ratio)
    width = int(size['width'] * device_pixel_ratio)
    height = int(size['height'] * device_pixel_ratio)
    image = Image.open('screenshot.png')
    cropped_image = image.crop((x, y, x + width, y + height))

    cropped_image.save(query['file_name'])

def click_element_by_xpath(driver, xpath, element_name, wait_time=10):
  time.sleep(20)
  try:
      element = WebDriverWait(driver, wait_time).until(
          EC.element_to_be_clickable((By.XPATH, xpath))
      )
      element.click()
      time.sleep(50) 
  except TimeoutException:
      logger.error(f"{element_name} 요소를 찾는 데 시간이 초과되었습니다.")
  except ElementClickInterceptedException:
      logger.error(f"{element_name} 요소를 클릭할 수 없습니다. 다른 요소에 가려져 있을 수 있습니다.")
  except Exception as e:
      logger.error(f"{element_name} 클릭 중 오류 발생: {e}")

def capture_chart_screenshot(driver):
  driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[2]/div[4]/div[1]/div/div[1]/div/iframe'))
  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/div/button[3]', "5 minutes", 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10)

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/div/button[4]', '15 minutes', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10)

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/div/button[5]', '1 Hour', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10)

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/div/button[6]', '4 Hours', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10)

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[13]/div', '8 Hours', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10)

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[14]/div', '12 Hours', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10) 

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[17]/div', '1 Day', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10) 
  

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[18]/div', '3 Days', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10) 

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[19]/div', '1 Week', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10) 

  click_element_by_xpath(driver, '//*[@id="header-toolbar-intervals"]/button', 'options', 10)
  click_element_by_xpath(driver, '//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[20]/div', '1 Month', 10)
  click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div[3]/div/div/div/div/div/div[15]/button[3]', 'Take a screenshot', 10)
  click_element_by_xpath(driver, '/html/body/div[7]/div/span/div[1]/div/div/div[2]', 'save-chart-image', 10) 

def get_token_data(token_addr: str):
  driver = None
  try:
    driver = create_driver()

    url = "https://www.geckoterminal.com/solana/pools/{token_addr}"
    driver.get(url)

    images = [{
      'element_query': ".grid.grid-cols-4.gap-2",
      'file_name': 'rise-rate.png'
    },
    {
      'element_query': ".rounded.border.border-gray-800.min-w-\[20rem\].flex-1.p-2.sm\:p-4.md\:min-w-0.md\:flex-none",
      'file_name': 'total-data.png'
    },
    {
      'element_query': ".rounded.border.border-gray-800.flex.h-full.flex-col.space-y-2.overflow-hidden.p-0.pb-2",
      'file_name': 'volumn-data.png'
    }]
    capture_full_page_screenshot(driver, images)
    capture_chart_screenshot(driver)

  except Exception as e:
    logger.error(f'Error: {e}')
  finally:
    if driver:
      driver.quit()
