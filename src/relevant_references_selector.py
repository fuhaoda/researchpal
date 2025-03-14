import asyncio
from src.ai import get_embbded_text
import numpy as np

async def text_text_similarity(text1, text2):
    emb1, emb2 = await asyncio.gather(
        get_embbded_text(text1),
        get_embbded_text(text2)
    )
    # Convert embeddings to NumPy arrays
    emb1 = np.array(emb1)
    emb2 = np.array(emb2)

    similarity = emb1.dot(emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
 
    return similarity

async def textlist_textlist_similarity(textlist_1, textlist_2):
    
    similarities = []
    
    all_tasks = [text_text_similarity(text1, text2) for text1 in textlist_1 for text2 in textlist_2]
    flat_results = await asyncio.gather(*all_tasks)
    num_text2 = len(textlist_2)
    similarities = [flat_results[i * num_text2:(i + 1) * num_text2] for i in range(len(textlist_1))]

    # debug codes illustration
    # Define two simple lists
    # textlist_1 = ['a', 'b', 'c']
    # textlist_2 = ['x', 'y']

    # # Consolidate: Create a flat list of all paired combinations
    # # This simulates what the async function would return, but using a simple string operation.
    # # For each element in textlist_1, combine it with every element in textlist_2.
    # flat_results = [f"{t1}-{t2}" for t1 in textlist_1 for t2 in textlist_2]
    # print("Flat results:", flat_results)
    # # Expected output:
    # # Flat results: ['a-x', 'a-y', 'b-x', 'b-y', 'c-x', 'c-y']

    # # Now, calculate how many items from textlist_2 there are.
    # num_text2 = len(textlist_2)

    # # Split: Group the flat list into sublists, one for each item in textlist_1.
    # # Each subgroup contains num_text2 items.
    # grouped_results = [flat_results[i * num_text2:(i + 1) * num_text2] for i in range(len(textlist_1))]
    # print("Grouped results:", grouped_results)
    # # Expected output:
    # # Grouped results: [['a-x', 'a-y'], ['b-x', 'b-y'], ['c-x', 'c-y']]#
    return similarities

async def relevant_references_selector(blocks, urls_with_summaries): 
    
    summaries = [entry["summary"] for entry in urls_with_summaries]

    similarities = await textlist_textlist_similarity(blocks, summaries)
    
    blocks_with_selected_references = []
    for i, block in enumerate(blocks):
        # Get similarity scores for the current block across all summaries
        block_similarities = similarities[i]
        # Sort indices of summaries by descending similarity score
        sorted_indices = sorted(range(len(block_similarities)), key=lambda j: block_similarities[j], reverse=True)
        # Select at most the top 5 most related summaries with their URLs
        top_indices = sorted_indices[:5]
        selected_refs = [urls_with_summaries[j] for j in top_indices]
        
        blocks_with_selected_references.append({
            "block": block,
            "selected_references": selected_refs
        })
    
    return blocks_with_selected_references