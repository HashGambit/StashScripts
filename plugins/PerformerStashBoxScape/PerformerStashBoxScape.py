import json, sys

from classes.StashAppPerformer import (
    StashAppPerformer,
    StashAppPerformerUpdate,
    StashId,
)
from classes.StashBoxPerformer import StashBoxPerformer
from classes.StashBox import StashBox

try:
    import stashapi.log as log
    from stashapi.stashapp import StashInterface
except ModuleNotFoundError:
    print(
        "You need to install stashapp-tools. (https://pypi.org/project/stashapp-tools/)",
        file=sys.stderr,
    )
    sys.exit()


def processPerformer(performer: StashAppPerformer):
    log.info(f"processPerformer (id: {performer.id} name: {performer.name}")
    combineData = StashAppPerformerUpdate(id=performer.id, name=performer.name)
    for box in stashBoxes:
        box = StashBox(**box)
        stashId = None
        for id in performer.stash_ids:
            if id.endpoint == box.endpoint:
                stashId = id.stash_id
        if "stashdb" or "thepornhub" in box.endpoint:
            result = box.getPerformer(performer.name, stashId)
            if result is not None:
                combineData.update(result.exportToStash())
                combineData.stash_ids.append(
                    StashId(endpoint=box.endpoint, stash_id=result.id)
                )
    variables = combineData.model_dump()
    log.debug(variables)
    updateResult = stash.update_performer(variables)
    return updateResult
    # log.debug(updateResult)


def processAllPerformers():
    allPerformers = stash.find_performers()
    allPerformers = allPerformers[:1]
    log.info(f"performerStashBoxScrape has {len(allPerformers)} performers to process")

    for index, performer in enumerate(allPerformers, start=1):
        stashPerformer = StashAppPerformer(**performer)
        result = processPerformer(stashPerformer)
        log.progress(index / len(allPerformers))


def processMissingPerformers():
    missingPerformers = []
    for box in stashBoxes:
        missingPerformers.extend(
            stash.find_performers(
                {
                    "stash_id_endpoint": {
                        "endpoint": box["endpoint"],
                        "modifier": "NOT_MATCHES_REGEX",
                    },
                    "gender": {"value": "MALE", "modifier": "EQUALS"},
                }
            )
        )
    log.info(
        f"performerStashBoxScrape has {len(missingPerformers)} performers to process"
    )

    for index, performer in enumerate(missingPerformers, start=1):
        stashPerformer = StashAppPerformer(**performer)
        result = processPerformer(stashPerformer)
        log.progress(index / len(missingPerformers))


json_input = json.loads(sys.stdin.read())
FRAGMENT_SERVER = json_input["server_connection"]
stash = StashInterface(FRAGMENT_SERVER)
stashBoxes = stash.get_configuration().get("general", {}).get("stashBoxes")

mode = json_input["args"]["mode"]
log.debug(f"Mode: {mode}")
if mode == "processAllPerformers":
    processAllPerformers()
elif mode == "processMissingPerformers":
    processMissingPerformers()
elif mode == "createHook":
    hookData = json_input["args"]["hookContext"]
    log.debug(hookData)
    processPerformer(StashAppPerformer(id=hookData["id"], **hookData["input"]))
else:
    pass
