import json
from datetime import datetime

from classes.miscClasses import *

class TitleCase:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value is not None:
            instance.__dict__[self._name] = str(value).title()


class BoxPerformer:
    gender = TitleCase()
    ethnicity = TitleCase()
    eye_color = TitleCase()
    hair_color = TitleCase()

    def __init__(
        self,
        id=None,
        name=None,
        aliases=None,
        band_size=None,
        birth_date=None,
        birthdate=None,
        breast_type=None,
        career_end_year=None,
        career_start_year=None,
        country=None,
        cup_size=None,
        death_date=None,
        disambiguation=None,
        ethnicity=None,
        eye_color=None,
        gender=None,
        hair_color=None,
        height=None,
        hip_size=None,
        images=None,
        piercings=[BodyMod()],
        scene_count=None,
        tattoos=[BodyMod()],
        urls=[Urls()],
        waist_size=None,
    ):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.band_size = band_size
        self.birth_date = birth_date
        self.birthdate = birthdate
        self.breast_type = breast_type
        self.career_end_year = career_end_year
        self.career_start_year = career_start_year
        self.country = country
        self.cup_size = cup_size
        self.death_date = death_date
        self.disambiguation = disambiguation
        self.ethnicity = ethnicity
        self.eye_color = eye_color
        self.gender = gender
        self.hair_color = hair_color
        self.height = height
        self.hip_size = hip_size
        self.images = images
        self.piercings = piercings
        self.scene_count = scene_count
        self.tattoos = tattoos
        self.urls = urls
        self.waist_size = waist_size

    def __str__(self):
        return json.dumps(self.__dict__)

    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()
    def load(self, input: dict):
        if input is not None:
            self.id = input["id"]
            self.name = input["name"]
            self.disambiguation = input["disambiguation"]
            self.aliases = input["aliases"]
            self.gender = input["gender"]
            self.urls = input["urls"]
            self.birth_date = input["birth_date"]
            self.age = input["age"]
            self.ethnicity = input["ethnicity"]
            self.country = input["country"]
            self.eye_color = input["eye_color"]
            self.hair_color = input["hair_color"]
            self.height = input["height"]
            self.cup_size = input["cup_size"]
            self.band_size = input["band_size"]
            self.waist_size = input["waist_size"]
            self.hip_size = input["hip_size"]
            self.breast_type = input["breast_type"]
            self.career_start_year = input["career_start_year"]
            self.career_end_year = input["career_end_year"]
            self.tattoos = input["tattoos"]
            self.piercings = input["piercings"]
            self.images = input["images"]
            self.scene_count = input["scene_count"]
