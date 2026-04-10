from pathlib import Path
from datetime import datetime


def save_itinerary(content: str, destination: str = "holiday") -> str:
    """Save the final itinerary as a Markdown file in the outputs/ directory.

    Returns the path of the saved file.
    """
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    slug = destination.lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.md"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(output_path)


def extract_destination(user_request: str) -> str:
    """Best-effort extraction of the destination name from the user request."""
    # Simple heuristic: look for 'to <Place>' pattern
    import re
    match = re.search(r"\bto\s+([A-Z][a-zA-Z\s]+)", user_request)
    if match:
        return match.group(1).strip().split()[0]  # first word of destination
    return "holiday"
