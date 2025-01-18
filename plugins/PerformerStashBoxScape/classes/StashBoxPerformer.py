from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Self

from classes.StashAppPerformer import StashAppPerformerUpdate, StashId


# @dataclass
class BirthData(BaseModel):
    date: Optional[datetime] = None
    accuracy: Optional[str] = ""


# @dataclass
class BodyMod(BaseModel):
    location: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        if self.location is not None and self.description is not None:
            return f"{self.location}, {self.description}"
        elif self.location is not None:
            return f"{self.location}"
        elif self.description is not None:
            return f"{self.description}"
        return None


# @dataclass
class ImageData(BaseModel):
    url: str


# @dataclass
class UrlData(BaseModel):
    url: str
    type: str


# @dataclass
class StashBoxPerformer(BaseModel):
    id: Optional[str] = ""
    name: Optional[str] = ""
    disambiguation: Optional[str] = ""
    aliases: List[str] = []
    gender: Optional[str] = ""
    urls: List[UrlData] = []
    birthdate: Optional[BirthData] = None
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    age: Optional[int] = None
    ethnicity: Optional[str] = ""
    country: Optional[str] = ""
    eye_color: Optional[str] = ""
    hair_color: Optional[str] = ""
    height: Optional[int] = None
    cup_size: Optional[str] = ""
    band_size: Optional[int] = None
    waist_size: Optional[int] = None
    hip_size: Optional[int] = None
    breast_type: Optional[str] = ""
    career_start_year: Optional[int] = None
    career_end_year: Optional[int] = None
    tattoos: Optional[List[BodyMod]] = []
    piercings: Optional[List[BodyMod]] = []
    images: Optional[List[ImageData]] = []
    is_favorite: bool = False

    def exportToStash(self) -> StashAppPerformerUpdate:
        export = StashAppPerformerUpdate()
        export.name = self.name
        export.disambiguation = self.disambiguation
        export.urls = list(map(lambda u: u.url, self.urls))
        export.gender = self.gender
        if self.birthdate and self.birthdate.date:
            export.birthdate = self.birthdate.date.strftime("%Y-%m-%d")
        export.ethnicity = self.ethnicity.title() if self.ethnicity else None
        export.country = self.country
        export.eye_color = self.eye_color.title() if self.eye_color else None
        export.height_cm = self.height
        export.measurements = (
            f"{self.band_size}{self.cup_size}-{self.waist_size}-{self.hip_size}"
            if self.band_size and self.cup_size and self.waist_size and self.hip_size
            else (
                f"{self.band_size}{self.cup_size}"
                if self.band_size and self.cup_size
                else None
            )
        )
        export.fake_tits = self.breast_type.title() if self.breast_type else None
        export.career_length = (
            f"{self.career_start_year} - {self.career_end_year}"
            if self.career_end_year
            else f"{self.career_start_year} -"
        )
        export.tattoos = (
            ""
            if self.tattoos is None
            else "; ".join(
                list(map(lambda t: "" if t is None else t.__str__(), self.tattoos))
            )
        )
        export.piercings = (
            ""
            if self.piercings is None
            else "; ".join(
                list(map(lambda p: "" if p is None else p.__str__(), self.piercings))
            )
        )
        export.alias_list = self.aliases
        export.image = self.images[0].url if self.images[0] else None
        export.death_date = self.death_date
        export.hair_color = self.hair_color.title() if self.hair_color else None
        return export

    def update(self, performer: Self):
        self.id = performer.id if performer.id else self.id
        self.name = performer.name if performer.name else self.name
        self.disambiguation = (
            performer.disambiguation
            if performer.disambiguation
            else self.disambiguation
        )
        self.aliases = performer.aliases if performer.aliases else self.aliases
        self.gender = performer.gender if performer.gender else self.gender
        self.urls = performer.urls if performer.urls else self.urls
        self.birthdate = performer.birthdate if performer.birthdate else self.birthdate
        self.birth_date = (
            performer.birth_date if performer.birth_date else self.birth_date
        )
        self.death_date = (
            performer.death_date if performer.death_date else self.death_date
        )
        self.age = performer.age if performer.age else self.age
        self.ethnicity = performer.ethnicity if performer.ethnicity else self.ethnicity
        self.country = performer.country if performer.country else self.country
        self.eye_color = performer.eye_color if performer.eye_color else self.eye_color
        self.hair_color = (
            performer.hair_color if performer.hair_color else self.hair_color
        )
        self.height = performer.height if performer.height else self.height
        self.cup_size = performer.cup_size if performer.cup_size else self.cup_size
        self.band_size = performer.band_size if performer.band_size else self.band_size
        self.waist_size = (
            performer.waist_size if performer.waist_size else self.waist_size
        )
        self.hip_size = performer.hip_size if performer.hip_size else self.hip_size
        self.breast_type = (
            performer.breast_type if performer.breast_type else self.breast_type
        )
        self.career_start_year = (
            performer.career_start_year
            if performer.career_start_year
            else self.career_start_year
        )
        self.career_end_year = (
            performer.career_end_year
            if performer.career_end_year
            else self.career_end_year
        )
        self.tattoos = performer.tattoos if performer.tattoos else self.tattoos
        self.piercings = performer.piercings if performer.piercings else self.piercings
        self.images = performer.images if performer.images else self.images
        self.is_favorite = (
            performer.is_favorite if performer.is_favorite else self.is_favorite
        )
