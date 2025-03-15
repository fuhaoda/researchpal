from src.utils import split_into_three_sentences
from src.relevant_references_selector import relevant_references_selector

import asyncio
from src.ai import get_ai_responses
from src.utils import ModelType
from src.prompts import extract_title_n_one_sentence

async def generate_annotated_report(base_report, urls_with_summaries):
    blocks = split_into_three_sentences(base_report)
    blocks_with_selected_references =await relevant_references_selector(blocks, urls_with_summaries)

    # For each block and each of its selected references, create a task to generate a supporting statement.
    ## debug setting begin ##
    import json
    import os

    def save_debug_info(data, filename="debug_blocks.json"):
        """
        Saves the provided 'blocks_with_selected_references' data to a JSON file in the project root output folder.
        """
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Debug data saved to {file_path}")

    save_debug_info(blocks_with_selected_references)
    
    ## debug setting end ##

    support_tasks = []
    for block_index, block_item in enumerate(blocks_with_selected_references):
        block_text = block_item["block"]
        for ref_index, ref in enumerate(block_item["selected_references"]):
            block_text_with_summary = f"**Report Block**:\n{block_text}\n\n**Reference Summary**:\n{ref['summary']}"
            messages = extract_title_n_one_sentence + [{"role": "user", "content": block_text_with_summary}]
            task = asyncio.create_task(get_ai_responses(messages=messages, model=ModelType.SUMMARIZING))
            support_tasks.append((block_index, ref_index, task))

    # Await all supporting statement generation tasks concurrently
    responses = await asyncio.gather(*(task for _, _, task in support_tasks))
    for (block_idx, ref_idx, _), response in zip(support_tasks, responses):
        blocks_with_selected_references[block_idx]["selected_references"][ref_idx]["supporting_statement"] = response.strip()

    # Format the annotated report by including the block along with its references and their new supporting statements.
    annotated_report = "\n"+ "# Annotated Report \n\n"

    for idx, block_item in enumerate(blocks_with_selected_references):
        annotated_report += "\n---\n" + "\n---\n" + f"## Statement {idx + 1}\n\n"
        quoted_block = "> " + block_item['block'].strip().replace("\n", "\n> ")
        annotated_report += f"{quoted_block}\n\n**Supporting Evidence:**\n\n"
        for ref in block_item["selected_references"]:
            annotated_report += "\n---\n"+f"\n{ref['supporting_statement']}\n"
            annotated_report += "\n"+f"**Link:** [{ref['url']}]({ref['url']})\n"
        annotated_report += "\n"
    return annotated_report