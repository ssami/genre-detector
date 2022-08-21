from bson import ObjectId
import pydantic
from pydantic import BaseModel, Field
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str  # https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977


class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs
    From https://stackoverflow.com/questions/63881516/objectid-object-is-not-iterable-error-while-fetching-data-from-mongodb-atlas
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class FeedbackModel(BaseModel):
    text: str
    label: str
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
