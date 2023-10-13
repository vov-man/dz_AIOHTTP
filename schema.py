import typing
import pydantic


class CreateAdvertisements(pydantic.BaseModel):
    title: str
    description: str
    creator: str

    @pydantic.validator("description")
    def secure_description(self, value):
        if len(value) < 5:
            raise ValueError("the description is too short")
        return value

    @pydantic.validator("creator")
    def secure_creator(self, value):
        if len(value) < 1:
            raise ValueError("you need to log in")
        return value


class UpdateAdvertisements(pydantic.BaseModel):
    title: typing.Optional[str]
    description: typing.Optional[str]
    creator: str

    @pydantic.validator("description")
    def secure_description(self, value):
        if len(value) < 5:
            raise ValueError("the description is too short")
        return value

    @pydantic.validator("creator")
    def secure_creator(self, value):
        if len(value) < 1:
            raise ValueError("you need to log in")
        return value
