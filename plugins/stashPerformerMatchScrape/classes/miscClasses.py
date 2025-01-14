import json


class BodyMod:
    def __init__(self, location, description):
        self.location = location
        self.description = description

    def __str__(self):
        return json.dumps(self.__dict__)


class Measure:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance.__dict__[self._name] = value
        elif isinstance(value, list):
            output = None
            instance.__dict__[self._name] = output


class TitleCase:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value is not None:
            instance.__dict__[self._name] = str(value).title()


class Urls:
    def __init__(self, url, type):
        self.url = url
        self.type = type

    def __str__(self):
        return json.dumps(self.__dict__)
