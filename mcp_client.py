import asyncio
import sys

from mcp import ClientSession, ListToolsResult, StdioServerParameters
from mcp.client.stdio import stdio_client


async def get_tools_from_mcp():
    # define the server params 
    params= StdioServerParameters(command=sys.executable,args=["time_zone_server.py"])
    tools_list =[]
    #Connecng with the Mcp Server
    async with stdio_client(server=params) as (read,write):
        # Creating the  session\
        try:
            async with ClientSession(read_stream=read,write_stream=write) as session:
                #itialise the session 
                await session.initialize()
                #List the tools the server provides
                response: ListToolsResult = await session.list_tools()

                print("Connected to the Server !")
                print("Available tools: ")
                for tool in response.tools:
                    print (f"-- {tool.name}: {tool.description}")
                tools_list = response.tools
        except Exception as e:
            print(f"no connection estavleched: {e} ")

    return response.tools

asyncio.run(get_tools_from_mcp())
