# scrape the web content of a url
# using playwright async mode
import asyncio
import json
import logging
import os
import random
import re
from typing import Any, Callable, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


def text_parser(html_text: str) -> Dict[str, str]:
    soup = BeautifulSoup(html_text, "html.parser")
    title = soup.title.string
    # 移除不需要的元素
    for script in soup(["script", "style", "nav", "header", "footer", "iframe", "aside", "form"]):
        script.decompose()

    # 尝试找到主要内容区域
    content_selectors = [
        "main",  # 主要内容标签
        "article",  # 文章内容
        ".content",  # 常见的内容类名
        "#content",
        ".main-content",
        ".article-content",
        ".post-content",
    ]

    for selector in content_selectors:
        content = soup.select_one(selector)
        if content is not None:
            soup = content
            break
    text = soup.get_text(separator=" ", strip=True)
    text = text[:8192]
    return {"title": title, "text": text}


# urls格式[{"url":url,"xhr_patter":pattern,"scroll_times":n}]
async def read_urls(
    urls: List[Dict[str, Any]],
    parser: Callable[[str], Any] = text_parser,
    headless=True,
    timeout: int = 1500,
    save_cookies: bool = True,
    **kwargs,
) -> Dict[str, Any]:  # url, result
    logger.info(f"Reading URLs in parallel: {urls},parser:{parser}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless,
            channel="chrome",
        )

        async def process_single_url(urlreq: Dict[str, Any]) -> dict:
            matched_calls = []
            xhr_pattern = urlreq.get("xhr_pattern", "")

            async def handle_response(response):
                if (
                    xhr_pattern
                    and re.search(xhr_pattern, response.url)
                    and response.request.resource_type in ["xhr", "fetch"]
                ):
                    if not response.ok:
                        logger.error(f"Matched XHR request Failed:{response.url}: {response.status}")
                    else:
                        logger.info(f"Matched XHR request successfully: {response.url}")
                        matched_calls.append(response)
                return response

            url = urlreq["url"]
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )
            # add cookie, get domain from url,use as cookie file
            domain = urlparse(url).netloc
            cookie_path = "cookies"
            if not os.path.exists(cookie_path):
                os.makedirs(cookie_path, exist_ok=True)
            cookie_file = f"cookies/{domain}.json"
            try:
                with open(cookie_file, "r") as f:
                    cookies = json.load(f)
                    await context.add_cookies(cookies)
            except Exception as e:
                logger.debug(f"Error reading cookie file {cookie_file}: {str(e)}")

            page = await context.new_page()
            page.on("response", handle_response)
            try:
                page.set_default_timeout(timeout)
                try:
                    await page.goto(url)
                except Exception as e:
                    logger.debug(f"Navigation timeout for {url}: {str(e)}")
                await page.wait_for_timeout(timeout)
                # get full content
                scroll_times: int = urlreq.get("scroll_times", 0)
                for _ in range(scroll_times):
                    scroll_ratio = random.uniform(0.75, 0.95)
                    scroll_js = f"""
                        const targetScroll = window.pageYOffset + (window.innerHeight * {scroll_ratio});
                        window.scrollTo(0, targetScroll);
                    """
                    await page.evaluate(scroll_js)
                    await page.wait_for_timeout(1000)

                result = ""
                if xhr_pattern:
                    if xhr_pattern and matched_calls:
                        content = await matched_calls[-1].json()
                        result = json.dumps(content)
                    else:
                        raise Exception("no matched XHR request found")
                else:
                    html_content = await page.content()
                    result = parser(html_content)
                # save cookie
                if save_cookies:
                    cookies = await context.cookies()
                    with open(cookie_file, "w") as f:
                        json.dump(cookies, f)
                        # logging
                        logger.debug(f"Saved cookies for {domain} to {cookie_file}")
                return {"result": result, "url": url}
            except Exception as e:
                logger.error(f"Error reading URL {url}: {str(e)}")
                return {"result": {"text": "", "title": ""}, "url": url}
            finally:
                await context.close()

        try:
            results = await asyncio.gather(*[process_single_url(urlreq) for urlreq in urls])
            result_dict = {result["url"]: result["result"] for result in results}
            return result_dict
        finally:
            await browser.close()
