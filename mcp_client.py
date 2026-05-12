import asyncio
import sys
from mcp import ClientSession, ListToolsResult, StdioServerParameters
from mcp.client.stdio import stdio_client

# Shared server parameters
PARAMS = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])

async def get_tools_from_mcp():
    """Phase 1: Discovery - List all available tools."""
    async with stdio_client(server=PARAMS) as (read, write):
        try:
            async with ClientSession(read, write) as session:
                await session.initialize()
                response = await session.list_tools()
                print("\n--- Available Tools ---")
                for tool in response.tools:
                    print(f"-- {tool.name}: {tool.description}")
                return response.tools
        except Exception as e:
            print(f"Connection failed: {e}")

async def read_resource(resource_uri: str):
    """Phase 2: Context - Read a specific resource."""
    async with stdio_client(PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(f"\n--- Reading Resource: {resource_uri} ---")
            resource_content = await session.read_resource(resource_uri)
            for content in resource_content.contents:
                print(content.text)
            return resource_content

async def call_mcp_tool(tool_name: str, arguments: dict):
    """Phase 3: Execution - Call a tool with arguments."""
    async with stdio_client(PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(f"\n--- Calling Tool: {tool_name} ---")
            result = await session.call_tool(tool_name, arguments)
            text_content = result.content[0].text
            print(f"Result: {text_content}")
            return text_content

async def list_prompts():
    """List all available prompts from the MCP server."""
    params = StdioServerParameters(command=sys.executable, args=["currency_server.py"])

    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            print(f"Available prompts: {[p.name for p in prompts.prompts]}")

            return prompts.prompts
        

async def read_prompt(user_input: str = "How much is 50 GBP in euros?", prompt_name: str = "convert_currency_prompt") -> str:
    """Retrieve a prompt from the MCP server with user input."""
    params = StdioServerParameters(command=sys.executable, args=["currency_server.py"])

    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            # Retrieve the prompt with the user's input
            prompt = await session.get_prompt(prompt_name, arguments={"currency_request": user_input})
            print(prompt.messages[0].content.text)
            # Print the full prompt text (template + user request)
            text = prompt.messages[0].content.text
            print(text)
            return text


async def main():
    # Execute the full workflow
    await get_tools_from_mcp()
    await read_resource("file://currencies.txt")
    await call_mcp_tool("convert_currency", {"amount": 250.0, "from_currency": "USD", "to_currency": "EUR"})
    await list_prompts
    await read_prompt(user_input="How much is 50 GBP in euros?")

if __name__ == "__main__":
    asyncio.run(main())