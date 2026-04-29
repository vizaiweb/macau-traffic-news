import requests
from bs4 import BeautifulSoup
import json
import re
import sys

def auto_scrape_dsat():
    # DSAT 詳細頁連結
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        res = requests.get(target_url, headers=headers, timeout=20)
        res.encoding = 'utf-8'
        if res.status_code != 200:
            print(f"網頁連線失敗，狀態碼: {res.status_code}")
            sys.exit(1)

        soup = BeautifulSoup(res.text, 'html.parser')

        # 鎖定主容器
        container = soup.find(class_='my_content')
        if not container:
            print("錯誤：找不到 class='my_content' 的容器。")
            sys.exit(1)

        # 提取標題
        title_tag = container.find(class_='content_title')
        title = title_tag.get_text(strip=True) if title_tag else "交通消息"
        
        # 移除不需要的標籤 (圖片、連結、腳本)
        if title_tag: title_tag.decompose()
        for noise in container.find_all(['img', 'script', 'style', 'a', 'button']):
            noise.decompose()

        # 獲取內容並過濾圖片描述文字
        raw_text = container.get_text(separator='|', strip=True)
        parts = raw_text.split('|')
        
        clean_parts = []
        # 關鍵過濾邏輯：排除包含底線的圖片名、附件及網址
        for p in parts:
            p = p.strip()
            if not p or len(p) < 5: continue
            # 排除帶有底線的圖片描述文字 (如: 措施_官也街)
            if "_" in p and any(k in p for k in ["措施", "假期", "交通"]): continue
            if any(k in p for k in ["附件：", "http", ">>>", "日期 :"]): continue
            
            clean_parts.append(p)

        full_content = " ".join(clean_parts)

        # 寫入 JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "date": "2026-04-29",
                "fullText": full_content
            }, f, ensure_ascii=False, indent=2)
            
        print(f"成功更新 JSON。標題: {title}")

    except Exception as e:
        print(f"執行發生異常錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    auto_scrape_dsat()
