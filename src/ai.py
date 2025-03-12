from openai import AsyncOpenAI
import asyncio
from src.utils import ModelType



async def get_ai_responses(*, messages, model):
    """
    Call OpenAI's API to get an assistant response using the provided messages.
    
    Parameters:
        messages (list): A list of message dictionaries for the conversation.
        model: The model to use for generating a response (expected to have 'value' and 'name' attributes).
        
    Returns:
        str: The assistant's reply, or an error message if something goes wrong.
    """
    try:
        client = AsyncOpenAI()
        if model == ModelType.REASONING:
            response = await client.chat.completions.create(
                model= model.value,
                messages=messages
            )
        elif model == ModelType.SUMMARIZING:
            response = await client.chat.completions.create(
                model=model.value,
                messages=messages,
                temperature=0
            )
        else:
            print("Invalid model type.")
            return "Sorry, I couldn't generate a response."
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't generate a response."
