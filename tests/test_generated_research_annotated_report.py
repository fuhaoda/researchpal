
import json
import os
import sys
import asyncio  # Added to enable async execution

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.ai import get_ai_responses
from src.utils import ModelType
from src.prompts import extract_title_n_one_sentence
from src.progress import ProgressManager
from src.generate_annotated_report import generate_annotated_report

def load_debug_info(report_filename="report.md", urls_summaries_filename="urls_summaries.json"):
        """
        Loads the 'blocks_with_selected_references' data from a JSON file in the project root output folder.
        """
        output_dir = os.path.join(os.getcwd(), "output")
        report_file_path = os.path.join(output_dir, report_filename)
        with open(report_file_path, "r", encoding="utf-8") as f:
            report = f.read()

        urls_summaries_path = os.path.join(output_dir, urls_summaries_filename)
        with open(urls_summaries_path, "r", encoding="utf-8") as f:
            urls_summaries = json.load(f)
        
        visited_urls_path = os.path.join(output_dir, "visited_urls.json")
        with open(visited_urls_path, "r", encoding="utf-8") as f:
            urls = json.load(f)
        return report, urls_summaries, urls 

async def main():

    report, urls_summaries, urls = load_debug_info()

    # # Print out the first 5 lines to check the results
    # report_lines = report.splitlines()
    # print("Report (first 5 lines):\n" + "\n".join(report_lines[:5]))
    
    # urls_summaries_str = json.dumps(urls_summaries, indent=2)
    # urls_summaries_lines = urls_summaries_str.splitlines()
    # print("Urls Summaries (first 5 lines):")
    # for line in urls_summaries_lines[:5]:
    #     print(line)
    urls_summaries = urls_summaries
    progress = ProgressManager()
    if progress:
        progress.update(f"Generating annotated report...")  
    annotated_report = await generate_annotated_report(report, urls_summaries, progress=progress)   

    if progress:
        progress.update(f"Generating the final research report...")    
    final_report =  report + annotated_report+ "\n\n" + "## All Reference Links\n\n" + "\n".join(f"- [{url}]({url})" for url in urls) + "\n\n" +"\n\n" + "\n---\n"
    

    
    short_desc = "annotated_report_test"
    output_filename = os.path.join("output", f"research_result_{short_desc}.md")
    os.makedirs("output", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(annotated_report)
    print(f"Final report saved to {output_filename}\n")

if __name__ == "__main__":
    asyncio.run(main())
    