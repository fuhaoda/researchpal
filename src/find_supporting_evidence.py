import asyncio
from src.utils import url_separator_begin, url_separator_end
from src.ai import get_ai_responses
from src.utils import ModelType 
from src.prompts import find_evidence

async def generate_evidence_for_a_block(block_with_references):
    block = block_with_references["statement"]
    references = block_with_references["references"]
    learnings = ""
    for ref in references:
        summary = ref.get("summary", "")
        url_str = ref.get("url", "")
        learnings += f"{url_separator_begin}\n **Source URL:** \"{url_str}\" \n{summary.strip()}\n{url_separator_end}\n\n"          
    
    user_input = "Original Statement:"+ block + "\n\n" + "Supporting Evidence:" + learnings
    
    messages = find_evidence+[{"role": "user", "content": user_input}]
    support_evidence = await get_ai_responses(messages= messages, model= ModelType.SUMMARIZING)
    
    return support_evidence



async def find_supporting_evidence(blocks_with_references):
    tasks = [generate_evidence_for_a_block(block) for block in blocks_with_references]
    return await asyncio.gather(*tasks)