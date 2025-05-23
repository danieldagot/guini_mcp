from typing import List
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from dotenv import load_dotenv 
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "gemini-2.5-pro-exp-03-25"

PROMPT = "list all partners from holon"

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["guini_mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def agent_loop(prompt: str, client: genai.Client, session: ClientSession):
    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    # Initialize the connection
    await session.initialize()
    
    # --- 1. Get Tools from Session and convert to Gemini Tool objects ---
    mcp_tools = await session.list_tools()
    tools = types.Tool(function_declarations=[
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema,
        }
        for tool in mcp_tools.tools
    ])
    print(f"Found {len(mcp_tools.tools)} tools: {[tool.name for tool in mcp_tools.tools]}")
    print(f"Tools: {tools}")


    # --- 2. Initial Request with user prompt and function declarations ---
    response = await client.aio.models.generate_content(
        model=model,  # Or your preferred model supporting function calling
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0,
            tools=[tools],

        ),  # Example other config
    )
    
    # --- 3. Append initial response to contents ---
    contents.append(response.candidates[0].content)

    # --- 4. Tool Calling Loop ---            
    turn_count = 0
    max_tool_turns = 5
    while response.function_calls and turn_count < max_tool_turns:
        turn_count += 1
        tool_response_parts: List[types.Part] = []
        print(f"Tool calling loop iteration {turn_count}, function calls: {response.function_calls}")

        # --- 4.1 Process all function calls in order and return in this turn ---
        for fc_part in response.function_calls:
            tool_name = fc_part.name
            args = fc_part.args or {}  # Ensure args is a dict
            print(f"Attempting to call MCP tool: '{tool_name}' with args: {args}")

            tool_response: dict
            try:
                # Call the session's tool executor
                tool_result = await session.call_tool(tool_name, args)
                print(f"MCP tool '{tool_name}' executed successfully.")
                if tool_result.isError:
                    tool_response = {"error": tool_result.content[0].text}
                else:
                    tool_response = {"result": tool_result.content[0].text}
            except Exception as e:
                tool_response = {"error":  f"Tool execution failed: {type(e).__name__}: {e}"}
            
            # Prepare FunctionResponse Part
            tool_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name, response=tool_response
                )
            )

        # --- 4.2 Add the tool response(s) to history ---
        contents.append(types.Content(role="user", parts=tool_response_parts))
        print(f"Added {len(tool_response_parts)} tool response parts to history.")

        # --- 4.3 Make the next call to the model with updated history ---
        print("Making subsequent API call with tool responses...")
        response = await client.aio.models.generate_content(
            model=model,
            contents=contents,  # Send updated history
            config=types.GenerateContentConfig(
                temperature=0,
                tools=[tools],
            ),  # Keep sending same config
        )
        contents.append(response.candidates[0].content)

    if turn_count >= max_tool_turns and response.function_calls:
        print(f"Maximum tool turns ({max_tool_turns}) reached. Exiting loop.")
    response_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "partnerUsername": {"type": "STRING"},
            "categories": {"type": "ARRAY", "items": {"type": "STRING"}},
            "businessCity": {"type": "STRING"},
            
        },
        "required": ["partnerUsername", "categories", "businessCity"],
    },
}
    response = await client.aio.models.generate_content(
            model=model,
            contents=contents,  # Send updated history
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),  # Keep sending same config
        )
    print("MCP tool calling loop finished. Returning final response.")
    # --- 5. Return Final Response ---
    return response
        
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read,
            write,
        ) as session:
            # Test prompt
            prompt = PROMPT
            print(f"Running agent loop with prompt: {prompt}")
            # Run agent loop
            res = await agent_loop(prompt, client, session)
            return res

# Proper way to run async functions
if __name__ == "__main__":
    import asyncio
    
    result = asyncio.run(run())
    print(result.text)
