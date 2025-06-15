## 🕵️ MCP Client CLI（已更新）

基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的命令行客户端，支持通过 Claude、OpenAI、DeepSeek 等大模型与工具（如 `sqlmap.exe`、`xscan`、`githack.py` 等）交互，完成漏洞扫描、安全测试任务。

------

## ✨ 特性 Features

- ✅ 启动本地脚本或 NPM 包形式的 MCP Server
- ✅ 支持 Claude / OpenAI / DeepSeek 等大语言模型
- ✅ 自动调用工具（如 `sqlmap`、`xscan` 等）并解析返回值
- ✅ 支持多轮对话 + 参数补全 + 工具推理
- ✅ 工具路径通过 `.env` 配置，支持 `.py`、`.exe` 等

------

## 🚀 快速开始 Quick Start

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

> 要求 Python 3.8+

------

### 2️⃣ 创建 `.env` 文件

在项目根目录创建 `.env` 文件，配置模型和工具路径：

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4

# 工具路径配置
GITHACK_PATH=D:/Tools/githack.py
PYTHON_PATH=python

SQLMAP_PATH=D:/Tools/sqlmap/sqlmap.exe
XSCAN_PATH=D:/Tools/xscan/xscan.exe
```

------

### 3️⃣ 启动 MCP Server 并交互测试

```bash
# 启动本地 MCP Server 脚本
python client.py ./build/index.js

# 或启动已发布的 NPM 包 MCP Server（如 sqlmap）
python client.py pluto-sqlmap-mcp
```

进入后直接提问：

```ruby
你：请测试 https://xxx.com/?id=1 是否存在 SQL 注入
🤖 自动调用 do-sqlmap 工具并返回检测结果
```

------

## 🛠 支持的 MCP 工具

| 工具名         | 功能描述       | 来源   | 运行方式       |
| -------------- | -------------- | ------ | -------------- |
| `do-githack`   | Git 泄露检测   | NPM 包 | Python + `.py` |
| `do-sqlmap`    | SQL 注入检测   | NPM 包 | 可执行 `.exe`  |
| `do-xss-xscan` | XSS / 端口扫描 | NPM 包 | 可执行 `.exe`  |
| ...            | ...            | ...    | ...            |

------

## ⚙️ 环境变量说明（`.env`）

| 变量名            | 描述                              |
| ----------------- | --------------------------------- |
| `OPENAI_API_KEY`  | OpenAI / Claude 的 API Key        |
| `OPENAI_BASE_URL` | 模型 API 接口地址（默认 OpenAI）  |
| `MODEL_NAME`      | 模型名称，如 `gpt-4`, `gpt-4o` 等 |
| `GITHACK_PATH`    | githack.py 的路径（绝对路径）     |
| `PYTHON_PATH`     | Python 解释器（如 `python3`）     |
| `SQLMAP_PATH`     | `sqlmap.exe` 的路径（绝对路径）   |
| `XSCAN_PATH`      | `xscan.exe` 的路径（绝对路径）    |
| ...               | ...                               |