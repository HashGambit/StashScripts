from pydantic import BaseModel, computed_field
from typing import List, Optional, Self


class StashId(BaseModel):
    endpoint: str
    stash_id: str


class Tag(BaseModel):
    id: int
    name: str


class StashAppPerformer(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    disambiguation: Optional[str] = None
    urls: Optional[List[str]] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    ethnicity: Optional[str] = None
    country: Optional[str] = None
    eye_color: Optional[str] = None
    height_cm: Optional[int] = None
    measurements: Optional[str] = None
    fake_tits: Optional[str] = None
    career_length: Optional[str] = None
    tattoos: Optional[str] = None
    piercings: Optional[str] = None
    alias_list: Optional[List[str]] = []
    favorite: Optional[bool] = False
    tags: Optional[List[Tag]] = []
    image_path: Optional[str] = None
    stash_ids: Optional[List[StashId]] = []
    details: Optional[str] = None
    death_date: Optional[str] = None
    hair_color: Optional[str] = None
    weight: Optional[int] = None


class StashAppPerformerUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    disambiguation: Optional[str] = None
    urls: Optional[List[str]] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    ethnicity: Optional[str] = None
    country: Optional[str] = None
    eye_color: Optional[str] = None
    height_cm: Optional[int] = None
    measurements: Optional[str] = None
    fake_tits: Optional[str] = None
    career_length: Optional[str] = None
    tattoos: Optional[str] = None
    piercings: Optional[str] = None
    alias_list: Optional[List[str]] = []
    favorite: Optional[bool] = False
    tag_ids: Optional[List[Tag]] = []
    image: Optional[str] = None
    stash_ids: Optional[List[StashId]] = []
    details: Optional[str] = None
    death_date: Optional[str] = None
    hair_color: Optional[str] = None
    weight: Optional[int] = None

    def update(self, input: Self, force=False):
        self.name = input.name if self.name is None else self.name
        self.disambiguation = (
            input.disambiguation if self.disambiguation is None else self.disambiguation
        )
        self.urls = input.urls if self.urls is None else self.urls
        self.gender = input.gender if self.gender is None else self.gender
        self.birthdate = input.birthdate if self.birthdate is None else self.birthdate
        self.ethnicity = input.ethnicity if self.ethnicity is None else self.ethnicity
        self.country = input.country if self.country is None else self.country
        self.eye_color = input.eye_color if self.eye_color is None else self.eye_color
        self.height_cm = input.height_cm if self.height_cm is None else self.height_cm
        self.measurements = (
            input.measurements if self.measurements is None else self.measurements
        )
        self.fake_tits = input.fake_tits if self.fake_tits is None else self.fake_tits
        self.career_length = (
            input.career_length if self.career_length is None else self.career_length
        )
        self.tattoos = input.tattoos if self.tattoos is None else self.tattoos
        self.piercings = input.piercings if self.piercings is None else self.piercings
        self.alias_list = (
            input.alias_list if self.alias_list is None else self.alias_list
        )
        self.favorite = input.favorite if self.favorite is None else self.favorite
        self.tag_ids = input.tag_ids if self.tag_ids is None else self.tag_ids
        self.image = input.image if self.image is None else self.image
        self.stash_ids = input.stash_ids if self.stash_ids is None else self.stash_ids
        self.details = input.details if self.details is None else self.details
        self.death_date = (
            input.death_date if self.death_date is None else self.death_date
        )
        self.hair_color = (
            input.hair_color if self.hair_color is None else self.hair_color
        )
        self.weight = input.weight if self.weight is None else self.weight
