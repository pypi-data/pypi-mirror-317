import os
import subprocess
import json
from pathlib import Path
from typing import Callable, List, Dict, Any, TypedDict
from datetime import datetime

# Memory file is a simple log of important information
MEMORY_FILE = Path.home() / ".termites" / "memory.log"

def read_memory() -> Dict[str, Any]:
    """
    Read the entire memory log.
    
    Returns:
        Dict containing memory contents or error
    """
    try:
        if not MEMORY_FILE.exists():
            return {
                "success": True,
                "content": []
            }
        
        memories = MEMORY_FILE.read_text().splitlines()
        return {
            "success": True,
            "content": memories
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def write_memory(content: str) -> Dict[str, Any]:
    """
    Append important information to memory log.
    
    Args:
        content: The important information to remember (should be concise)
        
    Returns:
        Dict indicating success or failure
    """
    try:
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory_entry = f"[{timestamp}] {content}\n"
        
        with MEMORY_FILE.open("a") as f:
            f.write(memory_entry)
            
        return {
            "success": True,
            "message": "Successfully stored memory"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def execute_command(command: str) -> Dict[str, Any]:
    """
    Execute a shell command and return the result.
    
    Args:
        command: The command to execute
        
    Returns:
        Dict containing stdout, stderr, and return code
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout for safety
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "error": "Command timed out after 30 seconds",
            "success": False
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def write_file(path: str, content: str) -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        path: Path to the file
        content: Content to write
        
    Returns:
        Dict indicating success or failure
    """
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return {
            "success": True,
            "message": f"Successfully wrote to {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def read_file(path: str) -> Dict[str, Any]:
    """
    Read content from a file.
    
    Args:
        path: Path to the file
        
    Returns:
        Dict containing file content or error
    """
    try:
        content = Path(path).read_text()
        return {
            "success": True,
            "content": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def list_directory(path: str = ".") -> Dict[str, Any]:
    """
    List contents of a directory.
    
    Args:
        path: Directory path to list
        
    Returns:
        Dict containing directory contents or error
    """
    try:
        dir_path = Path(path)
        contents = list(dir_path.iterdir())
        return {
            "success": True,
            "contents": [
                {
                    "name": str(item.name),
                    "type": "directory" if item.is_dir() else "file",
                    "path": str(item)
                }
                for item in contents
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
class Tool(TypedDict):
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable[..., Dict[str, Any]]

# List of available tools for the LLM agent
AVAILABLE_TOOLS: List[Tool] = [
    {
        "name": "execute_command",
        "function": execute_command,
        "description": "Execute a shell command and return the result",
        "parameters": {
            "command": "The command to execute"
        }
    },
    {
        "name": "write_file",
        "function": write_file,
        "description": "Write content to a file",
        "parameters": {
            "path": "Path to the file",
            "content": "Content to write to the file"
        }
    },
    {
        "name": "read_file",
        "function": read_file,
        "description": "Read content from a file",
        "parameters": {
            "path": "Path to the file"
        }
    },
    {
        "name": "list_directory",
        "function": list_directory,
        "description": "List contents of a directory",
        "parameters": {
            "path": "Directory path to list (optional, defaults to current directory)"
        }
    },
    {
        "name": "read_memory",
        "function": read_memory,
        "description": "Read the log of important information that has been remembered",
        "parameters": {}
    },
    {
        "name": "write_memory",
        "function": write_memory,
        "description": "Store a piece of important information in memory. Only store truly significant information and write it in a clear, concise manner. Do not store trivial details.",
        "parameters": {
            "content": "The important information to remember"
        }
    }
]

def get_tool_schemas() -> List[Dict[str, Any]]:
    """Convert tools to OpenAI function schema format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        param: {
                            "type": "string",
                            "description": desc
                        }
                        for param, desc in tool["parameters"].items()
                    },
                    "required": list(tool["parameters"].keys()) if tool["parameters"] else []
                }
            }
        }
        for tool in AVAILABLE_TOOLS
    ]