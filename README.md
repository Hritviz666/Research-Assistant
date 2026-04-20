# 🔍 AI Research Assistant

A Multi-Agent Research Assistant powered by **CrewAI**, **OpenAI GPT-4o-mini**, and **Tavily Search**. Users can generate research reports, compare topics, plan research, and get structured academic-style reports — all from a clean Streamlit UI backed by a FastAPI server. Every report can be downloaded as a **PDF**.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 📄 Research Topic | Generates a 3-format report — Concise Answer, Detailed Explanation, and Key Insights |
| ⚖️ Compare Topics | Compares two topics with Overview, Key Differences, Comparison Table, and When to Use What |
| 🗺️ Research Planner | Breaks a query into 3–5 focused sub-questions to guide deep research |
| 📋 Structured Report | Produces a full academic-style report with Abstract, Introduction, Core Concepts, Applications, and Conclusion |
| 📥 PDF Export | Every report across all 4 tabs can be downloaded as a formatted PDF |

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓
FastAPI Backend (main.py)
        ↓
CrewAI Orchestrator (research_crew.py)
        ↓
┌──────────────────────────────────────┐
│  Agent 1: Web Researcher             │  ← Tavily Search (live web)
│  Agent 2: Content Summarizer         │  ← GPT-4o-mini
│  Agent 3: Report Writer              │  ← GPT-4o-mini
└──────────────────────────────────────┘
        ↓
PDF Generator (pdf_utils.py)
        ↓
Downloaded PDF Report
```

### Agent Roles

| Agent | Role | Tools |
|-------|------|-------|
| Web Researcher | Searches the live web and collects factual, current information | Tavily Search |
| Content Summarizer | Distills research into concise key bullet points | GPT-4o-mini |
| Report Writer | Formats findings into structured markdown reports | GPT-4o-mini |

---

## 🧠 Why Both GPT-4o-mini AND Tavily?

They do completely different things:

| | GPT-4o-mini | Tavily Search |
|---|---|---|
| **Role** | The brain — reads, reasons, and writes | The eyes — fetches live web results |
| **Knowledge** | Frozen at training cutoff date | Real-time, up-to-date web data |
| **Internet access** | No | Yes |
| **Best for** | Understanding, summarizing, formatting | Finding current facts and sources |

**Without Tavily**, GPT-4o-mini can only answer from its training data — which may be outdated or incomplete for recent topics. Tavily fetches live articles first, then GPT-4o-mini reads and formats them into a clean report.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Multi-Agent Framework | CrewAI 1.4.1 |
| LLM | OpenAI GPT-4o-mini |
| Web Search | Tavily Search API |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| PDF Generation | fpdf2 |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
research_assistant/
├── .env                    # API keys (never commit this to git)
├── requirements.txt        # Python dependencies
├── README.md
└── src/
    ├── research_crew.py    # All CrewAI agents, tasks, and crew logic
    ├── main.py             # FastAPI backend with 4 endpoints
    ├── app.py              # Streamlit frontend with 4 tabs
    └── pdf_utils.py        # Markdown to PDF converter
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/research_assistant.git
cd research_assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file in the root folder

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Get your API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://app.tavily.com

---

## ▶️ Running the App

You need **two terminals** open simultaneously.

**Terminal 1 — Start FastAPI backend:**
```bash
cd src
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Start Streamlit frontend:**
```bash
cd src
streamlit run app.py
```

Then open your browser at:
```
http://localhost:8501
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/research` | Generate a 3-format research report |
| POST | `/compare` | Compare two topics |
| POST | `/plan` | Generate a research plan with sub-questions |
| POST | `/structured-report` | Generate a full academic-style report |

### Example Requests

```bash
# Research
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Future of quantum computing"}'

# Compare
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{"topic1": "Python", "topic2": "JavaScript"}'

# Plan
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{"query": "How does machine learning work?"}'

# Structured Report
curl -X POST "http://localhost:8000/structured-report" \
  -H "Content-Type: application/json" \
  -d '{"query": "Blockchain technology in supply chain"}'
```

Test all endpoints interactively at:
```
http://localhost:8000/docs
```

---

## 📦 Requirements

```
crewai[tools]==1.4.1
python-dotenv
fastapi
uvicorn
streamlit
fpdf2
markdown
```

---

## 🔍 How Each Feature Works

### 📄 Research Topic
3 agents run sequentially:
1. **Researcher** searches the web via Tavily (5 results)
2. **Summarizer** condenses findings into 5-7 bullet points
3. **Report Writer** formats into Concise Answer + Detailed Explanation + Key Insights

### ⚖️ Compare Topics
2 agents run sequentially:
1. **Researcher** gathers facts on both topics from the web
2. **Report Writer** structures into Overview, Key Differences, Comparison Table, When to Use What

### 🗺️ Research Planner
1 agent, no web search needed:
1. **Report Writer** generates 3-5 focused sub-questions from the query (~10 seconds)

### 📋 Structured Report
2 agents run sequentially:
1. **Researcher** collects detailed information from the web
2. **Report Writer** formats into Abstract → Introduction → Core Concepts → Key Insights → Applications → Conclusion

---

## ⚠️ Known Limitations

- Response time is 1-2 minutes for features involving web search (agents run sequentially)
- Research Planner is faster (~10 seconds) as it requires no web search
- OpenAI API credits are required for LLM inference
- Tavily free tier allows 1,000 searches/month

---

## 🙌 Acknowledgements

- [CrewAI](https://github.com/crewAIInc/crewAI) — Multi-agent orchestration framework
- [Tavily](https://tavily.com) — AI-optimized real-time web search API
- [OpenAI](https://openai.com) — GPT-4o-mini for LLM inference
- [FastAPI](https://fastapi.tiangolo.com) — Backend API framework
- [Streamlit](https://streamlit.io) — Frontend framework
- [fpdf2](https://py-pdf.github.io/fpdf2/) — PDF generation library