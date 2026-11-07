from typing import Dict, Any


class IDto:
    """Інтерфейс для перетворення доменних об'єктів у DTO (Data Transfer Object) та навпаки."""

    def put_into_dto(self) -> Dict[str, Any]:
        """Перетворює об'єкт моделі на словник DTO для JSON-відповіді."""
        raise NotImplementedError

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> object:
        """Створює об'єкт моделі зі словника DTO (JSON-запиту)."""
        raise NotImplementedError
