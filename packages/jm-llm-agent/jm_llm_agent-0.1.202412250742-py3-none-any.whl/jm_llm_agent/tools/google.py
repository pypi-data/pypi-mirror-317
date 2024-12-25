import logging
import os
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from jm_llm_agent.llm.function import llm_function
from jm_llm_agent.tools.web import read_urls

logger = logging.getLogger(__name__)


def google_parser(html_content: str) -> List[Dict[str, str]]:
    logger.info(f"Parsing Google search results... len=({len(html_content)})")
    # dump html content to file

    soup = BeautifulSoup(html_content, "html.parser")
    search_results: List[Dict[str, Any]] = []
    links = soup.select("a")
    for a in links:
        h3 = a.find("h3")
        if h3 is None:
            continue
        if "href" not in a.attrs:
            continue
        if a["href"].startswith("http"):
            search_results.append({"url": a["href"], "title": h3.get_text()})
        else:
            parsed_url = urlparse(a["href"])
            query_params = parse_qs(parsed_url.query)
            if "url" in query_params and len(query_params["url"]) > 0:
                search_results.append({"url": query_params["url"][0], "title": h3.get_text()})
    return search_results


async def google(query: str, max_results: int = 10, time: str = None) -> List[Dict[str, str]]:
    url = f"https://www.google.com/search?q={query}&pws=0&gl=us&gws_rd=cr"
    if time is not None:
        url = url + f"&tbs=qdr:{time}"
    results = await read_urls([{"url": url}], google_parser)
    if url in results:
        search_results: List[Dict[str, str]] = results[url]
        if isinstance(search_results, list):  # maybe search error
            return search_results[:max_results]
    return []


@llm_function(
    name="google_and_read",
    description="Search google and read the content of the search results",
)
async def google_and_read(query: str, max_results: int = 10, time: str = None) -> str:
    """Search google and read the content of the search results.

    :param query: The query to search for
    :param max_results: The maximum number of results to return,prefer bigger than 10
    :param time: The time period to search for, can be one of:
        - "d" for today
        - "w" for this week
        - "m" for this month
        - "y" for this year

    :return: The content of the urls in the search results, example: url1\ntitle1\ntext1\n\nurl2\ntitle2\ntext2\n\n
    """
    results = await google(query, max_results, time)
    urls = [{"url": result["url"]} for result in results]
    contents = await read_urls(urls)
    all_contents = "\n\n".join(
        [f"{url}\n{result.get('title', '')}\n" f"{result.get('text', '')}\n\n" for url, result in contents.items()]
    )
    # query to path
    # query to file name
    query_file_name = query.replace(" ", "_")
    out_path = "out"
    os.makedirs(out_path, exist_ok=True)
    with open(f"{out_path}/{query_file_name[:50]}.txt", "w") as f:
        f.write(all_contents)
    return all_contents
