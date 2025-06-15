# 🕵️ MCP Client CLI

基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的命令行客户端，支持通过 Claude/OpenAI 等大模型调用 `sqlmap`、`xscan` 等漏洞检测工具。

## ✨ 特性

- ✅ 支持从本地脚本或 npm 包启动 MCP Server
- ✅ 与 Claude/OpenAI/DeepSeek 语言模型交互
- ✅ 多轮对话 + 自动工具调用
- ✅ 自动处理工具返回值，结构清晰

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt