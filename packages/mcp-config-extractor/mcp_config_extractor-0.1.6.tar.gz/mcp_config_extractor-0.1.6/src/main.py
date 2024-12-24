#!/usr/bin/env python3
import os
import json
import asyncio
import argparse
from .llm_client import LLMClient
from dotenv import load_dotenv
from .config_extractor import get_config

# Load .env from the current working directory
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=dotenv_path)

async def main(github_url: str):
    template = await get_config(llm, github_url)
    print(json.dumps(template, indent=2))

def parse_args():
    parser = argparse.ArgumentParser(description='Extract mcp server config from GitHub repository README. Please refer to https://github.com/weightwave/mcp-registry for more details.')
    parser.add_argument('-s', '--source', required=True, help='GitHub repository URL')
    parser.add_argument('-u', '--openrouter-base-url', help='OpenRouter base URL (overrides environment variable)')
    parser.add_argument('-k', '--openrouter-api-key', help='OpenRouter API key (overrides environment variable)')
    return parser.parse_args()

def main_cli():
    args = parse_args()
    
    # Priority: command line args > environment variables
    base_url = args.openrouter_base_url or os.getenv("OPENROUTER_BASE_URL")
    api_key = args.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
    
    if not base_url or not api_key:
        raise ValueError("OpenRouter base URL and API key must be provided either through environment variables or command line arguments")
    
    global llm
    llm = LLMClient(base_url, api_key)
    llm.set_system_prompt("""
    You are a professional web scraper helper. Your task is to extract precise and accurate information from the content provided.
    For the commandInfo:
    - Prefer the one for Claude Desktop that use 'npx' or 'uvx' command, you can usually find in the content as Json with key "mcpServers"
    - Look for build scripts or main entry points
    - Include any necessary environment variables mentioned in the README
    """)
    
    asyncio.run(main(args.source))

if __name__ == "__main__":
    main_cli()
