from typing import TYPE_CHECKING, Literal, TypeVar

if TYPE_CHECKING:
    from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound="BaseModel")

Language = Literal["json", "yaml"]
