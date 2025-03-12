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


    report = await get_ai_responses(messages= messages, model= ModelType.SUMMARIZING)

    report += "\n\n" + "##All Reference Links\n\n" + "\n".join(f"- [{url}]({url})" for url in urls) + "\n\n"

    return report

