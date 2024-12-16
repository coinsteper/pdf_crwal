from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def search_dbpia(query, num_results=20):
    # Selenium WebDriver 설정
    driver = webdriver.Chrome()
    url = "https://www.dbpia.co.kr/"
    driver.get(url)

    try:
        # 검색창이 로딩될 때까지 대기
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))

        # 검색어 입력
        search_box.clear()
        search_box.send_keys(query)

        # 검색 버튼 클릭
        search_button = driver.find_element(By.ID, "submitSearchInput")
        search_button.click()
        
        # 검색 결과 로딩 대기
        time.sleep(3)

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 검색 결과 가져오기 (제목, 링크, 날짜 추출)
        results = soup.select("article.thesisWrap")  # 각 논문 요소 선택
        
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            # 제목 가져오기
            title_tag = result.select_one("h2.thesis__tit")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            
            # 링크 가져오기
            link_tag = title_tag.find_parent("a") if title_tag else None
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "#"
            full_link = f"https://www.dbpia.co.kr{link}" if link.startswith("/") else link
            
            # 날짜 가져오기
            date_tag = result.select_one("section.thesisAdditionalInfo span.thesis__item")
            date = date_tag.get_text(strip=True) if date_tag else "날짜 없음"

            # 출력
            count += 1
            print(f"{count}. {title}")
            print(f"   게시 날짜: {date}")
            print(f"   Link: {full_link}\n")
            
            if count >= num_results:
                break

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()


def search_scienceon(query, num_results=20):
    driver = webdriver.Chrome()
    url = "https://scienceon.kisti.re.kr/main/mainForm.do"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        
        # 검색 조건 "논문" 선택
        search_condition = wait.until(EC.element_to_be_clickable((By.ID, "searchCondition")))
        search_condition.click()
        search_condition.find_element(By.XPATH, ".//option[@value='thesis']").click()
        
        # 검색창에 검색어 입력
        search_box = wait.until(EC.presence_of_element_located((By.ID, "totSearchKeyword")))
        search_box.clear()
        search_box.send_keys(query)
        
        # 검색 버튼 클릭
        search_button = driver.find_element(By.CSS_SELECTOR, "button.tsb-btn")
        search_button.click()
        
        # 검색 결과 대기
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("div.powerful-con")  # 검색 결과 항목
        
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            # 제목 가져오기
            title_tag = result.select_one("a.subject")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            
            # 논문 ID 추출 (onclick 속성)
            onclick_data = title_tag.get("onclick", "")
            match = re.search(r"fncArticleDetail\('(\w+)'\)", onclick_data)
            article_id = match.group(1) if match else None
            
            # 실제 링크 재구성
            full_link = f"https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn={article_id}" if article_id else "링크 없음"
            
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


def search_koreascience(query, num_results=20):
    driver = webdriver.Chrome()
    url = "https://koreascience.kr/main.page"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        
        # 검색창에 검색어 입력
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='keywords']")))
        driver.execute_script("document.querySelector(\"input[name='keywords']\").value = arguments[0];", query)
        
        # 검색 버튼이 화면에 보이도록 스크롤 후 클릭
        search_button = driver.find_element(By.CSS_SELECTOR, "button.hd-srch")
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        time.sleep(1)
        driver.execute_script("document.querySelector(\"button.hd-srch\").click();")
        
        # 검색 결과 대기
        time.sleep(3)
        
        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("article.srched-box")  # 검색 결과 항목
        
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            # 제목 가져오기
            title_tag = result.select_one("span.articleTitle.artileTitleEng")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            
            # 링크 가져오기
            link_tag = result.select_one("a.articleLink")
            full_link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "링크 없음"
            
            # DOI 링크 가져오기
            doi_tag = result.select_one("a.doiLink")
            doi_link = doi_tag['href'] if doi_tag and 'href' in doi_tag.attrs else "DOI 없음"
            
            # PDF 링크 가져오기
            pdf_tag = result.select_one("a.pdfLink")
            pdf_link = pdf_tag['href'] if pdf_tag and 'href' in pdf_tag.attrs else "PDF 없음"
            
            # 연도 가져오기
            year_tag = result.select_one("li.pubYear")
            pub_year = year_tag.get_text(strip=True) if year_tag else "연도 없음"

            # 출력
            count += 1
            print(f"{count}. {title}")
            print(f"   Link: {full_link}")
            print(f"   DOI: {doi_link}")
            print(f"   PDF: {pdf_link}")
            print(f"   Published Year: {pub_year}\n")
            
            if count >= num_results:
                break

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()


def search_kci(query, num_results=20):
    # ChromeDriver 설정
    options = Options()
    options.add_argument("--headless")  # 필요시 헤드리스 모드 활성화
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # KCI 논문 검색 페이지로 이동
        url = "https://www.kci.go.kr/kciportal/po/search/poArtiSear.kci"
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # 검색어 입력 필드 대기
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "poSearchBean.keywordList")))

        # JavaScript로 값 입력
        driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
        driver.execute_script("arguments[0].value = arguments[1];", search_input, query)

        # 검색 버튼 클릭 (JavaScript 사용)
        search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btns.h50px.blueBtn.round5px")))
        driver.execute_script("arguments[0].click();", search_button)

        # 검색 결과 기다림
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.subject")))

        # 검색 결과 가져오기
        results = []
        articles = driver.find_elements(By.CSS_SELECTOR, "a.subject")

        for article in articles[:num_results]:
            title = article.text  # 논문 제목
            link = article.get_attribute('href')  # 논문 링크

            # 저자명 추출
            parent = article.find_element(By.XPATH, "./../..")  # article의 부모 컨테이너
            author_elements = parent.find_elements(By.CSS_SELECTOR, "ul.subject-info li a")
            authors = [author.text for author in author_elements]

            results.append({
                "title": title,
                "link": link,
                "authors": ", ".join(authors)
            })

        # 결과 출력
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Authors: {result['authors']}\n")

        return results

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = input("검색어를 입력하세요: ")
    search_dbpia(search_query)
    search_scienceon(search_query)
    search_koreascience(search_query)
    search_kci(search_query)
