"""
Handles the generation of the final report.
Uses an OpenAI SUMMARIZING_MODEL (e.g., "gpt-4o-mini") to create a detailed report and
append reference blocks for each report chunk.
"""

from src.ai import get_ai_responses
from src.utils import ModelType
from src.prompts import generate_report

async def generate_base_report(research_results=None):
    """
    Generate a base report from the research question and key learnings.
    (A real implementation would call the OpenAI SUMMARIZING_MODEL.)
    
    Parameters:
       user_query (str): Original research question.
       learnings (List[str]): Extracted learning points.
    
    Returns:
       str: A markdown-formatted report.
    """
    messages = generate_report + research_results.get("messages", [])
    urls = research_results.get("visited_urls", [])
    urls_summaries = research_results.get("urls_summaries", [])

    report = await get_ai_responses(messages= messages, model= ModelType.SUMMARIZING)

    report += "\n\n" + "## All Reference Links\n\n" + "\n".join(f"- [{url}]({url})" for url in urls) + "\n\n"
    report += "\n\n" + "\n---\n" + "\n" + "# Appendix: Summary of Key Learnings \n\n"
    for url_summary in urls_summaries:
         url = url_summary['url']
         summary = url_summary['summary']
         report += "\n---\n" + "\n---\n" + f"### [{url}]({url})\n\n{summary}" + "\n\n"
    return report

async def generate_evidence_report(blocks_with_references, supporting_evidence):
    report = "# Final Evidence Report\n\n"
    # Iterate over each block along with its corresponding supporting evidence
    for idx, block in enumerate(blocks_with_references):
        # Retrieve the statement from the block (fallback if missing)
        statement = block.get("statement", "No statement provided.")
        # Get supporting evidence for the block; if not available, display a fallback message.
        evidence = supporting_evidence[idx].strip() if idx < len(supporting_evidence) else "No supporting evidence available."
        
        report += "\n---\n" + "\n---\n" + f"## Statement {idx + 1}\n\n"
        report += f"**Statement:**\n\n{statement}\n\n"
        report += f"**Supporting Evidence:**\n\n{evidence}\n\n"
        report += "\n\n\n"
    
    report += "\n---\n" + "\n---\n"

    # Collect unique URL and summary pairs from blocks_with_references.
    unique_refs = {}
    for block in blocks_with_references:
        for ref in block.get("references", []):
            url = ref.get("url")
            summary = ref.get("summary", "").strip()
            if url:
                unique_refs[url] = summary  # ensure each url-summary pair is recorded uniquely.
    
    # Print out all unique URLs as links.
    if unique_refs:
        report += "\n---\n" + "\n---\n" + "# All Reference Links\n\n" + "\n".join(f"- [{url}]({url})" for url in sorted(unique_refs)) + "\n\n"
    
    # Print out the unique URL and summary pairs in the appendix.
    if unique_refs:
        report += "\n---\n" + "\n---\n" + "# Appendix: Summary of Key Learnings\n\n"
        for url in sorted(unique_refs):
            report += "\n---\n" + f"### [{url}]({url})\n\n{unique_refs[url]}\n\n"
    
    return report