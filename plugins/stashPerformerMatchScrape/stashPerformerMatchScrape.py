import sys, json, requests  # type: ignore
from datetime import datetime
from performerClass import BoxPerformer, StashPerformer
import graphqlClient as gql

try:
    import stashapi.log as log  # type: ignore
    from stashapi.stashapp import StashInterface  # type: ignore
except ModuleNotFoundError:
    print(
        "You need to install stashapp-tools. (https://pypi.org/project/stashapp-tools/)",
        file=sys.stderr,
    )

# Constants
STASHDB_ENDPOINT = "https://stashdb.org/graphql"
TPDB_ENDPOINT = "https://theporndb.net/graphql"


# Functions
def get_hook_context():
    try:
        json_input = json.loads(sys.stdin.read())
        hook_context = json_input.get("args", {}).get("hookContext", {})
        return hook_context
    except json.JSONDecodeError:
        log.error("Failed to decode JSON input.")
        return {}


def get_stashbox_apikey(endpoint):
    stash_boxes = stash.get_configuration().get("general", {}).get("stashBoxes")
    for box in stash_boxes:
        if box["endpoint"] == endpoint:
            return box["api_key"]
    return None


def parse_birthdate(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y").date()
            except ValueError:
                return None
    return None


def parse_measurements(cup_size, band_size, waist_size, hip_size):
    measurements = []
    if band_size and cup_size:
        measurements.append(f"{band_size}{cup_size}")
    if waist_size:
        measurements.append(waist_size)
    if hip_size:
        measurements.append(hip_size)
    return "-".join(measurements)


def update_performer(performer_data, local_id):
    performer_data["id"] = local_id

    # Convert date to string
    if isinstance(performer_data["birthdate"], datetime):
        performer_data["birthdate"] = performer_data["birthdate"].strftime("%Y-%m-%d")

    variables = {"input": performer_data}

    response = stash.update_performer(variables)
    if response:
        return response.get("performerUpdate")
    return None


def update_performer_data(performer):
    log.info(f"Processing performer: {performer['name']} (ID: {performer['id']})")

    # Check if the performer already has a ThePornDB or stashDB stash ID
    has_tpdb_id = any(
        stash["endpoint"] == TPDB_ENDPOINT for stash in performer["stash_ids"]
    )
    has_stashdb_id = any(
        stash["endpoint"] == STASHDB_ENDPOINT for stash in performer["stash_ids"]
    )

    tpdb_match = None
    stashdb_match = None

    if not has_stashdb_id:
        stashdb_results = gql.search_performer(
            performer["name"], STASHDB_ENDPOINT, stashdb_api_key
        )
        if stashdb_results:
            exact_matches = [
                result
                for result in stashdb_results
                if result["name"].lower() == performer["name"].lower()
            ]

            if len(exact_matches) == 1:
                stashdb_match = exact_matches[0]
            elif len(exact_matches) > 1:
                log.info(
                    f"Skipped performer {performer['name']} due to multiple exact matches on stashDB."
                )
            else:
                log.info(f"No exact match found on stashDB for: {performer['name']}")

    if not has_tpdb_id:
        tpdb_results = gql.search_performer(
            performer["name"], TPDB_ENDPOINT, tpdb_api_key
        )
        if tpdb_results:
            exact_matches = [
                result
                for result in tpdb_results
                if result["name"].lower() == performer["name"].lower()
            ]

            if len(exact_matches) == 1:
                tpdb_match = exact_matches[0]
            elif len(exact_matches) > 1:
                log.info(
                    f"Skipped performer {performer['name']} due to multiple exact matches on ThePornDB."
                )
            else:
                log.info(f"No exact match found on ThePornDB for: {performer['name']}")

    tpdb_performer_data = BoxPerformer(
        gql.find_performer(tpdb_match["id"], TPDB_ENDPOINT, tpdb_api_key)
        if tpdb_match
        else None
    )
    stashdb_performer_data = BoxPerformer(
        gql.find_performer(stashdb_match["id"], STASHDB_ENDPOINT, stashdb_api_key)
        if stashdb_match
        else None
    )

    if tpdb_performer_data or stashdb_performer_data:
        # Combine data from both sources, with stashDB taking precedence if available
        combined_data = StashPerformer()
        if tpdb_performer_data:
            log.debug(f"TPDB performer data: {tpdb_performer_data}")
            combined_data.load_from_box(performer=tpdb_performer_data)
        if stashdb_performer_data:
            # combined_data.update(stashdb_performer_data)
            log.debug(f"StashDB performer data: {stashdb_performer_data}")
            combined_data.update_from_box(stashdb_performer_data)

        image_url = None
        if tpdb_performer_data and isinstance(tpdb_performer_data, dict):
            image_url = (tpdb_performer_data.get("images") or [{}])[0].get("url")
        if (
            not image_url
            and stashdb_performer_data
            and isinstance(stashdb_performer_data, dict)
        ):
            image_url = (stashdb_performer_data.get("images") or [{}])[0].get("url")

        gender = combined_data.get("gender")
        if gender not in ["MALE", "FEMALE"]:
            gender = None
        alias_list = list(set(combined_data.get("aliases", [])))  # Remove duplicates
        birthdate = parse_birthdate(combined_data.get("birth_date"))
        measurements = parse_measurements(
            combined_data.get("cup_size", ""),
            combined_data.get("band_size", ""),
            combined_data.get("waist_size", ""),
            combined_data.get("hip_size", ""),
        )
        # Add existing stash IDs
        existing_stash_ids = performer["stash_ids"] if performer["stash_ids"] else []

        # Add new stash IDs
        new_stash_ids = []
        if tpdb_match:
            new_stash_ids.append(
                {
                    "stash_id": tpdb_match["id"],
                    "endpoint": "https://theporndb.net/graphql",
                }
            )
        if stashdb_match:
            new_stash_ids.append(
                {
                    "stash_id": stashdb_match["id"],
                    "endpoint": STASHDB_ENDPOINT,
                }
            )

        # Combine existing and new stash IDs
        combined_stash_ids = existing_stash_ids + new_stash_ids

        performer_update_data = {
            "name": combined_data["name"],
            "disambiguation": combined_data.get("disambiguation"),
            "alias_list": ", ".join(alias_list),
            "gender": gender,
            "birthdate": birthdate.strftime("%Y-%m-%d") if birthdate else None,
            "ethnicity": combined_data.get("ethnicity"),
            "country": combined_data.get("country"),
            "eye_color": combined_data.get("eye_color"),
            "hair_color": combined_data.get("hair_color"),
            "height_cm": combined_data.get("height"),
            "measurements": measurements,
            "fake_tits": combined_data.get("breast_type"),
            "career_length": (
                f"{combined_data.get('career_start_year', '')} - {combined_data.get('career_end_year', '')}"
                if combined_data.get("career_end_year")
                else f"{combined_data.get('career_start_year', '')}"
            ),
            "details": None,  # Set to None if you don't have the details field
            "death_date": None,  # Set to None if you don't have the death_date field
            "weight": None,  # Set to None if you don't have the weight field
            "twitter": None,  # Set to None if you don't have the twitter field
            "instagram": None,  # Set to None if you don't have the instagram field
            "image": image_url,
            "url": None,  # Set to None if you don't have the URL
            "tag_ids": None,  # Set to None if you don't have tag IDs
            "tattoos": None,  # Set to None if you don't have tattoo information
            "piercings": None,  # Set to None if you don't have piercing information
            "stash_ids": combined_stash_ids,
        }

        log.debug(f"Prepared performer update data: {performer_update_data}")

        try:
            update_result = update_performer(performer_update_data, performer["id"])
            if update_result:
                log.info(
                    f"Updated performer: {update_result['name']} (ID: {update_result['id']}) with new data."
                )
            else:
                log.info(
                    f"No new details added for performer {performer['name']} (ID: {performer['id']}) - already up to date."
                )
        except requests.exceptions.HTTPError as e:
            log.error(
                f"Failed to update performer: {performer['name']} (ID: {performer['id']})"
            )
            log.error(e.response.text)
    else:
        log.info(
            f"No new details added for performer {performer['name']} (ID: {performer['id']}) - already up to date."
        )


def update_all_performers():
    performers = stash.find_performers()
    total_performers = len(performers)
    log.debug(f"Found {total_performers} performers.")

    for index, performer in enumerate(performers, start=0):
        log.progress(index / total_performers)
        update_performer_data(performer)


def update_single_performer(performer_id):
    performer = stash.find_performer(performer_id)
    if performer:
        update_performer_data(performer)
    else:
        log.error(f"Performer with ID {performer_id} not found.")


def main():
    global stashdb_api_key, tpdb_api_key
    stashdb_api_key = get_stashbox_apikey(STASHDB_ENDPOINT)
    log.debug(f"StashDB API key: {stashdb_api_key}")
    tpdb_api_key = get_stashbox_apikey(TPDB_ENDPOINT)
    log.debug(f"ThePornDB API key: {tpdb_api_key}")

    hook_context = get_hook_context()
    if hook_context:
        performer_id = hook_context.get("id")
        if performer_id:
            update_single_performer(performer_id)
        else:
            log.error("No performer ID provided in the hook context.")
    else:
        update_all_performers()


json_input = json.loads(sys.stdin.read())
FRAGMENT_SERVER = json_input["server_connection"]
stash = StashInterface(FRAGMENT_SERVER)

if __name__ == "__main__":
    main()
