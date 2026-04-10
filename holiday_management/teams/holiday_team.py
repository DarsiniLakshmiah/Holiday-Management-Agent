import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

from holiday_management.models.gpt_model import model_client
from holiday_management.agents.planner import SYSTEM_MESSAGE as PLANNER_MSG, DESCRIPTION as PLANNER_DESC
from holiday_management.agents.researcher import SYSTEM_MESSAGE as RESEARCHER_MSG, DESCRIPTION as RESEARCHER_DESC
from holiday_management.agents.writer import SYSTEM_MESSAGE as WRITER_MSG, DESCRIPTION as WRITER_DESC


def create_holiday_team() -> RoundRobinGroupChat:
    """Create a fresh team with new agent instances for each run.

    Fresh instances are required so conversation history does not leak
    between separate planning requests.
    """
    planner = AssistantAgent(
        name="Holiday_Planner",
        description=PLANNER_DESC,
        model_client=model_client,
        system_message=PLANNER_MSG,
    )
    researcher = AssistantAgent(
        name="Holiday_Researcher",
        description=RESEARCHER_DESC,
        model_client=model_client,
        system_message=RESEARCHER_MSG,
    )
    writer = AssistantAgent(
        name="Holiday_Writer",
        description=WRITER_DESC,
        model_client=model_client,
        system_message=WRITER_MSG,
    )

    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(max_messages=10)

    return RoundRobinGroupChat(
        participants=[planner, researcher, writer],
        termination_condition=termination,
    )


async def run_holiday_agent(user_request: str):
    """CLI helper: run the pipeline and stream output to the console."""
    team = create_holiday_team()
    result = await Console(team.run_stream(task=user_request))
    return result
