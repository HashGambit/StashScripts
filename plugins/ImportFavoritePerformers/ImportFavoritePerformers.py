import requests
import json
import sys
import stashapi.log as log

from stashapi.stashapp import StashInterface

# Constants
PER_PAGE = 25
DEFAULT_GRAPHQL_URL = "http://localhost:9999/graphql"


def gql_query(endpoint, query, variables=None, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Apikey"] = api_key
    response = requests.post(
        endpoint, json={"query": query, "variables": variables}, headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        log.error(
            f"Query failed with status code {response.status_code}: {response.text}"
        )
        return None


def get_stash_connection_info():
    """
    Retrieves Stash connection details.
    """
    try:
        # Parse connection details from stdin
        json_input = json.loads(sys.stdin.read())
        FRAGMENT_SERVER = json_input.get("server_connection")

        stash = StashInterface(FRAGMENT_SERVER)
        stash_config = stash.get_configuration()

        api_key = stash_config.get("general", {}).get("apiKey")
        if not api_key:
            log.warning("Local API key not found. Proceeding without it.")

        return FRAGMENT_SERVER, api_key
    except Exception as e:
        log.error(f"Error retrieving Stash connection info: {e}")
        return None, None


def query_local_performers():
    performers = stash.find_performers()
    performer_ids = []

    for performer in performers:
        for stash_id in performer["stash_ids"]:
            if stash_id["endpoint"] == "https://stashdb.org/graphql":
                performer_ids.append(stash_id["stash_id"])
    return performer_ids


def query_stashdb_performers():
    """
    Fetch favorite performers from StashDB.
    """
    query = """
        query QueryPerformers ($page: Int!, $per_page: Int!) {
            queryPerformers(
                input: {
                    is_favorite: true,
                    per_page: $per_page,
                    page: $page
                }
            ) {
                count
                performers {
                    id
                    name
                }
            }
        }
    """

    performers = []
    page = 1
    total_performers = None
    while True:
        result = gql_query(
            STASHDB_ENDPOINT,
            query,
            {"page": page, "per_page": PER_PAGE},
            STASHDB_API_KEY,
        )
        if result:
            performer_data = result["data"]["queryPerformers"]
            performers.extend(performer_data["performers"])
            total_performers = total_performers or performer_data["count"]
            if (
                len(performers) >= total_performers
                or len(performer_data["performers"]) < PER_PAGE
            ):
                break
            page += 1
        else:
            break
    return performers


def compare_performers(local_performers, stashdb_performers):
    missing_performers = [
        performer
        for performer in stashdb_performers
        if performer["id"] not in local_performers
    ]
    log.info(f"Found {len(missing_performers)} missing performers.")
    return missing_performers


def importFavorites():
    local_performers = query_local_performers()

    log.info(f"Found {len(local_performers)} performers in Stash.")

    stashdb_performers = query_stashdb_performers()
    log.info(f"Found {len(stashdb_performers)} favorite performers in StashDB.")

    missing_performers = compare_performers(local_performers, stashdb_performers)

    if stashdb_performers:
        for performer in missing_performers:
            create_performer = {
                "name": performer["name"],
                "stash_ids": {
                    "stash_id": performer["id"],
                    "endpoint": STASHDB_ENDPOINT,
                },
            }
            result = stash.create_performer(create_performer)

            scrapedPerformer = stash.scrape_performer(
                {"stash_box_endpoint": STASHDB_ENDPOINT}, result["id"]
            )[0]

            scrapedPerformer["id"] = result["id"]
            scrapedPerformer["alias_list"] = scrapedPerformer["aliases"]
            scrapedPerformer["height_cm"] = scrapedPerformer["height"]
            scrapedPerformer["image"] = scrapedPerformer["images"][0]
            scrapedPerformer["tag_ids"] = scrapedPerformer["tags"]

            del scrapedPerformer["aliases"]
            del scrapedPerformer["height"]
            del scrapedPerformer["images"]
            del scrapedPerformer["remote_site_id"]
            del scrapedPerformer["stored_id"]
            del scrapedPerformer["tags"]
            log.debug(f"Scraped performer: {scrapedPerformer}")

            stash.update_performer(scrapedPerformer)
            # log.info(f"Created performer: {result}")


json_input = json.loads(sys.stdin.read())
FRAGMENT_SERVER = json_input["server_connection"]
stash = StashInterface(FRAGMENT_SERVER)

LOCAL_API_KEY = stash.get_configuration().get("general", {}).get("apiKey")
log.debug(f"Local API Key: {LOCAL_API_KEY}")
STASHDB_API_KEY = (
    stash.get_configuration()
    .get("plugins", {})
    .get("importFavoritePerformers", {})
    .get("StashDb Api Key")
)
STASHDB_ENDPOINT = "https://stashdb.org/graphql"
log.debug(f"StashDB API Key: {STASHDB_API_KEY}")

if __name__ == "__main__":
    importFavorites()
