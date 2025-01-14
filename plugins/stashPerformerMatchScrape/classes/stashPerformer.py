import json
from datetime import datetime

from classes.boxPerformer import BoxPerformer
from classes.miscClasses import *

class StashPerformer:
    gender = TitleCase()
    ethnicity = TitleCase()
    eye_color = TitleCase()
    hair_color = TitleCase()

    def __init__(
        self,
        id=None,
        name=None,
        alias_list=None,
        birthdate=None,
        career_length=None,
        circumcised=None,
        country=None,
        death_date=None,
        details=None,
        disambiguation=None,
        ethnicity=None,
        eye_color=None,
        fake_tits=None,
        gender=None,
        hair_color=None,
        height_cm=None,
        measurements=None,
        penis_length=None,
        piercings=None,
        stash_ids=None,
        tattoos=None,
        urls=None,
        weight=None,
    ):
        self.id = id
        self.name = name
        self.alias_list = alias_list
        self.birthdate = birthdate
        self.career_length = career_length
        self.circumcised = circumcised
        self.country = country
        self.death_date = death_date
        self.details = details
        self.disambiguation = disambiguation
        self.ethnicity = ethnicity
        self.eye_color = eye_color
        self.fake_tits = fake_tits
        self.gender = gender
        self.hair_color = hair_color
        self.height_cm = height_cm
        self.measurements = measurements
        self.penis_length = penis_length
        self.piercings = piercings
        self.stash_ids = stash_ids
        self.tattoos = tattoos
        self.urls = urls
        self.weight = weight

    def __str__(self):
        return json.dumps(self.__dict__)

    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    @property
    def measurements(self):
        return self._measurements

    @measurements.setter
    def measurements(self, value):
        if type(value) is str:
            self._measurements = value
        elif type(value) is list:
            if value[0] and value[1] and value[2] and value[3]:
                self._measurements = f"{value[1]}{value[0]}-{value[2]}-{value[3]}"
            elif value[0] and value[1]:
                self._measurements = f"{value[1]}{value[0]}"

    @property
    def piercings(self):
        return self._piercings

    @piercings.setter
    def piercings(self, value):
        if isinstance(value, str):
            self._piercings = value
        elif isinstance(value, list):
            self._piercings = ", ".join(value)

    def load(self, input: dict):
        if input is not None:
            self.id = input["id"]
            self.name = input["name"]
            self.alias_list = input["alias_list"]
            self.birthdate = input["birthdate"]
            self.career_length = input["career_length"]
            self.circumcised = input["circumcised"]
            self.country = input["country"]
            self.death_date = input["death_date"]
            self.details = input["details"]
            self.disambiguation = input["disambiguation"]
            self.ethnicity = input["ethnicity"]
            self.eye_color = input["eye_color"]
            self.fake_tits = input["fake_tits"]
            self.gender = input["gender"]
            self.hair_color = input["hair_color"]
            self.height_cm = input["height_cm"]
            self.measurements = input["measurements"]
            self.penis_length = input["penis_length"]
            self.piercings = input["piercings"]
            self.stash_ids = input["stash_ids"]
            self.tattoos = input["tattoos"]
            self.urls = input["urls"]
            self.weight = input["weight"]

    def fromBox(self, input: BoxPerformer):
        if input is not None:
            self.name = input.name
            self.alias_list = input.aliases
            self.birthdate = input.birth_date
            self.career_length = " - ".join(
                [str(input.career_start_year), str(input.career_end_year)]
            )
            self.country = input.country
            self.death_date = input.death_date
            self.disambiguation = input.disambiguation
            self.ethnicity = input.ethnicity
            self.eye_color = input.eye_color
            self.fake_tits = input.breast_type
            self.gender = input.gender
            self.hair_color = input.hair_color
            self.height_cm = input.height
            self.measurements = [
                input.cup_size,
                input.band_size,
                input.waist_size,
                input.hip_size,
            ]
            self.piercings = input.piercings
            self.stash_ids = input.id
            self.tattoos = input.tattoos
            self.urls = input.urls

    def toJson(self):
        json_data = json.dumps(self)
        return json.loads(json_data)
