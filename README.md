# 🕵️ Pluto's Mcp Client

基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的命令行客户端，集成 OpenAI 的等大语言模型（**注意不同大模型 API 之间存在差异，本项目支持的是 OpenAI**），通过自然语言驱动 `sqlmap`、`xscan`、`githack` 等工具完成安全测试、漏洞扫描任务，并自动生成 Markdown 报告。

------

## ✨ 特性 Features

- ✅ 支持 Claude / OpenAI / DeepSeek 模型（兼容 OpenAI SDK）
- ✅ 启动本地脚本或 NPM 包形式的 MCP Server（支持多个）
- ✅ 自动识别并调用工具，参数推理、补全、验证
- ✅ 工具调用后 AI 自动继续对话，支持多轮上下文
- ✅ 自动生成 Markdown 漏洞扫描报告（按时间命名）
- ✅ 工具路径、模型参数通过 `.env` 配置，支持 `.py`、`.exe` 等

------

## 🚀 快速开始 Quick Start

### 1️⃣ 安装依赖（推荐使用 venv 或 conda 等虚拟环境进行包管理）

```bash
pip install -r requirements.txt
```

> 要求 Python 3.8+

------

### 2️⃣ 创建 `.env` 文件

在项目根目录创建 `.env`，配置模型 API 与工具路径：

```txt
# 模型配置
OPENAI_API_KEY = your-openai-or-deepseek-key
OPENAI_BASE_URL = https://api.deepseek.com/v1
MODEL_NAME = deepseek-chat

# 工具路径配置(具体是 .py/.exe/... 文件由相应 mcp-server 规定)
PYTHON_PATH = python
GITHACK_PATH = /absolute/path/to/githack.py
SQLMAP_PATH = /absolute/path/to/sqlmap.exe
XSCAN_PATH = /absolute/path/to/xscan.exe
```

------

### 3️⃣ 设置 `mcp_server.json` 文件

```json
# 设置 mcp-server 的路径，支持本地文件/远程npm包，示例：
[
  "pluto-sqlmap-mcp",
  "pluto-xscan-mcp",
  "/absolute/path/to/githack.py"
]
```

### 4️⃣ 启动 MCP 客户端

```bash
python client.py mcp_server.json
```

------

### 5️⃣自然语言交互

进入对话后直接输入自然语言：

```text
你：请测试 https://example.com/?id=1 是否存在 SQL 注入并生成报告
🤖 自动调用 do-sqlmap 工具，分析响应并生成总结
📄 报告已保存：reports/report_20250616_230112.md
```

------

## 📂 报告输出路径

所有生成报告保存在：

```
./reports/report_YYYYMMDD_HHMMSS.md
```

> 使用 Markdown 格式输出，可使用 VSCode / Typora / Obsidian 查看。

---

## 🧪 报告内容示例（Markdown）

见 `reports/report_20250616_232349.md`

---

## 🛠 支持的 MCP 工具

| 工具名         | 功能             | 来源        | 类型         |
| -------------- | ---------------- | ----------- | ------------ |
| `do-githack`   | Git 泄露检测     | NPM 包      | Python 脚本  |
| `do-sqlmap`    | SQL 注入检测     | NPM 包      | 可执行文件   |
| `do-xss-xscan` | XSS / 端口扫描   | NPM 包      | 可执行文件   |
| ...            | 可自定义扩展工具 | 本地/NPM 包 | 任意语言支持 |

---

## ⚙️ 环境变量说明（`.env`）

| 变量名            | 描述                                     |
| ----------------- | ---------------------------------------- |
| `OPENAI_API_KEY`  | OpenAI 或 DeepSeek API Key               |
| `OPENAI_BASE_URL` | 模型 API 接口地址                        |
| `MODEL_NAME`      | 模型名称，如 `gpt-4`, `deepseek-chat` 等 |
| `PYTHON_PATH`     | Python 解释器路径（如 `python3`）        |
| `GITHACK_PATH`    | githack.py 脚本绝对路径                  |
| `SQLMAP_PATH`     | sqlmap.exe 绝对路径                      |
| `XSCAN_PATH`      | xscan.exe 绝对路径                       |
| ...               | 其他工具路径                             |

---

## 🧩 TODO

- [ ] 支持导出 PDF / HTML 报告
- [ ] 报告增加风险等级与修复建议结构
- [ ] 工具调用失败的错误日志自动汇总
- [ ] Web UI 界面化展示历史记录
