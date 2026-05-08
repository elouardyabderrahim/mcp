![Core](attachments/screen%20for%20the%20resume%20video%20first%20one.png)

## 1. Core Architecture
MCP uses a structured three-tier model to separate the AI's reasoning from the technical execution of tools.

### The Three Components:

* **Host:** The primary application (e.g., Claude Desktop, Cursor, or a custom IDE) that the user interacts with.

* **Client:** A component within the Host that manages the connection, security, and protocol negotiation with the server.

* **Server:** A lightweight, specialized service that exposes specific data (Resources), logic (Tools), or context (Prompts) to the AI.
![Three Components](attachments/Pasted%20image%202020260508201308.png)


  ![Tool](attachments/Pasted%20image%2020260508201927.png)

## 2. Server Implementation (Python)

The **FastMCP** SDK provides a high-level abstraction for building servers quickly.

### Defining a Server and Tool:

Tools allow the LLM to perform actions, such as querying a database or interacting with a local API.
```python
from mcp.server.fastmcp import FastMCP
# 1. Initialize the FastMCP server instance
mcp = FastMCP("SystemManager")
# 2. Define a tool using the @mcp.tool decorator
@mcp.tool()
def get_system_info(category: str) -> str:
\"\"\"Provides system-specific metadata.\"\"\"

return f"Data for {category}"
```
  
![Tool](attachments/Pasted%20image%2020260508203545.png)

## 3. The Communication Layer: JSON-RPC
MCP relies on **JSON-RPC 2.0** for all messaging. This ensures that every request from the client and every response from the server follows a strict, predictable format.
 
![Communication Layer](attachments/Pasted%20image%2020260508214323.png)
## 4. Transport Mechanisms
To move JSON-RPC messages between the Client and Server, MCP defines two primary "pipes" or transport layers:
### A. Standard I/O (stdio)
Used primarily for local integrations where the server runs as a subprocess.
* **No Network Configuration:** Ideal for local development and desktop apps.
* **Subprocess Lifecycle:** The server starts when the client connects and terminates when the client exits.

![Standard I/O](attachments/Pasted%20image%2020260508214353.png)

  ### B. Streamable HTTP (SSE)

Used for remote or networked servers.
* **Server-Sent Events (SSE):** The server sends events to the client.

* **HTTP POST:** The client sends commands back to the server.

* **Scalability:** Allows the AI to connect to tools hosted in the cloud.
![Streamable HTTP](attachments/Pasted%20image%2020260508214434.png)