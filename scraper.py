import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    # 使用你提供的特定新聞網址進行精確抓取
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 1. 嘗試多種可能的標題位置
        title_tag = soup.find('div', class_='news_title') or soup.find('h1') or soup.find('div', id='title')
        title = title_tag.get_text(strip=True) if title_tag else "交通事務局最新消息"

        # 2. 擷取日期 (從頁面中尋找 DD-MM-YYYY 格式)
        publish_date = "28-04-2026" # 預設值
        date_search = soup.find(text=re.compile(r'\d{2}-\d{2}-\d{4}'))
        if date_search:
            date_match = re.search(r'\d{2}-\d{2}-\d{4}', date_search)
            if date_match:
                publish_date = date_match.group()

        # 3. 核心：地毯式擷取所有正文文字
        # DSAT 詳情頁的主要內容通常在名為 news_content 或 td_content 的容器中
        content_container = soup.find('div', class_='news_content') or \
                            soup.find('div', id='news_content') or \
                            soup.find('div', class_='content_detail')

        if content_container:
            # 刪除不必要的腳本或按鈕標籤，避免雜訊
            for extra in content_container(["script", "style", "button"]):
                extra.decompose()
            
            # get_text(separator=' ') 確保不同段落間有空格，不會黏在一起
            full_content = content_container.get_text(separator=' ', strip=True)
            # 清理連續多餘空格
            full_content = re.sub(r'\s+', ' ', full_content)
        else:
            # 如果還是找不到容器，嘗試抓取所有 <p> 標籤
            paragraphs = soup.find_all('p')
            if paragraphs:
                full_content = " ".join([p.get_text(strip=True) for p in paragraphs])
            else:
                raise ValueError("無法定位新聞正文內容容器")

        # 4. 存儲數據
        output_data = {
            "title": title,
            "date": publish_date,
            "fullText": full_content
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功擷取新聞全文：{title}")

    except Exception as e:
        print(f"自動抓取失敗: {str(e)}")
        # 發生錯誤時生成一個備用的 data.json，防止前端崩潰
        fallback = {
            "title": "新聞加載失敗",
            "date": "00-00-0000",
            "fullText": "系統目前無法從目標網頁獲取數據，請檢查網絡連接或目標網址是否有效。"
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(fallback, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    auto_scrape_dsat()
