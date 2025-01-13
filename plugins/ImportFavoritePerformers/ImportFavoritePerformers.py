import sys, json, requests

try:
    import stashapi.log as log
    from stashapi.stashapp import StashInterface
except ModuleNotFoundError:
    print(
        "You need to install stashapp-tools. (https://pypi.org/project/stashapp-tools/)",
        file=sys.stderr,
    )
    print(
        "If you have pip (normally installed with python), run this command in a terminal (cmd): 'pip install stashapp-tools'",
        file=sys.stderr,
    )
    sys.exit()

# Constants
PER_PAGE = 25
STASHDB_ENDPOINT = "https://stashdb.org/graphql"


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


def query_local_performers():
    performers = stash.find_performers()
    performer_ids = []

    for performer in performers:
        for stash_id in performer["stash_ids"]:
            if stash_id["endpoint"] == STASHDB_ENDPOINT:
                performer_ids.append(stash_id["stash_id"])
    log.debug(f"Found {len(performer_ids)} performers in Stash.")
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
                    disambiguation
                    aliases
                    gender
                    urls {
                        url
                        type
                    }
                    birthdate {
                        date
                    }
                    death_date
                    ethnicity
                    country
                    eye_color
                    hair_color
                    height
                    measurements {
                        cup_size
                        band_size
                        waist
                        hip
                    }
                    breast_type
                    career_start_year
                    career_end_year
                    tattoos {
                        location
                        description
                    }
                    piercings {
                        location
                        description
                    }
                    images {
                        id
                        url
                        width
                        height
                    }
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
            stashdb_api_key,
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
    log.debug(f"Found {len(performers)} favorite performers in StashDB.")
    return performers


def clean_aliases(name, aliases):
    out_list = []
    for a in aliases:
        if a.lower() != name.lower():
            out_list.append(a)
    return out_list


def calc_measurements(measurements):
    if measurements is None:
        return ""
    if measurements["band_size"] and measurements["cup_size"] and measurements["waist"] and measurements["hip"]:
        return f"{measurements["band_size"]}{measurements["cup_size"]}-{measurements["waist"]}-{measurements["hip"]}"
    if measurements["band_size"] and measurements["cup_size"]:
        return f"{measurements["band_size"]}{measurements["cup_size"]}"
    return ""


def compare_performers(local_performers, stashdb_performers):
    missing_performers = [
        performer
        for performer in stashdb_performers
        if performer["id"] not in local_performers
    ]
    log.debug(f"Found {len(missing_performers)} missing performers.")
    return missing_performers


def convert_stashdb_performance_to_stash(performer):
    stash_performer = {
        "name": performer["name"],
        "alias_list": clean_aliases(performer["name"], performer["aliases"]),
        "birthdate": performer["birthdate"]["date"] if performer["birthdate"] else None,
        "career_length": format_career(
            performer["career_start_year"], performer["career_end_year"]
        ),
        "country": performer["country"],
        "death_date": performer["death_date"],
        "disambiguation": performer["disambiguation"],
        "ethnicity": convert_title_case(performer["ethnicity"]),
        "eye_color": convert_title_case(performer["eye_color"]),
        "fake_tits": convert_title_case(performer["breast_type"]),
        "gender": performer["gender"],
        "hair_color": convert_title_case(performer["hair_color"]),
        "height_cm": performer["height"],
        "image": performer["images"][0]["url"],
        "measurements": calc_measurements(performer["measurements"]),
        "piercings": convert_dictlist_to_string(
            performer["piercings"], "location", "description"
        ),
        "tattoos": convert_dictlist_to_string(
            performer["tattoos"], "location", "description"
        ),
        "urls": convert_dictlist_to_list(performer["urls"], "url"),
        "stash_ids": [{"endpoint": STASHDB_ENDPOINT, "stash_id": performer["id"]}],
    }
    return stash_performer


def convert_dictlist_to_list(dict, field):
    if dict is None:
        return None
    out_list = []
    for item in dict:
        out_list.append(item[field])
    return out_list


def convert_dictlist_to_string(dict, field1, field2):
    if dict is None:
        return None
    out_list = []
    for item in dict:
        pair = []
        if item[field1]:
            pair.append(item[field1])
        if item[field2]:
            pair.append(item[field2])
        out_list.append(", ".join(pair))
    return "; ".join(out_list)


def convert_title_case(string):
    return string.title() if string is not None else None


def format_career(start, end):
    if start is None:
        return None
    if end is None:
        return f"{start} -"
    return f"{start} - {end}"


def get_stashbox_config(endpoint):
    stash_boxes = stash.get_configuration().get("general", {}).get("stashBoxes")
    stash_box_config = [box for box in stash_boxes if box["endpoint"] == endpoint]
    return stash_box_config[0]


def run_import():
    global stashdb_api_key
    stashdb_api_key = get_stashbox_config(STASHDB_ENDPOINT)["api_key"]

    local_performers = query_local_performers()

    stashdb_performers = query_stashdb_performers()
    log.info(f"Found {len(stashdb_performers)} favorite performers in StashDB.")

    missing_performers = compare_performers(local_performers, stashdb_performers)

    if stashdb_performers:
        for index, performer in enumerate(missing_performers, start=1):
            create_performer = convert_stashdb_performance_to_stash(performer)
            result = stash.create_performer(create_performer)
            if result:
                if "id" in result and "name" in result:
                    log.info(
                        f"Created performer: {result['name']} with ID: {result['id']}"
                    )
            else:
                log.error(f"Failed to create performer: {performer['name']}")
            log.progress(index / len(missing_performers))


json_input = json.loads(sys.stdin.read())
FRAGMENT_SERVER = json_input["server_connection"]
stash = StashInterface(FRAGMENT_SERVER)

if __name__ == "__main__":
    run_import()
