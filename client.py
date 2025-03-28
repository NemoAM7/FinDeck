import asyncio
import sys
import json
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack
import re
import os

import groq  # Import the entire module instead of specific class

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GroqClient:
    def __init__(self, model_name: str = "llama-3.2-90b-vision-preview"):
        """Initialize Groq client with API key and model."""
        self.model_name = model_name
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = groq.Client(api_key=api_key)  # Use Client instead of Groq
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        print(self.tools)
        print("\nConnected to server with tools:", [tool.name for tool in self.tools])

    async def generate_response(self, messages: List[Dict[str, Any]]) -> str:
        """Generate a response using Groq
        
        Args:
            messages: List of message dictionaries
        """
        # Format messages for Groq
        prompt = """You are a helpful assistant that can use tools to help users. When you need to use a tool, format your response like this:
[TOOL_CALL]tool_name:{"arg1": value1, "arg2": value2}[/TOOL_CALL]

Available tools:
"""
        
        # Add tool descriptions based on what's available from the server
        tool_names = [tool.name for tool in self.tools]
        
        if "calculate" in tool_names:
            prompt += """- calculate: Performs basic arithmetic operations
  Arguments:
    - operation: "add", "subtract", "multiply", or "divide"
    - a: First number
    - b: Second number
  Example: [TOOL_CALL]calculate:{"operation": "add", "a": 5, "b": 3}[/TOOL_CALL]
"""

        if "list_channels" in tool_names:
            prompt += """- list_channels: Lists all available Discord channels and their IDs
  No arguments needed
  Example: [TOOL_CALL]list_channels:{}[/TOOL_CALL]
"""

        if "send_message" in tool_names:
            prompt += """- send_message: Sends a message to a specific Discord channel
  Arguments:
    - channel_id: The numeric ID of the channel to send to
    - message: The text message to send
  Example: [TOOL_CALL]send_message:{"channel_id": 123456789, "message": "Hello from the assistant!"}[/TOOL_CALL]
"""

        # Add data exploration tools
        if "load_csv" in tool_names:
            prompt += """- load_csv: Loads a CSV file into a pandas DataFrame
  Arguments:
    - csv_path: Path to the CSV file
    - df_name: (optional) Name for the DataFrame
  Example: [TOOL_CALL]load_csv:{"csv_path": "data/housing.csv", "df_name": "housing_data"}[/TOOL_CALL]
"""

        if "run_script" in tool_names:
            prompt += """- run_script: Executes a Python script with access to loaded DataFrames
  Arguments:
    - script: The Python script to execute
  Example: [TOOL_CALL]run_script:{"script": "import matplotlib.pyplot as plt\\nplt.figure()\\ndf_1.plot()\\nplt.savefig('plot.png')\\nprint('Plot saved!')"}}[/TOOL_CALL]
"""

        if "get_dataframe_info" in tool_names:
            prompt += """- get_dataframe_info: Gets detailed information about a loaded DataFrame
  Arguments:
    - df_name: Name of the DataFrame
  Example: [TOOL_CALL]get_dataframe_info:{"df_name": "df_1"}[/TOOL_CALL]
"""

        if "list_dataframes" in tool_names:
            prompt += """- list_dataframes: Lists all loaded DataFrames
  No arguments needed
  Example: [TOOL_CALL]list_dataframes:{}[/TOOL_CALL]
"""

        prompt += "\nWhen asked about data analysis, ALWAYS use the appropriate data exploration tool.\n\n"
        prompt += "Now, let's handle the user's query:\n"

        # Add user messages to prompt
        formatted_messages = [{"role": "system", "content": prompt}]
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, list):
                content = " ".join(item.get("text", "") for item in content if item.get("type") == "text")
            formatted_messages.append({"role": role, "content": content})

        # Make API call
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                stream=False
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return f"Error: {str(e)}"

    async def process_query(self, query: str) -> str:
        """Process a query using Groq and available tools"""
        messages = [{"role": "user", "content": query}]
        
        # Get initial response from Groq
        response = await self.generate_response(messages)
        
        # Check if response contains tool calls with better regex pattern
        tool_call_pattern = r'\[TOOL_CALL\](.*?):(.*?)\[/TOOL_CALL\]'
        tool_calls = re.findall(tool_call_pattern, response)
        
        if tool_calls:
            results = []
            for tool_name, tool_args_str in tool_calls:
                try:
                    # Clean and parse tool arguments
                    tool_args = json.loads(tool_args_str.strip())
                    
                    # Execute tool call
                    print(f"\nCalling tool: {tool_name} with args: {tool_args}")
                    
                    # Handle streaming response
                    current_result = ""
                    async for result in self.session.call_tool(tool_name, tool_args):
                        if isinstance(result.content, list):
                            for content in result.content:
                                if content.type == "text":
                                    current_result += content.text
                                    print(content.text, end="", flush=True)
                    
                    print()  # New line after streaming
                    
                    # Add the result
                    results.append(f"[Tool Result: {tool_name}] {current_result}")
                    
                    # Add tool result to messages
                    messages.append({"role": "assistant", "content": f"I'll use the {tool_name} tool."})
                    messages.append({
                        "role": "user",
                        "content": f"Tool result: {current_result}"
                    })
                except Exception as e:
                    error_msg = f"Error executing tool {tool_name}: {str(e)}"
                    print(error_msg)
                    results.append(error_msg)
                    messages.append({
                        "role": "user",
                        "content": f"Error: {error_msg}"
                    })
            
            # Get final response with all tool results
            final_response = await self.generate_response(messages)
            return f"{response}\n\n{''.join(results)}\n\n{final_response}"
        
        return response

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break
                
                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")
                import traceback
                traceback.print_exc()

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = GroqClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 