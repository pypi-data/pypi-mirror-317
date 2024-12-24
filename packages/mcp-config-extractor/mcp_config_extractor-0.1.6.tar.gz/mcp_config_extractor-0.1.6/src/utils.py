def clean_markdown_response(response: str) -> str:
    # Remove markdown code block markers if present
    if response.startswith("```json\n"):
        response = response.replace("```json\n", "", 1)
        if response.endswith("\n```"):
            response = response[:-4]
    elif response.startswith("```\n"):
        response = response.replace("```\n", "", 1)
        if response.endswith("\n```"):
            response = response[:-4]
    return response.strip()