import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 鎖定容器
        container = soup.find(class_='my_content')
        if not container: return

        # 1. 提取標題並徹底刪除該標籤，避免其進入 fullText
        title_tag = container.find(class_='content_title')
        title = title_tag.get_text(strip=True) if title_tag else ""
        if title_tag: title_tag.decompose()

        # 2. 徹底刪除所有非正文標籤 (圖片、連結、腳本)
        # 這能解決「文字不一樣」的問題，因為它移除了隱藏的圖片描述
        for noise in container.find_all(['img', 'script', 'style', 'a', 'button']):
            noise.decompose()

        # 3. 逐段過濾雜訊文字
        paragraphs = container.find_all(['p', 'div', 'span'])
        clean_list = []
        
        # 雜訊關鍵字黑名單
        blacklist = ["措施_", "協調會議", "附件：", "日期 :", ">>>", ".jpg", ".png"]

        for p in paragraphs:
            txt = p.get_text(strip=True)
            # 過濾掉太短的片段、黑名單文字、或純網址
            if not txt or any(item in txt for item in blacklist) or "http" in txt:
                continue
            if txt not in clean_list: # 避免重複抓取
                clean_list.append(txt)

        # 4. 重新組合成乾淨的長字串
        full_text = " ".join(clean_list)
        # 強制清理多餘空格
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        # 5. 輸出
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "date": "28-04-2026",
                "fullText": full_text
            }, f, ensure_ascii=False, indent=2)

        print("數據同步成功，雜訊已移除。")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    auto_scrape_dsat()
