from src.utils import split_into_three_sentences
from src.relevant_references_selector import relevant_references_selector

import asyncio
from src.ai import get_ai_responses
from src.utils import ModelType


async def generate_annotated_report(base_report, urls_with_summaries):
    blocks = split_into_three_sentences(base_report)
    blocks_with_selected_references =await relevant_references_selector(blocks, urls_with_summaries)

    # For each block and each of its selected references, create a task to generate a supporting statement.
    support_tasks = []
    for block_index, block_item in enumerate(blocks_with_selected_references):
        block_text = block_item["block"]
        for ref_index, ref in enumerate(block_item["selected_references"]):
            prompt = (
                f"Based on the report block: \"{block_text}\", "
                f"and the reference summary: \"{ref['summary']}\", "
                f"Write the most related extracted sentence from summary (or write a brief two-sentence summary) to support the report block"
            )
            message_payload = [{"role": "user", "content": prompt}]
            task = asyncio.create_task(get_ai_responses(messages=message_payload, model=ModelType.SUMMARIZING))
            support_tasks.append((block_index, ref_index, task))

    # Await all supporting statement generation tasks concurrently
    responses = await asyncio.gather(*(task for _, _, task in support_tasks))
    for (block_idx, ref_idx, _), response in zip(support_tasks, responses):
        blocks_with_selected_references[block_idx]["selected_references"][ref_idx]["supporting_statement"] = response.strip()

    # Format the annotated report by including the block along with its references and their new supporting statements.
    annotated_report = ""
    for block_item in blocks_with_selected_references:
        annotated_report += f"# Annotated Report \n\n> {block_item['block']}\n\n"
        for ref in block_item["selected_references"]:
            annotated_report += f"- **URL:** [{ref['url']}]({ref['url']})\n"
            annotated_report += f"**Supporting Statement:** {ref['supporting_statement']}\n\n"
        annotated_report += "\n"
    return annotated_report