

async def blocks_to_references(blocks, urls, references):
    """
    Associates each text block with a list of supporting references.

    Parameters:
      blocks (list): List of text blocks (statements).
      urls (list): List of URL lists; each sub-list corresponds to a text block.
      references (list): List of crawl result dictionaries for various URLs.

    Returns:
      list: A list where each element is a dictionary with:
          - "statement": The original text block.
          - "references": A list of dictionaries, each containing a "url" and its "summary" 
                          from successful crawl results.
    """
    # Build a lookup dictionary mapping URLs to their successful crawl results.
    url_to_reference = {ref["url"]: ref for ref in references if ref.get("success")}

    # Initialize list to store the final result of blocks with associated references.
    blocks_with_references = []

    # Iterate over each text block together with its corresponding list of URLs.
    for block, block_urls in zip(blocks, urls):
        # Initialize a list to collect references for the current block.
        block_references = []
        # For each URL related to the current block, check if there is a successful crawl result.
        for url in block_urls:
            if url in url_to_reference:
                # Append the reference data with URL and its summary.
                block_references.append({
                    "url": url,
                    "summary": url_to_reference[url].get("summary", "")  # Default to empty string if summary is missing.
                })
        # Append the block along with its gathered references to the result list.
        blocks_with_references.append({
            "statement": block,
            "references": block_references
        })

    # Return the final list mapping each block to its corresponding references.
    return blocks_with_references



