# 文件名：baidu_news_api.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    keyword = request.json.get('keyword')
    max_results = request.json.get('max_results', 5)

    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded_keyword}&tn=news"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    results = []
    for item in soup.select(".result")[:max_results]:
        title = item.select_one("h3").text if item.select_one("h3") else "无标题"
        link = item.select_one("a")["href"] if item.select_one("a") else ""
        summary = item.select_one(".c-span18") or item.select_one(".c-span-last")
        summary_text = summary.text.strip() if summary else ""
        results.append({
            "title": title,
            "link": link,
            "summary": summary_text
        })

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(port=8000)
