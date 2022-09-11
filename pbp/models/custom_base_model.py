from pydantic import BaseModel


def to_camel(string: str) -> str:
    words = [word for word in string.split('_')]
    return ''.join([word.capitalize() if words.index(word) != 0 else word for word in words])


class CustomBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True