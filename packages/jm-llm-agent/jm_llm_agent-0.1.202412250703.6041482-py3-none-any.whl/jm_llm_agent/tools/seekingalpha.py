import json
import logging
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from jm_llm_agent.tools.web import read_urls

logger = logging.getLogger(__name__)


def select_one(soup: BeautifulSoup, pattern: str) -> str:
    element = soup.select_one(pattern)
    return element.get_text(separator="\n", strip=True) if element else ""


def select(soup: BeautifulSoup, pattern: str) -> list[str]:
    return [div.get_text(separator="\n", strip=True) for div in soup.select(pattern)]


def convert_time(time: str) -> str:
    if not time:
        return ""
    time_str = time
    clean_str = time_str.replace(" ET", "")
    naive_date = datetime.strptime(clean_str, "%b. %d, %Y %I:%M %p")
    aware_date = naive_date.astimezone(ZoneInfo("America/New_York"))
    return aware_date.isoformat()


def parse_sk(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    title = select_one(soup, "h1")
    content = "\n".join(select(soup, "div[data-test-id='content-container']"))
    comments = select(soup, "div[data-test-id='comment-content']")

    # metas
    time = select_one(soup, "span[data-test-id='post-date']")
    time = convert_time(time)
    ticker = select_one(soup, "a[data-test-id='key-stats-ticker-link']")

    return {
        "title": title,
        "time": time,
        "ticker": ticker,
        "content": content,
        "comments": comments,
    }


def parse_sk_json(json_str: str):
    # logger.info(f"parse_sk_json json_str: {json_str}")
    base_url = "https://seekingalpha.com"
    try:
        articles_obj = json.loads(json_str)
        articles = articles_obj["data"]
        return [
            {
                "title": article["attributes"]["title"],
                "url": f"{base_url}/{article['links']['self']}",
            }
            for article in articles
        ]
    except Exception as e:
        logger.error(f"parse_sk_json: {str(e)}")
        return []


async def list_articles(tick: str):
    url = f"https://seekingalpha.com/symbol/{tick}/analysis"
    results = await read_urls(
        [{"url": url, "xhr_pattern": r"analysis\?"}],
        parse_sk_json,
        headless=False,
        timeout=5000,
        save_cookies=False,
    )
    return results


async def get_articles(urls: List[str]):
    article_infos = {}
    for url in urls:
        results = await read_urls([{"url": url}], parse_sk)
        result = results[url]
        article_infos[url] = result
    return article_infos


async def sk_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )
            page = await context.new_page()
            await page.goto("https://seekingalpha.com")
            await page.wait_for_timeout(60000)  # 等待手动登录
            cookies = await context.cookies()
            cookie_file = "cookies/seekingalpha.com.json"
            with open(cookie_file, "w") as f:
                json.dump(cookies, f)
                # logging
                logger.info(f"Saved cookies for seekingalpha.com to {cookie_file}")
            await page.close()
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
        finally:
            await browser.close()
