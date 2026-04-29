import requests
from bs4 import BeautifulSoup
import json
import re
import sys

def auto_scrape_dsat():
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        res = requests.get(target_url, headers=headers, timeout=20)
        res.encoding = 'utf-8'
        if res.status_code != 200: sys.exit(1)

        soup = BeautifulSoup(res.text, 'html.parser')
        container = soup.find(class_='my_content')
        if not container: sys.exit(1)

        # 擷取標題並從容器中移除
        title_tag = container.find(class_='content_title')
        title = title_tag.get_text(strip=True) if title_tag else "交通消息"
        if title_tag: title_tag.decompose()
        
        # 徹底移除圖片、腳本、連結、附件
        for noise in container.find_all(['img', 'script', 'style', 'a', 'button']):
            noise.decompose()

        # 分段擷取文字並過濾
        raw_text = container.get_text(separator='|', strip=True)
        parts = raw_text.split('|')
        
        clean_parts = []
        for p in parts:
            p = p.strip()
            # 過濾條件：排除圖片名(帶_)、排除附件與網址
            if not p or len(p) < 5: continue
            if "_" in p and any(k in p for k in ["措施", "假期", "交通"]): continue
            if any(k in p for k in ["附件：", "http", ">>>", "日期 :"]): continue
            clean_parts.append(p)

        full_content = " ".join(clean_parts)

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "date": "2026-04-29",
                "fullText": full_content
            }, f, ensure_ascii=False, indent=2)
        print("Scrape Successful")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    auto_scrape_dsat()
