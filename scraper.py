import requests
from bs4 import BeautifulSoup
import json
import re

def auto_scrape_dsat():
    # 請替換為你實際要抓取的 DSAT 詳細頁網址
    target_url = "https://www.dsat.gov.mo/dsat/news_detail.aspx?a_id=6411412D3DE9A671E1D150550511DAD9"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 1. 定位主容器 class="my_content"
        main_container = soup.find(class_='my_content')
        
        if not main_container:
            # 容錯機制：如果網頁結構變動，嘗試之前的標籤
            main_container = soup.find(class_='news_content') or soup.find(id='news_content')

        if main_container:
            # 2. 提取標題 class="content_title"
            # 使用 find 尋找容器內的標題
            title_tag = main_container.find(class_='content_title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # 為了避免標題重複出現在正文中，我們可以將其從容器中暫時「挖掉」
                title_tag.decompose() 
            else:
                title = "交通事務局最新消息"

            # 3. 提取日期 (尋找特定的日期模式)
            date_match = re.search(r'\d{2}-\d{2}-\d{4}', main_container.get_text())
            publish_date = date_match.group() if date_match else "29-04-2026"

            # 4. 擷取其餘所有文字內容 (一字不漏)
            # 因為標題已經 decompose 了，這裡 get_text 拿到的就是剩下的所有內容
            full_content = main_container.get_text(separator=' ', strip=True)
            # 清理多餘空格
            full_content = re.sub(r'\s+', ' ', full_content)
        else:
            raise ValueError("找不到 class='my_content' 容器")

        # 5. 存儲數據
        output_data = {
            "title": title,
            "date": publish_date,
            "fullText": full_content
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功擷取！標題：{title}")

    except Exception as e:
        print(f"抓取失敗: {str(e)}")

if __name__ == "__main__":
    auto_scrape_dsat()
