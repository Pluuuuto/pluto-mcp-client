import asyncio
import json
import os
import sys
import datetime
from typing import List
from contextlib import AsyncExitStack
from dotenv import load_dotenv

from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

class MCPClient:
    def __init__(self):
        self.sessions: List[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        self.chat_history = []
        self.report_buffer = []  # ⬅ 收集用于 Markdown 报告
        self.openai = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("MODEL_NAME", "deepseek-chat")

    async def connect_to_servers(self, config_path: str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件未找到: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            servers = json.load(f)

        for server_source in servers:
            if server_source.endswith(".py"):
                command = "python"
                args = [server_source]
            elif server_source.endswith(".js"):
                command = "node"
                args = [server_source]
            else:
                command = "npx"
                args = ["-y", server_source]

            print(f"\n🔌 启动 MCP Server: {command} {' '.join(args)}")
            server_params = StdioServerParameters(command=command, args=args, env=os.environ.copy())
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            stdio, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()
            self.sessions.append(session)

        print(f"\n✅ 已连接 {len(self.sessions)} 个 MCP Server")

    async def collect_all_tools(self):
        tools = []
        for session in self.sessions:
            response = await session.list_tools()
            tools += [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                for tool in response.tools
            ]
        return tools

    async def call_tool(self, tool_name: str, args: dict) -> str:
        for session in self.sessions:
            response = await session.list_tools()
            if any(tool.name == tool_name for tool in response.tools):
                print(f"[DEBUG] 正在调用 MCP 工具: {tool_name} 参数: {args}")
                result = await session.call_tool(tool_name, args)
                result_text = "\n".join(block.text for block in result.content if block.type == "text")
                return result_text
        return f"❌ 工具 {tool_name} 未找到"

    def save_markdown_report(self):
        folder = os.path.abspath("reports")
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.md"
        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# 漏洞扫描报告\n\n")
                for section in self.report_buffer:
                    f.write(section + "\n\n")
            print(f"\n📄 Markdown 报告已保存:\n{filepath}")
        except Exception as e:
            print(f"\n❌ 报告保存失败: {e}")

    async def process_query(self, query: str) -> str:
        self.chat_history.append({"role": "user", "content": query})
        tools = await self.collect_all_tools()

        chat = await self.openai.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            tools=tools,
            tool_choice="auto"
        )

        reply = chat.choices[0].message
        self.chat_history.append(reply.model_dump(exclude_unset=True))

        final_texts = []
        if reply.content:
            final_texts.append(reply.content)

        tool_calls = reply.tool_calls or []
        print(f"[DEBUG] AI tool_calls: {tool_calls}")

        if not tool_calls:
            print("[INFO] AI 未实际触发工具调用，跳过工具执行阶段。")
            if final_texts:
                self.report_buffer.append(f"## 最终总结\n{final_texts[-1]}")
                self.save_markdown_report()
            return "\n".join(final_texts)

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except Exception as e:
                err = f"❌ 工具参数 JSON 解析失败: {e}"
                final_texts.append(err)
                continue

            result_text = await self.call_tool(tool_name, tool_args)

            self.chat_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": result_text
            })

            # 收集工具调用结果为 Markdown 块
            section = (
                f"## 工具：{tool_name}\n"
                f"**参数：**\n```json\n{json.dumps(tool_args, indent=2, ensure_ascii=False)}\n```\n"
                f"**结果：**\n```\n{result_text}\n```"
            )
            self.report_buffer.append(section)

        # 工具调用后继续与 AI 对话
        chat = await self.openai.chat.completions.create(
            model=self.model,
            messages=self.chat_history
        )
        next_reply = chat.choices[0].message
        self.chat_history.append(next_reply.model_dump(exclude_unset=True))

        if next_reply.content:
            final_texts.append(next_reply.content)
            self.report_buffer.append(f"## 最终总结\n{next_reply.content}")

        # 保存 Markdown 报告
        self.save_markdown_report()

        return "\n".join(final_texts)

    async def chat_loop(self):
        print("\n💬 DeepSeek + MCP 客户端已启动，输入你的问题 (输入 'quit' 退出):")
        while True:
            try:
                query = input("\n你：").strip()
                if query.lower() == "quit":
                    break
                reply = await self.process_query(query)
                print(f"\n🤖 {reply}")
            except Exception as e:
                print(f"\n❌ 错误: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    client = MCPClient()
    try:
        await client.connect_to_servers("mcp_server.json")
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())