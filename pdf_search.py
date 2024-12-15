import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def search_scienceon(query, num_results=20):
    # Selenium 드라이버 설정
    driver = webdriver.Chrome()
    url = "https://scienceon.kisti.re.kr/main/mainForm.do"
    driver.get(url)

    try:
        # 검색창이 로딩될 때까지 기다림
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "totSearchKeyword")))

        # 검색어 입력
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # 검색 결과 로딩 대기

        # 페이지 소스를 가져와 BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 검색 결과 항목 가져오기
        results = soup.select("a.subject")

        print(f"\n'{query}' 검색 결과:")
        if not results:
            print("검색 결과가 없습니다.")
            return

        for i, result in enumerate(results[:num_results]):
            # 제목 추출
            title = result.get_text(strip=True)

            # onclick 속성에서 ID 추출
            onclick_attr = result.get("onclick", "")
            match = re.search(r"fncArticleDetail\('([\w\d]+)'\)", onclick_attr)
            article_id = match.group(1) if match else "ID_NOT_FOUND"

            # 링크 재구성
            detail_link = f"https://scienceon.kisti.re.kr/srch/selectPORSrchDetail.do?cn={article_id}"

            # 결과 출력
            print(f"{i+1}. {title}")
            print(f"   Link: {detail_link}\n")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = input("검색어를 입력하세요: ")
    search_scienceon(search_query)
