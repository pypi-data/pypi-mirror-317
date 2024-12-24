import json
from datetime import datetime, timezone
from src.github_scraper import get_github_readme
from src.llm_client import LLMClient
from src.utils import clean_markdown_response

class GitHubScraperError(Exception):
    """Custom exception for GitHub scraping related errors"""
    pass

def get_empty_template() -> dict:
    return {
        "id": "",
        "title": "",
        "description": "",
        "tags": [],
        "creator": "",
        "logoUrl": "",
        "publishDate": "",
        "rating": 5,
        "sources": {
            "github": ""
        },
        "type": "stdio",
        "commandInfo": {
            "command": "",
            "args": [],
            "env": {}
        },
        "defVersion": "1",
        "parameters": {},
    }

async def extract_info_with_llm(llm: LLMClient, content: str) -> dict:
    prompt = f"""
Given this README content from a GitHub repository:

{content}

Extract the following information in JSON format:
1. A concise description (1-2 sentences max)
2. tags (around 3, technology keywords)
3. 
-Any environment variables or configuration parameters required in either args or env (name, type, description, required).
-Format the value of parameter as **PARAM_NAME**, so that it can be manually injected later.
-Parameters only contains required parameters that wrapped by ** like **PARAM_NAME**, do not include others
4. Command information for running the server (command, arguments, environment variables)

Format the response as a JSON object with these exact keys:
{{
    "description": "string",
    "tags": ["string"],
    "commandInfo": {{
        "command": "string",  // e.g., "npx", "uvx"
        "args": [        
            "-y",
            "@modelcontextprotocol/server-aws-kb-retrieval",
            "-e",
            "**PARAM_NAME_1**"

        ],   // e.g., ["build/index.js", "--port", "3000"]
        "env": {{             // Required environment variables for running
            "PARAM_NAME_2": "**PARAM_NAME_2**"
        }}
    }},
    "parameters": {{
        "PARAM_NAME_1": {{
            "type": "string",
            "required": boolean,
            "description": "string"
        }},
        "PARAM_NAME_2": {{
            "type": "string",
            "required": boolean,
            "description": "string"
        }}
    }}
}}
"""

    response = await llm.generate_completion(prompt, model="openai/chatgpt-4o-latest",remember=True)
    
    try:
        cleaned_response = clean_markdown_response(response)
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        return {
            "description": "",
            "tags": [],
            "parameters": {},
            "commandInfo": {
                "command": "",
                "args": [],
                "env": {}
            }
        }

async def get_config(llm: LLMClient, github_url: str) -> dict:
    author, repo, content, success = get_github_readme(github_url)
    
    if not success:
        raise GitHubScraperError(f"Failed to fetch GitHub README: {content}")

    template = get_empty_template()
    template["id"] = repo
    template["title"] = repo.title()
    template["creator"] = author
    template["sources"]["github"] = github_url
    template["publishDate"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Extract additional info using LLM
    info = await extract_info_with_llm(llm, content)
    template["description"] = info["description"]
    template["tags"] = info["tags"]
    template["parameters"] = info["parameters"]
    template["commandInfo"] = info["commandInfo"]
    
    return template