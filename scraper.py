import requests
from bs4 import BeautifulSoup
import json
import re
import os

def auto_scrape_dsat():
    # DSAT 新聞列表頁面（獲取最新一條新聞的 ID）
    list_url = "https://www.dsat.gov.mo/dsat/news.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # 1. 獲取列表頁以找到最新的連結
        res = requests.get(list_url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 找到第一個新聞連結 (假設連結在特定 class 內)
        first_news_link = soup.select_one(".news_list_row a") 
        if not first_news_link:
            print("無法獲取列表，使用預設連結測試...")
            target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
        else:
            target_url = "https://www.dsat.gov.mo/dsat/" + first_news_link['href']

        # 2. 進入詳情頁抓取全文
        detail_res = requests.get(target_url, headers=headers)
        detail_res.encoding = 'utf-8'
        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')

        # 擷取標題
        title = detail_soup.find('div', class_='news_title').get_text(strip=True)
        
        # 擷取發佈日期 (從標題下的欄位)
        date_text = detail_soup.find('div', class_='news_info').get_text()
        date_match = re.search(r'\d{2}-\d{2}-\d{4}', date_text)
        publish_date = date_match.group() if date_match else "----/--/--"

        # 核心：擷取所有文字內容 (一字不漏)
        # 鎖定正文容器
        content_container = detail_soup.find('div', class_='news_content')
        
        # 提取容器內所有層級的文字內容
        if content_container:
            # 使用換行符作為分隔符保留結構感，隨後清理多餘空格
            raw_text = content_container.get_text(separator=' ', strip=True)
            # 移除連續多個空格或換行，轉為乾淨的長字串
            full_content = re.sub(r'\s+', ' ', raw_text)
        else:
            full_content = "未找到正文內容。"

        # 3. 打包輸出
        output_data = {
            "title": title,
            "date": publish_date,
            "fullText": full_content
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功更新 data.json: {title}")

    except Exception as e:
        print(f"自動抓取發生錯誤: {e}")

if __name__ == "__main__":
    auto_scrape_dsat()
