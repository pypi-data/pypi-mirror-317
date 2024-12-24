from asyncio import FastChildWatcher
import requests
from urllib.parse import urlparse


def get_github_readme(github_url: str) -> tuple[str, str, str, bool]:
    """
    Returns:
        tuple[str, str, str, bool]: A tuple containing:
            - author: Repository owner/organization
            - repo: Repository or subdirectory name
            - content: README content or error message
            - success: True if successful, False otherwise
    """
    path_paths = urlparse(github_url).path.strip('/').split('/')

    if (path_paths[0] == 'modelcontextprotocol'):
        return path_paths[0], *get_modelcontextprotocol_github_readme(github_url)
    else:
        return path_paths[0], *get_thirdparty_github_readme(github_url)


def get_thirdparty_github_readme(github_url: str) -> tuple[str, str, bool]:
    try:
        path_parts = urlparse(github_url).path.strip('/').split('/')
        if len(path_parts) < 2:
            return None, "Invalid GitHub URL format", False
            
        owner, repo = path_parts[0], path_parts[1]
        
        # Construct raw content URL for README
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
        response = requests.get(raw_url)
        
        if response.status_code == 404:
            # Try master branch if main doesn't exist
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
            response = requests.get(raw_url)
        
        if response.status_code == 200:
            return repo, response.text, True
        else:
            return repo, f"Failed to fetch README. Status code: {response.status_code}", False
            
    except Exception as e:
        return repo, f"Error: {str(e)}", False



def get_modelcontextprotocol_github_readme(github_url: str) -> tuple[str, str, bool]:
    try:
        path_parts = urlparse(github_url).path.strip('/').split('/')

        if len(path_parts) != 6 or "/".join(path_parts[:4]) != 'modelcontextprotocol/servers/tree/main':
            return None, "Invalid modelcontextprotocol URL format", False

        subdir = path_parts[-1]
        readme_paths = f"https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/{subdir}/README.md"
        print(readme_paths)
        
        response = requests.get(readme_paths)
        if response.status_code == 200:
            return subdir, response.text, True
                
        return subdir, f"Failed to fetch README. Status code: {response.status_code}", False
            
    except Exception as e:
        return subdir, f"Error: {str(e)}", False