from typing import Any, TYPE_CHECKING
from abc import ABC, abstractmethod

from pydantic import BaseModel


if TYPE_CHECKING:
    from ..application import Application


__all__ = (
    'PluralModel',
    'EditableBase',
)


class PluralClientState:
    _app: Application | None = None


class PluralModel(BaseModel, PluralClientState):
    class Config:
        json_encoders = {
            set: list
        }

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.__raw_data = data.copy()

    @property
    def _raw(self) -> dict[str, Any]:
        return self.__raw_data


class EditableBase(ABC):
    @abstractmethod
    async def edit(self) -> None:
        """Edit the object. This docstring should be overridden."""
        pass
