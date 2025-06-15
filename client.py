#!/usr/bin/env python3
import asyncio
import json
import os
import sys
from typing import Optional
from contextlib import AsyncExitStack

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.model = os.getenv("MODEL_NAME", "gpt-4")

    async def connect_to_server(self, server_source: str):
        """连接到 MCP Server，可以是本地文件或 NPM 包名"""
        if server_source.endswith(".py") or server_source.endswith(".js"):
            command = "python" if server_source.endswith(".py") else "node"
            args = [server_source]
        else:
            command = "npx"
            args = ["-y", server_source]

        print(f"🔌 启动 MCP Server: {command} {' '.join(args)}")

        env = os.environ.copy()
        server_params = StdioServerParameters(command=command, args=args, env=env)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        tools = (await self.session.list_tools()).tools
        print("\n✅ 已连接到 MCP Server，可用工具:", [tool.name for tool in tools])


    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        response = await self.session.list_tools()
        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            } for tool in response.tools
        ]

        chat = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )

        reply = chat.choices[0].message
        tool_calls = reply.tool_calls or []
        final_text = []

        if reply.content:
            final_text.append(reply.content)
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except Exception as e:
                final_text.append(f"❌ 工具参数 JSON 解析失败: {e}")
                continue

            print(f"\n🛠️ 调用工具：{tool_name}，参数：{tool_args}")
            result = await self.session.call_tool(tool_name, tool_args)

            result_text = "\n".join(
                block.text for block in result.content if block.type == "text"
            )
            final_text.append(result_text)

        return "\n".join(final_text)

    async def chat_loop(self):
        print("\n💬 MCP 客户端启动。输入查询（quit 退出）:")
        while True:
            try:
                query = input("\n你：").strip()
                if query.lower() == "quit":
                    break
                reply = await self.process_query(query)
                print(f"🤖 {reply}")
            except Exception as e:
                print(f"❌ 错误：{e}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("❗ 用法: python client.py <server_script_path_or_npm_package>")
        sys.exit(1)
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
