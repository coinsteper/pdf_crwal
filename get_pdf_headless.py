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

# 공통 설정: Headless 옵션
def get_headless_driver():
    options = Options()
    options.add_argument("--headless")  # 백그라운드 실행
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def search_dbpia(query, num_results=20):
    driver = get_headless_driver()
    url = "https://www.dbpia.co.kr/"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
        search_box.clear()
        search_box.send_keys(query)

        search_button = driver.find_element(By.ID, "submitSearchInput")
        search_button.click()

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        results = soup.select("article.thesisWrap")
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            title_tag = result.select_one("h2.thesis__tit")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            link_tag = title_tag.find_parent("a") if title_tag else None
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "#"
            full_link = f"https://www.dbpia.co.kr{link}" if link.startswith("/") else link
            date_tag = result.select_one("section.thesisAdditionalInfo span.thesis__item")
            date = date_tag.get_text(strip=True) if date_tag else "날짜 없음"

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
    driver = get_headless_driver()
    url = "https://scienceon.kisti.re.kr/main/mainForm.do"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        search_condition = wait.until(EC.element_to_be_clickable((By.ID, "searchCondition")))
        search_condition.click()
        search_condition.find_element(By.XPATH, ".//option[@value='thesis']").click()

        search_box = wait.until(EC.presence_of_element_located((By.ID, "totSearchKeyword")))
        search_box.clear()
        search_box.send_keys(query)

        search_button = driver.find_element(By.CSS_SELECTOR, "button.tsb-btn")
        search_button.click()

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("div.powerful-con")
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            title_tag = result.select_one("a.subject")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            onclick_data = title_tag.get("onclick", "")
            match = re.search(r"fncArticleDetail\('(\w+)'\)", onclick_data)
            article_id = match.group(1) if match else None
            full_link = f"https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn={article_id}" if article_id else "링크 없음"

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
    driver = get_headless_driver()
    url = "https://koreascience.kr/main.page"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='keywords']")))
        driver.execute_script("document.querySelector(\"input[name='keywords']\").value = arguments[0];", query)

        search_button = driver.find_element(By.CSS_SELECTOR, "button.hd-srch")
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        time.sleep(1)
        driver.execute_script("document.querySelector(\"button.hd-srch\").click();")

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("article.srched-box")
        print(f"\n'{query}' 검색 결과:")
        count = 0
        for result in results:
            title_tag = result.select_one("span.articleTitle.artileTitleEng")
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
            link_tag = result.select_one("a.articleLink")
            full_link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "링크 없음"
            year_tag = result.select_one("li.pubYear")
            pub_year = year_tag.get_text(strip=True) if year_tag else "연도 없음"

            count += 1
            print(f"{count}. {title}")
            print(f"   Link: {full_link}")
            print(f"   Published Year: {pub_year}\n")
            if count >= num_results:
                break

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()


def search_kci(query, num_results=20):
    driver = get_headless_driver()
    url = "https://www.kci.go.kr/kciportal/po/search/poArtiSear.kci"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "poSearchBean.keywordList")))
        driver.execute_script("arguments[0].value = arguments[1];", search_input, query)

        search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btns.h50px.blueBtn.round5px")))
        driver.execute_script("arguments[0].click();", search_button)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.subject")))
        articles = driver.find_elements(By.CSS_SELECTOR, "a.subject")

        print(f"\n'{query}' 검색 결과:")
        for i, article in enumerate(articles[:num_results], start=1):
            title = article.text
            link = article.get_attribute('href')
            print(f"{i}. {title}")
            print(f"   Link: {link}\n")

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
