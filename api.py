import json
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from holiday_management.teams.holiday_team import create_holiday_team
from holiday_management.utils.utils import save_itinerary, extract_destination

app = FastAPI(title="Holiday Management Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class PlanRequest(BaseModel):
    request: str


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/plan")
async def plan(body: PlanRequest):
    """Stream agent messages back to the client using Server-Sent Events."""

    async def event_stream():
        from autogen_agentchat.base import TaskResult
        from autogen_agentchat.messages import TextMessage

        team = create_holiday_team()
        final_content = ""

        try:
            async for message in team.run_stream(task=body.request):
                if isinstance(message, TaskResult):
                    # Last message is the Writer's output
                    if message.messages:
                        final_content = message.messages[-1].content.replace("TERMINATE", "").strip()
                    # Save to disk
                    destination = extract_destination(body.request)
                    saved_path = save_itinerary(final_content, destination)
                    payload = {
                        "type": "done",
                        "content": final_content,
                        "saved_path": saved_path,
                    }
                    yield f"data: {json.dumps(payload)}\n\n"

                elif isinstance(message, TextMessage):
                    payload = {
                        "type": "message",
                        "source": message.source,
                        "content": message.content,
                    }
                    yield f"data: {json.dumps(payload)}\n\n"

        except Exception as exc:
            payload = {"type": "error", "content": str(exc)}
            yield f"data: {json.dumps(payload)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
