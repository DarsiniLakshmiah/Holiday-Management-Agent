# Holiday Management Agent

An autonomous multi-agent AI system that turns a vague travel prompt into a fact-checked, day-by-day itinerary — complete with addresses, opening hours, prices, and a polished Markdown travel guide.

## Live webpage - https://holiday-management-agent-01t3.onrender.com/
---

## How It Works

Three specialised AI agents run in sequence, each handing their output to the next:

```
User Prompt → Planner → Researcher → Writer → Itinerary
```

| Agent | Role |
|-------|------|
| **Planner** | Builds a geographic skeleton itinerary — logical routing, balanced pacing, thematic consistency |
| **Researcher** | Enriches every activity with verified facts: addresses, hours, costs, and practical tips |
| **Writer** | Transforms the research into a beautifully formatted Markdown travel guide |

> The Writer is only allowed to use facts provided by the Researcher — no hallucinated hotels or made-up prices.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Agent framework | [AutoGen](https://github.com/microsoft/autogen) `autogen-agentchat 0.5.7` |
| LLM | OpenAI GPT-4o |
| API backend | FastAPI + Uvicorn |
| Streaming | Server-Sent Events (SSE) |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Data validation | Pydantic |
| Config | python-dotenv |

---

## Project Structure

```
Holiday-Management-Agent/
├── api.py                          # FastAPI server (web UI entry point)
├── app.py                          # CLI entry point
├── requirements.txt
├── setup.py
├── .env                            # Your API keys (not committed)
├── .env.example                    # Key template
│
├── holiday_management/
│   ├── agents/
│   │   ├── planner.py              # Planner agent
│   │   ├── researcher.py           # Researcher agent
│   │   └── writer.py               # Writer agent
│   ├── teams/
│   │   └── holiday_team.py         # Team orchestration & factory
│   ├── models/
│   │   └── gpt_model.py            # OpenAI model client
│   ├── config/
│   │   └── settings.py             # Env config
│   └── utils/
│       └── utils.py                # Save itinerary to disk
│
└── static/                         # Web UI assets
    ├── index.html
    ├── style.css
    └── script.js
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Holiday-Management-Agent.git
cd Holiday-Management-Agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=sk-...your-key-here...
MODEL_NAME=gpt-4o
```

---

## Running the App

### Web UI (recommended)

```bash
uvicorn api:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

![UI flow: type your trip → watch agents stream live → download the itinerary]

**Features:**
- Live streaming output — watch each agent think in real time
- Progress tracker showing Planner → Researcher → Writer stages
- Final itinerary rendered as formatted Markdown (tables, headings, tips)
- One-click `.md` download

### CLI

```bash
python app.py
```

Prompts you for a trip description and streams agent output to the terminal. The final itinerary is saved to `outputs/`.

---

## Example Prompt

```
7-day trip to Japan focusing on anime culture, authentic street food,
and modern city life. Budget is moderate.
```

The system will produce a complete day-by-day guide with:
- Specific neighbourhoods and venues per day
- Opening hours and entrance fees
- Transport recommendations
- A budget summary table

---

## Outputs

Finished itineraries are saved automatically to the `outputs/` folder as `.md` files:

```
outputs/
└── japan_20260410_143022.md
```

---

## Future Improvements

- Parallel research across multiple days to reduce latency
- PDF export of the final guide
- Direct booking links via Skyscanner / Booking.com APIs
- User accounts to save and revisit past itineraries

---

## What I Learned

This project was a deep dive into building real-world agentic AI systems — going far beyond a simple chatbot. Here are the key things I took away from it:

### Multi-Agent Architecture
I learned how to decompose a complex task (travel planning) into specialised roles — Planner, Researcher, and Writer — each with a focused responsibility. This taught me that giving an LLM one clear job produces far better results than asking a single prompt to do everything.

### Hallucination Prevention by Design
One of the hardest problems with LLMs is making things up. I tackled this structurally: the Writer agent is explicitly constrained to only use facts sourced from the Researcher. This separation of reasoning (Planner) from fact-finding (Researcher) from presentation (Writer) was a key architectural insight.

### AutoGen Agent Framework
I gained hands-on experience with Microsoft's **AutoGen** library (`autogen-agentchat`), learning how to:
- Define `AssistantAgent` instances with custom system prompts
- Compose agents into a `RoundRobinGroupChat` team
- Use termination conditions (`TextMentionTermination`, `MaxMessageTermination`) to control when a pipeline stops
- Build a factory pattern so each request gets fresh agent instances with clean conversation history

### Streaming with Server-Sent Events (SSE)
I learned how to stream live data from a Python backend to a browser using **Server-Sent Events**. This involved:
- Yielding SSE-formatted chunks from a FastAPI `StreamingResponse`
- Reading a streaming `fetch` response in JavaScript with a `ReadableStream` reader
- Buffering incoming chunks to handle partial SSE events correctly

### FastAPI for AI Backends
I built a production-style REST API with **FastAPI** that acts as the bridge between the browser and the agent pipeline — handling requests, streaming responses, and serving static files.

### Frontend Without a Framework
I built the entire UI in **vanilla HTML, CSS, and JavaScript** — no React, no Vue. This forced me to think carefully about DOM manipulation, event handling, and state management from first principles. I used the `marked.js` library to render the final Markdown output in the browser.

### Python Project Packaging
I structured the project as a proper installable Python package using `setup.py` and `find_packages()`, learned how to manage a virtual environment, and understood why isolating dependencies matters for reproducibility.

### Prompt Engineering
Writing effective system prompts for each agent was an art in itself. I learned to be explicit about output format, constraints, and handoff points — for example, telling the Planner to never include prices (that's the Researcher's job) and telling the Writer to end with `TERMINATE` so the pipeline knows when to stop.

---

## Technologies Used

| Technology | Purpose | What I Used It For |
|---|---|---|
| **Python 3.12** | Core language | Entire backend and agent logic |
| **AutoGen (`autogen-agentchat`)** | Multi-agent framework | Defining agents, team orchestration, streaming |
| **OpenAI GPT-4o** | Large Language Model | Powers all three agents |
| **FastAPI** | Web framework | REST API, SSE streaming endpoint, static file serving |
| **Uvicorn** | ASGI server | Running the FastAPI application |
| **Pydantic** | Data validation | Request body models in the API |
| **python-dotenv** | Config management | Loading API keys from `.env` securely |
| **HTML5 / CSS3** | Frontend markup & styling | Responsive UI, CSS Grid layout, animations |
| **Vanilla JavaScript** | Frontend logic | Fetch streaming, SSE parsing, DOM manipulation |
| **marked.js** | Markdown rendering | Rendering the final itinerary in the browser |
| **Git** | Version control | Source control throughout the project |
