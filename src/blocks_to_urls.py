# Import the required functions from the serp module and the asyncio library for asynchronous processing.
from src.serp import generate_serp_queries, search_serp
import asyncio

# Asynchronously processes a single block of text.
# This function generates SERP queries for the block, executes search tasks concurrently,
# and returns a deduplicated list of URLs obtained from the search results.
async def process_block(block):
    # Prepare a message payload based on the text block.
    messages = [{"role": "user", "content": block}]
    # Generate search queries using the SERP module.
    queries = await generate_serp_queries(messages)
    # Create asynchronous search tasks for each query.
    query_tasks = [search_serp(query) for query in queries]
    # Execute all search tasks concurrently and collect the results.
    query_results = await asyncio.gather(*query_tasks)
    # Flatten the list of URL lists from each query result.
    urls = []
    for result in query_results:
        urls.extend(result)
    # Remove duplicates by converting the list to a set, then back to a list.
    return list(set(urls))

# Asynchronously processes multiple text blocks.
# Each block is processed via the process_block function to fetch URLs,
# and the results are returned as a list where each element is a deduplicated URL list.
async def blocks_to_urls(blocks):
    # Create a list of asynchronous tasks for each block.
    tasks = [process_block(block) for block in blocks]
    # Wait for all processing tasks to complete concurrently.
    urls = await asyncio.gather(*tasks)
    # Return the combined results.
    return urls