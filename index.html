import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    # 這是你提供的新聞連結
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 擷取標題
        title_tag = soup.select_one(".news_title") or soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "DSAT 交通新聞"

        # 擷取日期 (從文字內容中尋找日期格式)
        publish_date = "28-04-2026"
        date_area = soup.select_one(".news_info") or soup
        date_match = re.search(r'\d{2}-\d{2}-\d{4}', date_area.get_text())
        if date_match:
            publish_date = date_match.group()

        # 核心：地毯式擷取新聞內文的所有文字 (一字不漏)
        # 鎖定 DSAT 專用的內容容器
        content_container = soup.select_one(".news_content") or soup.select_one("#news_content")

        if content_container:
            # 獲取所有段落、編號文字內容
            # separator=' ' 確保文字間有間隔，strip=True 移除頭尾空白
            raw_text = content_container.get_text(separator=' ', strip=True)
            # 將多個空白或換行符號整合成一個空格，確保文字流完整
            full_content = re.sub(r'\s+', ' ', raw_text)
        else:
            # 備案：如果抓不到容器，就抓取所有 p 標籤內容
            full_content = " ".join([p.get_text(strip=True) for p in soup.find_all('p')])

        # 寫入 JSON
        output_data = {
            "title": title,
            "date": publish_date,
            "fullText": full_content
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功擷取全文: {title}")

    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    auto_scrape_dsat()
