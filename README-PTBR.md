Aqui está a tradução do seu README para português, mantendo os termos técnicos, nomes de bibliotecas e jargões de desenvolvimento em inglês, conforme solicitado.

***

# 🤖 Jarbas AI — Assistente Virtual para Telegram

Um assistente virtual alimentado por IA, integrado ao Telegram, capaz de raciocínio, uso de ferramentas e recuperação de conhecimento utilizando arquiteturas modernas de LLM.

---

## ✨ Funcionalidades

* 🤖 Suporte a múltiplos LLMs (OpenAI + DeepSeek + pronto para Anthropic)
* 🔍 Busca na web em tempo real (Tavily)
* 🧠 RAG (Retrieval-Augmented Generation)
* 🧮 Uso de ferramentas (calculadora, data/hora, etc.)
* 🧠 Respostas conscientes do contexto com memória por conversa
* 🧩 Arquitetura modular usando LangGraph
* 📊 Logging estruturado com Loguru
* 🎭 Tom adaptativo (baseado na classificação da mensagem)

---

## 🧠 Visão Geral da Arquitetura

```
Usuário (Telegram)
↓
Serviço Telegram (Telethon)
↓
Agente LangGraph
├── Nó Classificador
├── Nó de Resposta
└── Roteamento de Ferramentas (Edges)
    ├── Web Search
    ├── RAG
    ├── Calculadora
    └── Data/Hora
↓
Resposta
```

---

## ⚙️ Stack Tecnológica

### Linguagem

* Python 3.14.3

### Bibliotecas Principais

* Ecossistema LangChain:

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

* Integrações:

  * telethon (cliente Telegram)

* Utilitários:

  * numexpr (avaliação segura de expressões matemáticas)
  * pymupdf (parsing de PDF)
  * babel + pytz (formatação de data/hora)
  * markdown-it-py (parsing de markdown)
  * python-dotenv (gerenciamento de variáveis de ambiente)
  * loguru (logging)

---

## 🚀 Primeiros Passos

### 1. Clone o repositório

```bash
git clone <repo-url>
cd <repo>
```

---

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

`cp .env.example .env`

Preencha com suas credenciais:

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

### 4. Execute o projeto

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

### Raiz

* main.py
  Ponto de entrada. Carrega as variáveis de ambiente e inicia o serviço do Telegram.

* requirements.txt
  Dependências do projeto.

* .env.example
  Modelo para configuração do ambiente.

---

### src/

Código principal da aplicação.

---

## 🔧 Módulos Principais

### core/logger.py

Configura o logging estruturado usando Loguru:

* Console (colorizado)
* Logs em JSON (para análise)
* Arquivos de log rotativos

---

### services/telegram.py

Gerencia a integração com o Telegram usando Telethon:

* Escuta mensagens privadas
* Aplica lógica de gatilhos (triggers)
* Envia mensagens para o agente
* Simula atrasos humanos (human-like delay)

---

## 🤖 Agente (LangGraph)

### agent/graph.py

Define o fluxo de trabalho do agente usando LangGraph:

* Orquestração de nós
* Memória (InMemorySaver)
* Fluxo de execução

---

### agent/state.py

Define o `AgentState`:

* message
* messages
* classification
* response
* rastreamento de uso de ferramentas

---

### agent/edges.py

Controla a execução das ferramentas:

* Limita o uso de ferramentas custosas (web search, RAG)
* Previne uso excessivo da API
* Roteia chamadas de ferramentas dinamicamente

---

### Nós

#### classifier.py

Classifica a entrada do usuário:

* intent
* tone
* style
* confidence

---

#### answer.py

Nó principal de raciocínio:

* Decide quando usar ferramentas
* Gera a resposta final

---

#### schemas.py

Schemas Pydantic para saídas estruturadas.

---

## 🧰 Ferramentas

### Web Search

tools/websearch.py

* Usa a API Tavily
* Busca rápida em tempo real

---

### Calculadora

tools/calculator.py

* Avaliação segura usando numexpr
* Suporta expressões complexas

---

### Data/Hora

tools/datetime.py

* Consciente de fuso horário (timezone-aware)
* Formatação localizada (pt-BR)

---

### Sistema RAG (tools/rag/)

#### loader.py

Carrega documentos de `src/data`

#### splitter.py

Divide markdown usando `MarkdownTextSplitter`

#### vecstore.py

Cria vector store FAISS usando:

* Embeddings HuggingFace (all-MiniLM-L6-v2)

#### tool.py

Constrói a ferramenta de retriever para o agente

---

## 📄 Processamento de Dados

### data_processing/process_resume.py

Pipeline:

1. Extrai texto do PDF (PyMuPDF)
2. Envia para o LLM
3. Converte em Markdown estruturado
4. Armazena para uso no RAG

---

## 📂 Dados

Localizados em `src/data/`

* resume.pdf → entrada bruta
* resume.md → processado para RAG
* extra.md → dados contextuais adicionais

---

## 🧠 Decisões de Design

### Estratégia Multi-Model

O sistema suporta múltiplos provedores de LLM e pode ser estendido para rotear dinamicamente entre eles.

---

### Arquitetura Orientada a Ferramentas

Em vez de depender apenas do conhecimento do LLM, o agente:

* busca dados em tempo real
* realiza cálculos
* recupera conhecimento estruturado

---

### Uso Controlado de Ferramentas

Ferramentas custosas têm limitação de taxa (rate-limited) por interação para:

* reduzir custos
* melhorar a estabilidade

---

### RAG para Contexto Pessoal

Base de conhecimento personalizada permite que o agente:

* responda perguntas sobre o dono do sistema
* simule um assistente virtual em cenários reais

---

## 🔮 Melhorias Futuras

* Persistência de memória de longo prazo
* Execução autônoma de tarefas
* Personas multi-agente
* Respostas em streaming
* Observabilidade / tracing

---

## 📌 Notas Finais

Este projeto explora como sistemas modernos de IA podem ser desenhados além de prompts simples — focando em orquestração, ferramentas e integração com o mundo real.

Em vez de tratar LLMs como componentes isolados, o sistema os aproveita como parte de uma arquitetura mais ampla capaz de raciocinar, agir e se adaptar a diferentes contextos.

## 🎥 Demo

[▶️ Assista ao Teste](https://drive.google.com/file/d/1eIhc6EvsRozMnLkqibB361EVEAeL62rr/view?usp=sharing)