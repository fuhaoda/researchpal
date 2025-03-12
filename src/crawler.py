"""
Handles web crawling and scraping using Crawl4AI.
For each URL, crawls and extracts markdown content.
"""

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, PruningContentFilter
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
    crawler_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(
            threshold=0.35,  # Less aggressive filtering (was 0.5)
            threshold_type="fixed",  # Use a fixed threshold to keep more content
            min_word_threshold=20  # Retain more short sections
        )
    ),
    
    exclude_external_links=False,  # Allow external references for research
    exclude_social_media_links=True,  # Still remove distracting social links
    )
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