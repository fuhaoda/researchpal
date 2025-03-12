"""
Core research functionality.
Supports both recursive deep research and supporting evidence collection.

Functions:
- conduct_research: recursively gathers learnings using SERP queries, web crawling, and OpenAI.
- find_supporting_evidence: extracts supporting references for given text chunks.
"""

import asyncio
from src.config import RESEARCH_DEPTH, MAX_REFERENCE_PER_PARAGRAPH
from src.serp import generate_serp_queries, search_serp
from src.crawler import crawl_urls
from src.extract_learnings import extract_learnings


async def conduct_research(messages, depth=RESEARCH_DEPTH, progress=None, visited_urls=None):
    """
    Recursively conduct research.
    1. Generate follow-up questions (if not provided).
    2. Generate SERP queries using the provided query and follow-up responses.
    3. Search each query to get URLs, filtering out URLs that have already been visited.
    4. Crawl new URLs and extract learnings.
    5. If depth > 1, use current learnings as new follow-up info and repeat.
    
    Parameters:
       messages: original research question and follow-up answers.
       depth (int): Current recursion depth.
       progress (ProgressManager): Progress manager instance (optional).
       visited_urls (set): Set of URLs that have already been crawled.
    
    Returns:
       dict: { "messages": updated messages,
               "learnings": List[str],
               "visited_urls": List[str],
               "crawl_results": List[dict] }
    """
    if visited_urls is None:
        visited_urls = set()
        
    if progress:
        progress.update(f"Conducting research at depth {depth}...")

    # Generate SERP queries via OpenAI (simulation).
    serp_queries = await generate_serp_queries(messages)

    # Gather new URLs from search results, skipping already visited ones.
    new_urls = set()
    for query in serp_queries:
        urls = await search_serp(query)
        for url in urls:
            if url not in visited_urls:
                new_urls.add(url)
                visited_urls.add(url)
    unique_urls = list(new_urls)
    
    if progress:
        progress.update(f"Found {len(unique_urls)} new unique URLs for research.")

    # Crawl the new URLs.
    crawl_results = await crawl_urls(unique_urls)
    
    # Extract learnings.
    current_learnings = await extract_learnings(crawl_results)

    # Append additional context for further exploration.
    messages.append({"role": "user", "content": f"Additional context: {current_learnings}"})
    
    # Recursive exploration.
    if depth > 1:
        await conduct_research(messages=messages, depth=depth-1, progress=progress, visited_urls=visited_urls)

    return {"messages": messages,
            "visited_urls": list(visited_urls)}

# async def find_supporting_evidence(input_text, progress=None):
#     """
#     For a given input text, break it into chunks and, for each chunk,
#     generate SERP queries, crawl results, and extract supporting references.
#     Each reference includes a title (using the original URL), the link, and a statement.
    
#     Parameters:
#        input_text (str)
#        progress (ProgressManager, optional)
    
#     Returns:
#        dict: Mapping chunk -> List[reference dict]
#     """
#     chunks = split_text_into_chunks(input_text)
#     evidence = {}
#     for chunk in chunks:
#         if progress:
#             progress.update(f"Processing evidence for chunk: {chunk[:50]}...")
#         serp_queries = generate_serp_queries(chunk)
#         unique_urls = set()
#         for query in serp_queries:
#             urls = search_serp(query)
#             unique_urls.update(urls)
#         unique_urls = list(unique_urls)
#         crawl_results = await crawl_urls(unique_urls)
        
#         references = []
#         count = 0
#         for result in crawl_results:
#             if count >= MAX_REFERENCE_PER_PARAGRAPH:
#                 break
#             if result.get("success") and result.get("markdown"):
#                 statement = result["markdown"].strip().split("\n")[0]
#                 reference_title = result["url"]  # In practice, extract title from content.
#                 references.append({
#                     "reference_title": reference_title,
#                     "link": result["url"],
#                     "statement": statement
#                 })
#                 count += 1
#         evidence[chunk] = references
#     return evidence