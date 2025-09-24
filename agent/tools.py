import pathlib
import subprocess
import re
from typing import Tuple

from langchain_core.tools import tool

# Global variable to store the current project root
PROJECT_ROOT = None


def generate_project_name(user_prompt: str) -> str:
    """Generate a project folder name based on the user prompt."""
    # Extract key words from the prompt
    words = re.findall(r'\b\w+\b', user_prompt.lower())
    
    # Filter out common words
    common_words = {'build', 'create', 'make', 'a', 'an', 'the', 'in', 'with', 'and', 'or', 'for', 'to', 'of', 'app', 'application', 'web', 'site'}
    meaningful_words = [word for word in words if word not in common_words and len(word) > 2]
    
    # Take first 3 meaningful words or use a default
    if meaningful_words:
        project_name = '_'.join(meaningful_words[:3])
    else:
        project_name = 'generated_project'
    
    # Clean up the name (remove special characters, limit length)
    project_name = re.sub(r'[^a-zA-Z0-9_]', '', project_name)
    project_name = project_name[:30]  # Limit length
    
    return project_name if project_name else 'generated_project'


def set_project_root(user_prompt: str):
    """Set the project root based on the user prompt."""
    global PROJECT_ROOT
    project_name = generate_project_name(user_prompt)
    PROJECT_ROOT = pathlib.Path.cwd() / project_name


def safe_path_for_project(path: str) -> pathlib.Path:
    if PROJECT_ROOT is None:
        raise ValueError("Project root not initialized. Call set_project_root() first.")
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to write outside project root")
    return p


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def init_project_root():
    """Initialize the project root directory."""
    if PROJECT_ROOT is None:
        raise ValueError("Project root not initialized. Call set_project_root() first.")
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)