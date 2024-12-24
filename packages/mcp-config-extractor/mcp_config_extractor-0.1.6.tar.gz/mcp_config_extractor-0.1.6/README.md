# MCP Config Extractor

Extract MCP server configurations from GitHub repository READMEs.

## Installation

```bash
pip install mcp-config-extractor
```

## Usage

```bash
mcp-extract -s https://github.com/user/repo
```

### Additional Arguments

- `-u, --url`: OpenRouter base URL (overrides environment variable)
- `-k, --key`: OpenRouter API key (overrides environment variable)

## Environment Variables

The following environment variables are required:

- `OPENROUTER_BASE_URL`: OpenRouter API base URL
- `OPENROUTER_API_KEY`: OpenRouter API key

You can set these in a `.env` file in your working directory.

## Output

The tool outputs a JSON configuration that includes:
- Repository information
- Command information for running the server
- Required parameters and environment variables
- Tags and description

For more details, visit: https://github.com/weightwave/mcp-registry
