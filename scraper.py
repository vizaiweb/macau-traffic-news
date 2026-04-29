import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    # DSAT 新聞詳細頁網址
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 1. 定位主容器
        main_container = soup.find(class_='my_content')
        if not main_container:
            print("找不到指定容器，嘗試備用標籤...")
            main_container = soup.find(class_='news_content')

        if main_container:
            # 2. 提取並移除標題 (避免標題重複出現在正文)
            title_tag = main_container.find(class_='content_title')
            title = title_tag.get_text(strip=True) if title_tag else "交通事務局最新消息"
            if title_tag:
                title_tag.decompose()

            # 3. 提取日期
            date_match = re.search(r'\d{2}-\d{2}-\d{4}', main_container.get_text())
            publish_date = date_match.group() if date_match else "28-04-2026"

            # 4. 【深度清洗】移除圖片說明、連結、腳本
            # 移除所有圖片、超連結、腳本和樣式標籤
            for noise in main_container.find_all(['script', 'style', 'img', 'a', 'button']):
                noise.decompose()

            # 5. 擷取純文字並進行最後整理
            raw_text = main_container.get_text(separator=' ', strip=True)
            
            # 移除網址、日期前綴及結尾符號
            clean_text = re.sub(r'https?://\S+', '', raw_text) # 移除連結
            clean_text = re.sub(r'日期\s*:\s*\d{2}-\d{2}-\d{4}', '', clean_text) # 移除重複日期
            clean_text = clean_text.replace('>>>', '').strip()
            
            # 將多個空格合併為一個
            full_content = re.sub(r'\s+', ' ', clean_content)
        else:
            full_content = "無法解析新聞內容。"

        # 6. 打包
        output_data = {
            "title": title,
            "date": publish_date,
            "fullText": full_content
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功更新 JSON！標題：{title}")

    except Exception as e:
        print(f"抓取發生錯誤: {e}")

if __name__ == "__main__":
    auto_scrape_dsat()
