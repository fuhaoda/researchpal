"""
Handles web crawling and scraping using Crawl4AI.
For each URL, crawls and extracts markdown content.
"""

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from src.ai import get_ai_responses
from src.prompts import summarize_crawl
from src.utils import ModelType
async def crawl_url(url):
    """
    Crawl a single URL using Crawl4AI.
    
    Parameters:
       url (str): The URL to crawl.
    
    Returns:
       dict: A dictionary with keys 'url', 'success', and 'markdown'.
    """
    crawler_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url, config=crawler_config)
            if result.success:
                messages = summarize_crawl + [{"role": "user", "content": result.markdown}]
                summary = await get_ai_responses(messages=messages, model= ModelType.SUMMARIZING)
            return {
                "url": url,
                "success": result.success,
                "markdown": result.markdown if result.success else "",
                "summary": summary if result.success else ""
            }
    except Exception as e:
        return {"url": url, "success": False, "markdown": "", "summary":"","error": str(e)}

async def crawl_urls(urls):
    """
    Crawl a list of URLs concurrently.
    
    Parameters:
       urls (List[str]): The list of URLs.
    
    Returns:
       List[dict]: List of crawl result dictionaries.
    """
    tasks = [crawl_url(url) for url in urls]
    return await asyncio.gather(*tasks)