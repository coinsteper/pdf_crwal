import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def search_riss(query, num_results=20):
    # Selenium WebDriver 설정
    driver = webdriver.Chrome()
    url = "https://www.riss.kr/index.do"
    driver.get(url)

    try:
        # 검색창이 로딩될 때까지 대기
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "query")))

        # 검색어 입력
        search_box.clear()
        search_box.send_keys(query)

        # 검색 버튼 클릭
        search_button = driver.find_element(By.CSS_SELECTOR, "button.btnSearch")
        search_button.click()

        # 검색 결과 로딩 대기
        time.sleep(3)

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 검색 결과에서 제목과 링크 추출
        results = soup.select("div.cont p.title a")  # 제목과 링크를 포함하는 태그 선택
        
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            title = result.get_text(strip=True)  # 제목 텍스트 추출
            link = result['href']  # 링크 추출

            # 상대 경로 처리
            full_link = f"https://www.riss.kr{link}" if link.startswith("/") else link

            # 출력
            count += 1
            print(f"{count}. {title}")
            print(f"   Link: {full_link}\n")

            if count >= num_results:
                break

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = input("검색어를 입력하세요: ")
    search_riss(search_query)
