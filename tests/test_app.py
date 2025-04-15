import json
import os
import sys
import asyncio  # Added to enable async execution

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.ai import get_embbded_text


async def main():
    x = await get_embbded_text("Hello, how are you?")
    print(x)

if __name__ == "__main__":
    asyncio.run(main())