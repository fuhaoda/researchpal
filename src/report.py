"""
Handles the generation of the final report.
Uses an OpenAI SUMMARIZING_MODEL (e.g., "gpt-4o-mini") to create a detailed report and
append reference blocks for each report chunk.
"""

from src.ai import get_ai_responses
from src.utils import ModelType
from src.prompts import generate_report_research
from src.generate_annotated_report import generate_annotated_report
import os
import json

async def generate_research_report(research_results=None, progress=None):
    """
    Generate a base report from the research question and key learnings.
    (A real implementation would call the OpenAI SUMMARIZING_MODEL.)
    
    Parameters:
       user_query (str): Original research question.
       learnings (List[str]): Extracted learning points.
    
    Returns:
       str: A markdown-formatted report.
    """
    messages = generate_report_research + research_results.get("messages", [])

   #   ## debug setting begin ##
   #  import json

    def save_messages(messages, filepath):
      """
      Save a list of messages to a JSON file.

      Parameters:
         messages (list): The list of message dictionaries to save.
         filepath (str): The path to the file where the messages will be saved.
      """
      with open(filepath, "w", encoding="utf-8") as f:
         json.dump(messages, f, indent=2)
    save_filepath = "output/saved_messages.json"
    save_messages(research_results.get("messages", []), save_filepath)
    ## debug setting end ##

    
    if progress:
        progress.update(f"Generating base report...")  
    report = await get_ai_responses(messages= messages, model= ModelType.SUMMARIZING)

    urls = research_results.get("visited_urls", [])
    urls_summaries = research_results.get("urls_summaries", [])
    
    # Save the base report and urls_summaries to a file for debugging purposes.

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    urls_summaries_path = os.path.join(output_dir, "urls_summaries.json")
    with open(urls_summaries_path, "w", encoding="utf-8") as f:
        json.dump(urls_summaries, f, indent=2)

    visited_urls_path = os.path.join(output_dir, "visited_urls.json")
    with open(visited_urls_path, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)


    # Example of loading the data
    # with open(report_path, "r", encoding="utf-8") as f:
    #    report = f.read()    
    # with open(urls_summaries_path, "r", encoding="utf-8") as f:
    #    urls_summaries = json.load(f)

    if progress:
        progress.update(f"Generating annotated report...")  
    annotated_report = await generate_annotated_report(report, urls_summaries, progress=progress)   

    if progress:
        progress.update(f"Generating the final research report...")    
    final_report =  report + annotated_report+ "\n\n" + "## All Reference Links\n\n" + "\n".join(f"- [{url}]({url})" for url in urls) + "\n\n" +"\n\n" + "\n---\n"
    
    return final_report

async def generate_evidence_report(blocks_with_references, supporting_evidence):
    report = "# Final Evidence Report\n\n"
    assert len(blocks_with_references) == len(supporting_evidence), "blocks_with_references and supporting_evidence must have the same length"
    # Iterate over each block along with its corresponding supporting evidence
    for idx, block in enumerate(blocks_with_references):
        # Retrieve the statement from the block (fallback if missing)
        statement = block.get("statement", "No statement provided.")
        # Get supporting evidence for the block; if not available, display a fallback message.
        evidence = supporting_evidence[idx].strip() if idx < len(supporting_evidence) else "No supporting evidence available."
        
        report += "\n---\n" + "\n---\n" + f"## Statement {idx + 1}\n\n"
        report += "**Statement:**\n\n"+f"> {statement}\n\n"
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


async def appendix_report(research_results=None):
    urls_summaries = research_results.get("urls_summaries", [])
    
    appendix = "# Appendix: Summary of Key Learnings \n\n"
    
    for url_summary in urls_summaries:
         url = url_summary['url']
         summary = url_summary['summary']
         appendix += "\n---\n" + "\n---\n" + f"### [{url}]({url})\n\n{summary}" + "\n\n"

    return appendix