# Holiday Management Agent

An autonomous multi-agent AI system that turns a vague travel prompt into a fact-checked, day-by-day itinerary — complete with addresses, opening hours, prices, and a polished Markdown travel guide.

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
