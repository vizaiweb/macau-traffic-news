import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    # 這裡放你要擷取的詳細頁網址
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 鎖定大容器
        main_container = soup.find(class_='my_content')
        if not main_container: return

        # 提取標題
        title_tag = main_container.find(class_='content_title')
        title = title_tag.get_text(strip=True) if title_tag else "交通消息"
        
        # 清洗內容：移除標題標籤、圖片、網址、圖片說明
        if title_tag: title_tag.decompose()
        for noise in main_container.find_all(['img', 'script', 'style', 'a', 'button']):
            noise.decompose()

        # 獲取純文字
        raw_text = main_container.get_text(separator=' ', strip=True)
        
        # 排除圖片敍述 (例如: 2026年...措施_官也街)
        clean_text = re.sub(r'[^。；！？]*_[\u4e00-\u9fa5]+', '', raw_text)
        # 排除網址和雜訊
        clean_text = re.sub(r'https?://\S+', '', clean_text)
        clean_text = clean_text.replace('>>>', '').strip()

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "date": "2026-04-29",
                "fullText": clean_text
            }, f, ensure_ascii=False, indent=2)
        print("JSON 更新完成")

    except Exception as e:
        print(f"抓取失敗: {e}")

if __name__ == "__main__":
    auto_scrape_dsat()
