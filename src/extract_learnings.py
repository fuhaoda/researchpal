
from src.utils import url_separator_begin, url_separator_end

async def extract_learnings(crawled_results):
    """
    Extract key learnings from crawled markdown results.
    (For this demo, we simply take the first non-empty line.)
    
    Parameters:
       crawled_results (List[dict])
    
    Returns:
       List[str]: Extracted learning points.
    """
    learnings = ""
    for result in crawled_results:
        if result.get("success"):
            summary = result.get("summary", "")
            if summary:
                url_str = result.get("url", "")
                learnings += f"{url_separator_begin}\n **Source URL:** \"{url_str}\"\n{summary.strip()}\n{url_separator_end}\n\n"          
    return learnings