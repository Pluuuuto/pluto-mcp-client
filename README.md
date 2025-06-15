# 🕵️ MCP Client CLI

基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的命令行客户端，支持通过 Claude、OpenAI、DeepSeek 等大模型与工具（如 `sqlmap`、`xscan`、`githack` 等）交互，完成漏洞扫描、安全测试任务。

---

## ✨ 特性 Features

* ✅ 启动本地脚本或远程 NPM 包形式的 MCP Server
* ✅ 支持与 Claude / OpenAI / DeepSeek 等多种大语言模型（LLM）交互
* ✅ 自动调用工具（如 `sqlmap`、`xscan` 等）并处理响应
* ✅ 支持多轮对话，自动参数补全、自动工具推理
* ✅ 工具输出结构化显示，适合自动化调用链

---

## 🚀 快速开始 Quick Start

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

> ✅ 要求 Python 3.8+

---

### 2️⃣ 配置 `.env` 文件

在项目根目录创建 `.env` 文件，示例：

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
```

如需使用 Claude / DeepSeek 等模型，请设置对应的 API 地址与 Key。

---

### 3️⃣ 启动 MCP Server + 交互聊天

```bash
# 启动本地脚本（如封装好的 githack.js）
python client.py ./index.js

# 或启动远程 NPM 包（如 sqlmap）
python client.py pluto-sqlmap-mcp
```

运行后你将进入聊天界面：

```text
💬 MCP 客户端启动。输入查询（quit 退出）:

你：帮我测试 http://target.com/.git 是否存在泄露
🤖 （大模型自动调用 do-githack 工具并返回结果）
```

---

## ⚙️ 环境变量说明

| 变量名               | 说明                                          |
| ----------------- | ------------------------------------------- |
| `OPENAI_API_KEY`  | OpenAI / Claude / DeepSeek 等 LLM 的 API Key  |
| `OPENAI_BASE_URL` | 接口地址，OpenAI 默认为 `https://api.openai.com/v1` |
| `MODEL_NAME`      | 模型名称，如 `gpt-4`、`gpt-3.5-turbo`、`gpt-4o` 等   |
| `GITHACK_PATH`    | GitHack 工具脚本路径（绝对路径）                        |
| `PYTHON_PATH`     | Python 解释器路径，默认 `python`                    |

你可以临时设置，也可以写入 `.env` 文件统一管理。

---

## ⚠️ 使用注意事项

### 1. MCP 工具路径依赖环境变量传入

* 如 GitHack 等脚本类工具，需通过 `GITHACK_PATH` 设置为绝对路径
* 示例（Windows）：

  ```cmd
  set GITHACK_PATH=D:\Tools\githack.py
  python client.py index.js
  ```

### 2. 路径中请避免中文 / 空格

* 推荐放在 `D:\Tools\xxx.py` 这类纯英文路径下

### 3. `client.py` 已支持环境变量显式传入

* 所有环境变量会自动传给 MCP Server（不需修改服务端代码）

### 4. 所有远程工具应统一通过 `npx -y mcp-server-name` 调用

* 例如：

  ```bash
  python client.py pluto-sqlmap-mcp
  ```

---

## 🧪 测试工具建议

你可以先测试 `githack.py` 等工具是否能被 MCP 正常调用：

```python
# githack.py 示例
import sys
print("✅ GitHack 启动成功")
print("Target URL:", sys.argv[1])
```

放在项目根目录，通过 `.env` 设置路径，然后运行即可。

---

## 📦 已适配的 MCP 工具列表（可扩展）

| 工具名          | 功能        | 来源方式  |
| ------------ | --------- | ----- |
| `do-sqlmap`  | SQL 注入测试  | NPM 包 |
| `do-xscan`   | 端口/Web扫描  | NPM 包 |
| `do-githack` | .git 泄露检测 | 本地脚本  |

欢迎自定义封装自己的 MCP 工具，基于 `@modelcontextprotocol/sdk` 开发。

---

## 📂 项目结构说明

```bash
client.py         # MCP 客户端主程序
index.js          # MCP Server 示例（如 githack 封装）
githack.py        # 本地测试脚本（模拟 MCP 工具）
.env              # 环境变量配置
requirements.txt  # Python 依赖
```

---

## 🤝 贡献 & 扩展建议

* ✅ 封装更多安全工具为 MCP Server（如 `whatweb`、`nmap`）
* ✅ 支持自定义提示词模板
* ✅ 接入更多 LLM 平台（DeepSeek、Claude、ZhipuAI 等）
