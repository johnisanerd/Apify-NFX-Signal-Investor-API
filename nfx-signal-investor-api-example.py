"""
NFX Signal Investor API - Python quick start.

Pulls venture investors, VC firms, and the investor-list catalog from Signal by
NFX as structured JSON, including the check size each investor writes.

Get a free Apify account and API token: https://apify.com?fpr=9n7kx3
Actor page: https://apify.com/johnvc/nfx-signal-investor-api?fpr=9n7kx3

Every run below is deliberately small (low maxItems, one list) so your first run
stays cheap. Raise maxItems, or set it to 0, once you know the shape you want.
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR = "johnvc/nfx-signal-investor-api"
TOKEN = os.getenv("APIFY_API_TOKEN")


def client() -> ApifyClient:
    if not TOKEN:
        raise SystemExit(
            "Set APIFY_API_TOKEN first. Copy .env.example to .env and paste your token. "
            "Free account: https://apify.com?fpr=9n7kx3"
        )
    return ApifyClient(TOKEN)


def run(run_input: dict) -> list[dict]:
    """Run the Actor and return its dataset rows.

    apify-client 3.x returns a typed Run object, so read run.default_dataset_id
    rather than subscripting the result like a dict.
    """
    api = client()
    started = api.actor(ACTOR).call(run_input=run_input)
    rows = list(api.dataset(started.default_dataset_id).iterate_items())
    print(f"{run_input.get('mode', 'investors')}: {len(rows)} row(s)")
    return rows


def show(rows: list[dict], *fields: str, limit: int = 5) -> None:
    for row in rows[:limit]:
        print("  " + " | ".join(f"{f}={row.get(f)}" for f in fields))


# ---------------------------------------------------------------------------
# 1. Discover what you can pull. Start here: the catalog of every public list.
#    Mirrors the task "VC Database Export by Sector and Stage".
# ---------------------------------------------------------------------------
def run_vc_database_catalog() -> list[dict]:
    rows = run({"mode": "lists", "maxItems": 10})
    show(rows, "slug", "investorCount", "stage", "vertical")
    return rows


# ---------------------------------------------------------------------------
# 2. How to find investors for a startup: investors by stage and sector, with
#    the check size each one writes.
#    Mirrors "Find Investors for Your Startup by Stage and Check Size".
# ---------------------------------------------------------------------------
def run_find_investors() -> list[dict]:
    rows = run(
        {
            "mode": "investors",
            "listSlugs": ["saas-seed"],
            "maxItems": 25,
            "pageSize": 50,
        }
    )
    show(rows, "name", "position", "firmName", "targetInvestment", "personUrl")
    return rows


# ---------------------------------------------------------------------------
# 3. A list of VC firms for one geography, ready for a CRM import.
#    Mirrors "List of VC Firms in San Francisco Bay Area".
# ---------------------------------------------------------------------------
def run_list_of_vc_firms() -> list[dict]:
    rows = run({"mode": "firms", "listSlugs": ["san-francisco-bay-area"], "maxItems": 25})
    show(rows, "firmName", "firmUrl", "sourceListVertical")
    return rows


# ---------------------------------------------------------------------------
# 4. Optional firm enrichment. Each unique firm is enriched once and billed
#    once, and unresolved firms are never charged. Enrichment adds minutes to a
#    run, so keep maxItems small while you are testing.
# ---------------------------------------------------------------------------
def run_enriched_investors() -> list[dict]:
    rows = run(
        {
            "mode": "investors",
            "listSlugs": ["ai-seed"],
            "maxItems": 10,
            "enrichWithCrunchbase": True,
            # "enrichWithLinkedIn": True,   # turn on for firmographics too
        }
    )
    show(rows, "name", "firmName", "crunchbaseRank", "crunchbaseStatus", "crunchbaseUrl")
    return rows


# ---------------------------------------------------------------------------
# 5. Filter the catalog to one stage, then pull the lists that matter.
# ---------------------------------------------------------------------------
def run_pre_seed_lists() -> list[dict]:
    rows = run({"mode": "lists", "stage": "pre_seed", "maxItems": 10})
    show(rows, "slug", "investorCount", "vertical")
    return rows


if __name__ == "__main__":
    print("1. Catalog of investor lists")
    run_vc_database_catalog()

    print("\n2. Investors with check sizes")
    run_find_investors()

    print("\n3. VC firms in one geography")
    run_list_of_vc_firms()

    print("\n4. Pre-seed lists only")
    run_pre_seed_lists()

    # Enrichment is slower and costs more per firm, so it is opt-in here.
    # print("\n5. Investors with Crunchbase enrichment")
    # run_enriched_investors()
