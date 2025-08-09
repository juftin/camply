"""
Providers Seed Data
"""

from db.models.providers import Provider
from db.utils import format_description

RecreationDotGov = Provider(
    id=1,
    name="Recreation.gov",
    description=format_description("""
        Recreation.gov is the government's centralized travel planning platform and
        reservation system for 14 federal agencies, offering the tools, tips, and
        information needed for you to discover destinations and activities, plan
        a trip, and explore outdoor and cultural destinations in your zip code
        and across the country. Find and reserve incredible experiences that
        help you bring home a story through Recreation.gov!
    """),
    url="https://www.recreation.gov",
    enabled=True,
)
