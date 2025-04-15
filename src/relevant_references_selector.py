import asyncio
from src.ai import get_embbded_text
import numpy as np

async def batched_gather(tasks, batch_size):
    results = []
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
    return results

async def compute_embeddings(text_list):
    # Compute embeddings for each text in the list using batching to avoid rate limits.
    tasks = [get_embbded_text(text) for text in text_list]
    embeddings = await batched_gather(tasks, batch_size=2000)
    # Convert each embedding to a NumPy array for efficient similarity computation.
    return [np.array(emb) for emb in embeddings]

async def textlist_textlist_similarity(textlist_1, textlist_2):
    # Pre-compute embeddings for both lists.
    embeddings_1 = await compute_embeddings(textlist_1)
    embeddings_2 = await compute_embeddings(textlist_2)
    
    # Compute pairwise cosine similarities.
    similarities = []
    for emb1 in embeddings_1:
        norm1 = np.linalg.norm(emb1)
        row_similarities = []
        for emb2 in embeddings_2:
            norm2 = np.linalg.norm(emb2)
            if norm1 == 0 or norm2 == 0:
                sim = 0.0
            else:
                sim = emb1.dot(emb2) / (norm1 * norm2)
            row_similarities.append(sim)
        similarities.append(row_similarities)
    
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