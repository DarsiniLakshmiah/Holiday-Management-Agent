import asyncio
from dotenv import load_dotenv

from holiday_management.teams.holiday_team import run_holiday_agent
from holiday_management.utils.utils import save_itinerary, extract_destination

load_dotenv()

DEFAULT_REQUEST = (
    "Plan a 7-day trip to Japan focusing on anime culture, "
    "authentic street food, and modern city life. Budget is moderate."
)


async def main() -> None:
    print("=" * 60)
    print("       Holiday Management Agent  (CLI)")
    print("=" * 60)
    print("Describe your ideal holiday and the agent team will build")
    print("a personalised, fact-checked itinerary for you.\n")

    user_request = input("Your request (press Enter for demo): ").strip()
    if not user_request:
        user_request = DEFAULT_REQUEST
        print(f"\n[Using demo request]: {user_request}")

    print("\n" + "=" * 60)
    print("Starting agents: Planner → Researcher → Writer")
    print("=" * 60 + "\n")

    result = await run_holiday_agent(user_request)

    if result and result.messages:
        final_content = result.messages[-1].content
        clean_content = final_content.replace("TERMINATE", "").strip()
        destination = extract_destination(user_request)
        saved_path = save_itinerary(clean_content, destination)
        print("\n" + "=" * 60)
        print(f"Itinerary saved to: {saved_path}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
