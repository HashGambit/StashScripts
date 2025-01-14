from datetime import datetime
from multipledispatch import dispatch

class BoxPerformer:
    @dispatch()
    def __init__(self):
        self.id
        self.name
        self.disambiguation
        self.aliases
        self.gender
        self.urls
        self.birthdate
        self.birth_date
        self.death_date
        self.age
        self.ethnicity
        self.country
        self.eye_color
        self.hair_color
        self.height
        self.cup_size
        self.band_size
        self.waist_size
        self.hip_size
        self.breast_type
        self.career_start_year
        self.career_end_year
        self.tattoos
        self.piercings
        self.images
        self.scene_count

    @dispatch(dict)
    def __init__(self, performer):
        self.id
        self.name
        self.disambiguation
        self.aliases
        self.gender
        # self.urls {
        #     url
        #     type
        # }
        # self.birthdate {
        #     date
        #     accuracy
        # }
        self.birth_date
        self.death_date
        self.age
        self.ethnicity
        self.country
        self.eye_color
        self.hair_color
        self.height
        # measurements {
        #     cup_size
        #     band_size
        #     waist
        #     hip
        # }
        self.cup_size
        self.band_size
        self.waist_size
        self.hip_size
        self.breast_type
        self.career_start_year
        self.career_end_year
        # self.tattoos {
        #     location
        #     description
        # }
        # self.piercings {
        #     location
        #     description
        # }
        # self.images {
        #     id
        #     url
        #     width
        #     height
        # }
        self.scene_count


class StashPerformer:
    @dispatch()
    def __init__(self):
        self.id = None
        self.name = None
        self.alias_list = None
        self.birthdate = None
        self.career_length = None
        self.country = None
        self.death_date = None
        self.disambiguation = None
        self.ethnicity = None
        self.eye_color = None
        self.fake_tits = None
        self.gender = None
        self.hair_color = None
        self.height_cm = None
        self.image = None
        self.measurements = None
        self.piercings = None
        self.stash_ids = None
        self.tattoos = None

    @dispatch(dict)
    def __init__(self, performer):
        self.id = performer["id"]
        self.name = performer["name"]
        self.alias_list = performer["aliases"]
        self.birthdate = performer["birthdate"]
        self.career_length = performer["career_length"]
        self.country = performer["country"]
        self.death_date = performer["death_date"]
        self.disambiguation = performer["disambiguation"]
        self.ethnicity = performer["ethnicity"]
        self.eye_color = performer["eye_color"]
        self.fake_tits = performer["fake_tits"]
        self.gender = performer["gender"]
        self.hair_color = performer["hair_color"]
        self.height_cm = performer["height_cm"]
        self.image = performer["image"]
        self.measurements = performer["measurements"]
        self.piercings = performer["piercings"]
        self.stash_ids = performer["stash_ids"]
        self.tattoos = performer["tattoos"]

    @dispatch(BoxPerformer)
    def load_from_box(self, performer: BoxPerformer):
        self.name = performer.name
        self.alias_list = performer["aliases"]
        self.birthdate = performer["birthdate"]
        self.career_length = performer["career_length"]
        self.country = performer["country"]
        self.death_date = performer["death_date"]
        self.disambiguation = performer["disambiguation"]
        self.ethnicity = performer["ethnicity"]
        self.eye_color = performer["eye_color"]
        self.fake_tits = performer["fake_tits"]
        self.gender = performer["gender"]
        self.hair_color = performer["hair_color"]
        self.height_cm = performer["height_cm"]
        self.image = performer["image"]
        self.measurements = performer["measurements"]
        self.piercings = performer["piercings"]
        self.stash_ids = performer["stash_ids"]
        self.tattoos = performer["tattoos"]

    @dispatch(BoxPerformer)
    def update_from_box(self, performer: BoxPerformer):
        self.id = performer["id"]
        self.name = performer["name"]
        self.alias_list = performer["aliases"]
        self.birthdate = performer["birthdate"]
        self.career_length = performer["career_length"]
        self.country = performer["country"]
        self.death_date = performer["death_date"]
        self.disambiguation = performer["disambiguation"]
        self.ethnicity = performer["ethnicity"]
        self.eye_color = performer["eye_color"]
        self.fake_tits = performer["fake_tits"]
        self.gender = performer["gender"]
        self.hair_color = performer["hair_color"]
        self.height_cm = performer["height_cm"]
        self.image = performer["image"]
        self.self.measurements = performer["measurements"]
        self.piercings = performer["piercings"]
        self.stash_ids = performer["stash_ids"]
        self.tattoos = performer["tattoos"]

