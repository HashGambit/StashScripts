import sys, requests, time  # type: ignore

try:
    import stashapi.log as log  # type: ignore
    from stashapi.stashapp import StashInterface  # type: ignore
except ModuleNotFoundError:
    print(
        "You need to install stashapp-tools. (https://pypi.org/project/stashapp-tools/)",
        file=sys.stderr,
    )


def find_performer(id, api_url, api_key):
    response = graphql_request(find_performer_query, {"id": id}, api_url, api_key)
    if response:
        return response.get("findPerformer")
    return None


def search_performer(term, api_url, api_key):
    response = graphql_request(search_performer_query, {"term": term}, api_url, api_key)
    if response:
        return response.get("searchPerformer")
    return None


def graphql_request(query, variables, endpoint, api_key, retries=5):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Apikey"] = api_key
    for attempt in range(retries):
        try:
            response = requests.post(
                endpoint, json={"query": query, "variables": variables}, headers=headers
            )
            response.raise_for_status()
            response_json = response.json()
            if "errors" in response_json:
                log.error(f"GraphQL request returned errors: {response_json['errors']}")
                return None
            return response_json.get("data")
        except requests.exceptions.RequestException as e:
            log.error(
                f"GraphQL request failed (attempt {attempt + 1} of {retries}): {e}"
            )
            if attempt < retries - 1:
                sleep_time = 2**attempt
                log.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                log.error("Max retries reached. Giving up.")
                raise


# GraphQL queries and mutations
local_find_performer_query = """
query FindLocalPerformer($id: ID!) {
    findPerformer(id: $id) {
        id
        name
        stash_ids {
            endpoint
            stash_id
        }
    }
}
"""


all_performers_query = """
query AllPerformers {
    allPerformers {
        id
        name
        stash_ids {
            endpoint
            stash_id
        }
    }
}
"""


search_performer_query = """
query SearchPerformer($term: String!) {
    searchPerformer(term: $term) {
        id
        name
    }
}
"""


find_performer_query = """
query FindPerformer($id: ID!) {
    findPerformer(id: $id) {
        id
        name
        disambiguation
        aliases
        gender
        birth_date
        age
        ethnicity
        country
        eye_color
        hair_color
        height
        cup_size
        band_size
        waist_size
        hip_size
        breast_type
        career_start_year
        career_end_year
        deleted
        scene_count
        merged_ids
        is_favorite
        created
        updated
        images {
            id
            url
        }
    }
}
"""


performer_update_mutation = """
mutation PerformerUpdate($input: PerformerUpdateInput!) {
    performerUpdate(input: $input) {
        id
        name
    }
}
"""
