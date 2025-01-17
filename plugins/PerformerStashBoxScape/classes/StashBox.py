import requests
import stashapi.log as log
from classes.StashBoxPerformer import StashBoxPerformer

from pydantic import BaseModel

PER_PAGE = 25


class StashBox(BaseModel):
    name: str
    endpoint: str
    api_key: str

    def getPerformer(self, name, id) -> StashBoxPerformer:
        matchingPerformers = []
        performers = []
        page = 1
        total_performers = None

        if "stashdb" in self.endpoint:
            query = self.__stashPerformerQuery
            while True:
                result = self.__query(
                    query, {"input": {"name": name, "page": page, "per_page": PER_PAGE}}
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
        elif "theporndb" in self.endpoint:
            query = self.__tpdbPerformerQuery
            result = self.__query(query, {"input": name})
            if result:
                log.debug(result)
                performer_data = result["data"]["searchPerformer"]
                performers.extend(performer_data)
        log.debug(f"Query results: {len(performers)} performers from {self.name}")
        # Match by existing stashId
        for p in performers:
            if p["id"] == id:
                matchingPerformers.append(StashBoxPerformer(**p))
        if len(matchingPerformers) == 1:
            return matchingPerformers[0]
        # Match by exact name
        for p in performers:
            if p["name"] == name:
                matchingPerformers.append(StashBoxPerformer(**p))
        if len(matchingPerformers) == 1:
            return matchingPerformers[0]

        log.warning(
            f"{self.name}: Error matching, found {len(matchingPerformers)} matching records for {name}!"
        )
        return None

    def __query(self, query, variables=None):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["ApiKey"] = self.api_key

        log.trace(f"variables: {variables}")
        log.trace(f"query: {query}")
        log.trace(f"headers: {headers}")

        response = requests.post(
            self.endpoint,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            log.error(
                f"Query to {self.endpoint} failed with status code {response.status_code}: {response.text}"
            )
            return None

    __stashPerformerQuery = " ".join(
        (
            """query Query($input: PerformerQueryInput!) {
                queryPerformers(input: $input) {
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
                            accuracy
                        }
                        birth_date
                        death_date
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
                        }
                        is_favorite
                    }
                }
            }
        """
        ).split()
    )
    __tpdbPerformerQuery = " ".join(
        (
            """query Query($input: String!) {
                searchPerformer(term: $input) {
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
                        accuracy
                    }
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
                    }
                    is_favorite
                }
            }
        """
        ).split()
    )
