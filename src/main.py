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
from src.report import generate_base_report
from src.progress import ProgressManager
from src.followups import followups

def get_short_description(text, max_words=3):
    """
    Generate a short description from the first few words of the given text.
    """
    words = text.split()
    return "_".join(words[:max_words]).lower() if words else "research"


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

        print("\n Enter your follow-up answers (Press Enter + Ctrl+D or Ctrl+Z to finish): \n")
        user_followup_answers = sys.stdin.read().strip() 
        
        messages = [{"role": "assistant", "content": "What's your research question?"},
                    {"role": "user", "content": user_initial_query}, 
                    {"role": "assistant", "content": followup_questions}, 
                    {"role": "user", "content": user_followup_answers}]
        progress.update("Starting research process...")
        
        research_results = await conduct_research(messages=messages, depth=RESEARCH_DEPTH, progress=progress)
        
        progress.update("Generating base report...")
        base_report = await generate_base_report(research_results=research_results)
        
        short_desc = get_short_description(user_initial_query)
        output_filename = os.path.join("output", f"research_result_{short_desc}.md")
        os.makedirs("output", exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(base_report)
        print(f"Final report saved to {output_filename}\n")
        
        
    elif choice == "2":
        print("coming soon!")
    #     print("Enter the text for which you want to find supporting evidence:")
    #     input_text = input().strip()
    #     progress.update("Processing supporting evidence...")
    #     evidence = await find_supporting_evidence(input_text, progress=progress)
    #     final_report = ""
    #     chunks = input_text.split("\n\n")
    #     for chunk in chunks:
    #         final_report += chunk + "\n\n"
    #         refs = evidence.get(chunk, [])
    #         for ref in refs:
    #             final_report += f"Reference Title: {ref['reference_title']}\n"
    #             final_report += f"Link: {ref['link']}\n"
    #             final_report += f"Statement: {ref['statement']}\n\n"
    #     short_desc = get_short_description(input_text)
    #     output_filename = os.path.join("output", f"supporting_evidence_{short_desc}.md")
    #     os.makedirs("output", exist_ok=True)
    #     with open(output_filename, "w", encoding="utf-8") as f:
    #         f.write(final_report)
    #     print(f"Supporting evidence report saved to {output_filename}\n")
    #     print(final_report)
        
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())