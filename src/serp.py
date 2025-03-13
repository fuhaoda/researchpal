"""
Handles generation of follow-up questions and SERP queries via OpenAI models,
as well as searching using the googlesearch package.
"""

from src.config import SEARCH_PER_SERP
from src.ai import get_ai_responses
from src.utils import ModelType 
from googlesearch import search

async def generate_serp_queries(messages):
    """
    Generate up to MAX_SERP high-quality SERP queries using the REASONING model.
    
    Parameters:
       combined_query (str): The combined research question and follow-up answers.
    
    Returns:
       List[str]: A list of SERP query strings.
    """
    
    response = await get_ai_responses(messages=messages, model=ModelType.REASONING)
    queries = [line.strip() for line in response.split("\n") if line.strip()]
    return queries
    

async def search_serp(query):
    """
    Use the googlesearch package to search for a query.
    
    Parameters:
       query (str): The search query.
    
    Returns:
       List[str]: A list of URLs (up to SEARCH_PER_SERP results).
    """
    # Convert the generator to a list.
    return list(search(query, num_results=SEARCH_PER_SERP, unique=True, region="us"))