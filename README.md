# Guini MCP Server

A Model Context Protocol (MCP) server implementation for Guini API integration with LLMs.



## Overview

This project implements an MCP server that enables LLMs to interact with the Guini API through a set of defined tools. The server facilitates operations like listing partners and potentially other functionality through a standardized interface.

The `main.py` file serves as a client application that interacts with the MCP server. It performs the following functions:

1. **Client Setup**: Creates a Gemini API client and configures the connection to the MCP server.
2. **Agent Loop Implementation**: Implements an agent loop that:
   - Retrieves available tools from the MCP server
   - Sends user prompts to the Gemini LLM model
   - Processes tool calling requests from the LLM
   - Executes tools through the MCP server
   - Handles response formatting
3. **Example Usage**: Contains a sample implementation that lists partners from a specific location (Holon).
4. **JSON Response Handling**: Formats the final LLM response as structured JSON data.

The client application demonstrates how to integrate the Gemini API with the MCP server, creating a seamless experience where the LLM can interact with external tools through standardized interfaces.


## Requirements

- Python 3.13
- uv package manager

## Installation and Setup

### Using uv (Recommended)

This project uses [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

1. Install uv if not already installed:
   ```bash
   pip install uv
   # OR
   curl --proto '=https' --tlsv1.2 -sSf https://sh.uv.global | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/guini_mcp.git
   cd guini_mcp
   ```

3. Create and activate a virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .\.venv\Scripts\activate  # On Windows
   ```

4. Install dependencies using uv:
   ```bash
   uv pip install -e .
   ```

5. Set up environment variables:
   Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Alternative: Using pip

If you prefer not to use uv:

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# OR
.\.venv\Scripts\activate  # On Windows
pip install -e .
```


## How to Run the Project

```bash
python main.py
```

## Development

### Adding New Tools

To add a new tool to the MCP server:

1. Open `guini_mcp_server.py`
2. Add a new function decorated with `@mcp.tool()`
3. Implement the tool functionality

Example:
```python
@mcp.tool()
async def new_tool_name(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Description of what the tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dict containing tool response
    """
    # Implementation here
```

## uv Cheatsheet

Here are some common commands when working with uv:

- Create a virtual environment: `uv venv`
- Activate virtual environment: `source .venv/bin/activate` (Unix/macOS) or `.\.venv\Scripts\activate` (Windows)
- Install dependencies: `uv pip install -e .`
- Add a new package: `uv pip install package_name`
- Update lockfile: `uv pip compile pyproject.toml -o uv.lock`
- List installed packages: `uv pip list`
- Update all packages: `uv pip install --upgrade -e .`
- Install a specific version: `uv pip install package_name==1.2.3`

### Why uv?

uv offers several advantages over traditional Python package management:

- **Speed**: uv is significantly faster than pip for installing packages
- **Reliability**: Deterministic builds with lockfiles
- **Compatibility**: Works with existing Python projects
- **Isolation**: Better environment management

## Troubleshooting

- If you encounter issues with permissions when installing uv, try using `pip install --user uv`.
- Make sure your `.env` file is properly configured with your API credentials.
- Check that Python 3.13 is properly installed and selected as your interpreter.
- If you see "command not found" after installing uv, you may need to add it to your PATH.

## Working with the uv.lock File

The `uv.lock` file in this repository ensures consistent dependency versions across all development environments:

- Never edit this file manually
- Commit this file to version control
- To update dependencies while respecting the lock file: `uv pip install -e . --resolution=highest`