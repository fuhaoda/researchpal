"""
Main entry point for My ResearchPal.
Handles interactive prompts, process flow, and report generation.
"""
import os
import sys

if __name__ == "__main__" and __package__ is None:
    # Adjust the sys.path to include the parent directory
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Now set the package name so that relative imports work correctly.
    __package__ = "src"

import asyncio

from src.config import RESEARCH_DEPTH
from src.research import conduct_research
from src.report import generate_base_report, generate_evidence_report
from src.progress import ProgressManager
from src.followups import followups
from src.utils import split_into_three_sentences, unique_urls, ModelType
from src.blocks_to_urls import blocks_to_urls
from src.crawler import crawl_urls
from src.blocks_to_references import blocks_to_references
from src.find_supporting_evidence import find_supporting_evidence
from src.ai import get_ai_responses

async def get_short_description(text):
    """
    Generate a short description from the first few words of the given text.
    """
    message = [{"role":"system", "content": "find 3 words to summariz user input so that I can put in a file name."},{"role": "user", "content": text}]
    short_title = await get_ai_responses(messages=message, model=ModelType.SUMMARIZING)
    from datetime import datetime
    processed_title = short_title.strip().replace(" ", "_").lower()
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M")
    final_short_description = f"{processed_title}_{dt_string}"
    return final_short_description
    
async def main():
    progress = ProgressManager()
    print("Welcome to My ResearchPal!")
    print("Select an option:")
    print("1. Conduct a research on a topic")
    print("2. Find supporting evidence")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        print("Enter your research question (Press Enter + Ctrl+D or Ctrl+Z to finish):")
        user_initial_query = sys.stdin.read().strip()
        print("\n=========\n"+"DrBombe may need you to provide up to 5 follow-up clarifications... Here are the questions ...\n")
        user_initial_query_messages = [{"role": "user", "content": user_initial_query}]
        
        followup_questions = await followups(user_initial_query_messages)
        print(followup_questions)

        print("\n Enter your follow-up answers (Press Enter + Ctrl+D or Ctrl+Z to finish):")
        user_followup_answers = sys.stdin.read().strip() 
        
        messages = [{"role": "assistant", "content": "What's your research question?"},
                    {"role": "user", "content": user_initial_query}, 
                    {"role": "assistant", "content": followup_questions}, 
                    {"role": "user", "content": user_followup_answers}]
        progress.update("Starting research process...")
        
        research_results = await conduct_research(messages=messages, depth=RESEARCH_DEPTH, progress=progress)
        
        progress.update("Generating research report...")
        base_report = await generate_base_report(research_results=research_results)
        
        short_desc = await get_short_description(user_initial_query)
        output_filename = os.path.join("output", f"research_{short_desc}.md")
        os.makedirs("output", exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(base_report)
        print(f"Final report saved to {output_filename}\n")
        
        
    elif choice == "2": #"2. Find supporting evidence"
        print("Enter the text for which you want to find supporting evidence (Press Enter + Ctrl+D or Ctrl+Z to finish):")
        user_statement = sys.stdin.read().strip()

        
        splitted_statement = split_into_three_sentences(user_statement)
        progress.update("Step 1 complete: Statement successfully split into blocks of three sentences.")

        progress.update("Step 2: Generating SERP queries and retrieving URLs for each block...")
        ref_urls_from_splitted_statement = await blocks_to_urls(splitted_statement)
        progress.update("Step 2 complete: URLs retrieved for each block.")

        progress.update("Step 3: Crawling unique URLs from all blocks...")
        all_references = await crawl_urls(unique_urls(ref_urls_from_splitted_statement))
        progress.update("Step 3 complete: Unique URL crawling finished.")

        progress.update("Step 4: Organizing references by statement...")
        splitted_statement_with_references = await blocks_to_references(
            blocks=splitted_statement,
            urls=ref_urls_from_splitted_statement,
            references=all_references
        )
        progress.update("Step 4 complete: References organized by statement.")
       
        # Step 5: Generate Markdown summaries for each splitted statement.
        progress.update("Step 5: Generating Markdown summaries for each splitted statement...")
        supporting_evidence = await find_supporting_evidence(splitted_statement_with_references)
        progress.update("Step 5 complete: Generated Markdown summaries for splitted statement.")
        
        # Step 6: Generate the final report by compiling all markdown sections.
        progress.update("Step 6: Compiling all markdown sections into the final evidence report...")
        final_report = await generate_evidence_report(blocks_with_references=splitted_statement_with_references, supporting_evidence=supporting_evidence)
        progress.update("Step 6 complete: Final evidence report generated.")
        
        # Save the final report.
        short_desc = await get_short_description(user_statement)
        output_filename = os.path.join("output", f"evidence_{short_desc}.md")
        os.makedirs("output", exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)
        progress.update(f"Report saved to {output_filename}")
        print(f"Supporting evidence report saved to {output_filename}\n")
 
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())