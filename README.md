# 🤖 Jarbas AI — Virtual Telegram Assistant

An AI-powered virtual assistant integrated with Telegram, capable of reasoning, tool usage, and knowledge retrieval using modern LLM architectures.

---

## ✨ Features

* 🤖 Multi-LLM support (OpenAI + DeepSeek + Anthropic-ready)
* 🔍 Real-time web search (Tavily)
* 🧠 RAG (Retrieval-Augmented Generation)
* 🧮 Tool usage (calculator, datetime, etc.)
* 🧠 Context-aware responses with memory per conversation
* 🧩 Modular architecture using LangGraph
* 📊 Structured logging with Loguru
* 🎭 Adaptive tone (based on message classification)

---

## 🧠 Architecture Overview

```
User (Telegram)
↓
Telegram Service (Telethon)
↓
LangGraph Agent
├── Classifier Node
├── Answer Node
└── Tool Routing (Edges)
  ├── Web Search
  ├── RAG
  ├── Calculator
  └── Datetime
↓
Response
```

---

## ⚙️ Tech Stack

### Language

* Python 3.14.3

### Core Libraries

* LangChain ecosystem:

  * langchain
  * langchain-core
  * langchain-community
  * langgraph
  * langchain-openai
  * langchain-anthropic
  * langchain-deepseek
  * langchain-text-splitters
  * langchain-huggingface
  * langchain-tavily

* Embeddings & Vector Store:

  * sentence-transformers
  * faiss-cpu

* Integrations:

  * telethon (Telegram client)

* Utilities:

  * numexpr (safe math evaluation)
  * pymupdf (PDF parsing)
  * babel + pytz (datetime formatting)
  * markdown-it-py (markdown parsing)
  * python-dotenv (env management)
  * loguru (logging)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo>
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup environment variables

Copy the example file:

`cp .env.example .env`

Fill in:

```.env
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
ANTHROPIC_API_KEY=

TAVILY_API_KEY=

API_ID=
API_HASH=

LOG_DIR=logs
DEBUG=true
```

---

### 4. Run the project

```bash
python main.py
```

---

## 📁 Project Structure

### Root

* main.py
  Entry point. Loads environment variables and starts the Telegram service.

* requirements.txt
  Project dependencies.

* .env.example
  Template for environment configuration.

---

### src/

Main application code.

---

## 🔧 Core Modules

### core/logger.py

Configures structured logging using Loguru:

* Console (colorized)
* JSON logs (for analysis)
* Rotating log files

---

### services/telegram.py

Handles Telegram integration using Telethon:

* Listens to private messages
* Applies trigger logic
* Sends messages to the agent
* Simulates human-like delay

---

## 🤖 Agent (LangGraph)

### agent/graph.py

Defines the agent workflow using LangGraph:

* Node orchestration
* Memory (InMemorySaver)
* Execution flow

---

### agent/state.py

Defines the AgentState:

* message
* messages
* classification
* response
* tool usage tracking

---

### agent/edges.py

Controls tool execution:

* Limits usage of expensive tools (web search, RAG)
* Prevents excessive API usage
* Routes tool calls dynamically

---

### Nodes

#### classifier.py

Classifies user input:

* intent
* tone
* style
* confidence

---

#### answer.py

Main reasoning node:

* Decides when to use tools
* Generates final response

---

#### schemas.py

Pydantic schemas for structured outputs.

---

## 🧰 Tools

### Web Search

tools/websearch.py

* Uses Tavily API
* Fast real-time search

---

### Calculator

tools/calculator.py

* Safe evaluation using numexpr
* Supports complex expressions

---

### Datetime

tools/datetime.py

* Timezone-aware
* Localized formatting (pt-BR)

---

### RAG System (tools/rag/)

#### loader.py

Loads documents from src/data

#### splitter.py

Splits markdown using MarkdownTextSplitter

#### vecstore.py

Creates FAISS vector store using:

* HuggingFace embeddings (all-MiniLM-L6-v2)

#### tool.py

Builds retriever tool for the agent

---

## 📄 Data Processing

### data_processing/process_resume.py

Pipeline:

1. Extract text from PDF (PyMuPDF)
2. Send to LLM
3. Convert into structured Markdown
4. Store for RAG usage

---

## 📂 Data

Located in src/data/

* resume.pdf → raw input
* resume.md → processed for RAG
* extra.md → additional contextual data

---

## 🧠 Design Decisions

### Multi-Model Strategy

The system supports multiple LLM providers and can be extended to dynamically route between them.

---

### Tool-Oriented Architecture

Instead of relying only on LLM knowledge, the agent:

* fetches real-time data
* performs calculations
* retrieves structured knowledge

---

### Controlled Tool Usage

Expensive tools are rate-limited per interaction to:

* reduce cost
* improve stability

---

### RAG for Personal Context

Custom knowledge base allows the agent to:

* answer questions about the system owner
* simulate a virtual assistant in real scenarios

---

## 🔮 Future Improvements

* Long-term memory persistence
* Autonomous task execution
* Multi-agent personas
* Streaming responses
* Observability / tracing

---

## 📌 Final Notes

This project explores how modern AI systems can be designed beyond simple prompts — focusing on orchestration, tooling, and real-world integration.

Instead of treating LLMs as isolated components, the system leverages them as part of a broader architecture capable of reasoning, acting, and adapting to different contexts.

## 🎥 Demo

[▶️ Watch the Test Here](https://drive.google.com/file/d/1eIhc6EvsRozMnLkqibB361EVEAeL62rr/view?usp=sharing)