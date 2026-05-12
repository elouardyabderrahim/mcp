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
                await session.initialize()[cite: 1, 3]
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
            await session.initialize()[cite: 1, 3]
            print(f"\n--- Reading Resource: {resource_uri} ---")
            resource_content = await session.read_resource(resource_uri)
            for content in resource_content.contents:
                print(content.text)
            return resource_content

async def call_mcp_tool(tool_name: str, arguments: dict):
    """Phase 3: Execution - Call a tool with arguments."""
    async with stdio_client(PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()[cite: 1, 3]
            print(f"\n--- Calling Tool: {tool_name} ---")
            result = await session.call_tool(tool_name, arguments)
            text_content = result.content[0].text
            print(f"Result: {text_content}")
            return text_content

async def main():
    # Execute the full workflow
    await get_tools_from_mcp()
    await read_resource("file://currencies.txt")
    await call_mcp_tool("convert_currency", {"amount": 250.0, "from_currency": "USD", "to_currency": "EUR"})

if __name__ == "__main__":
    asyncio.run(main())