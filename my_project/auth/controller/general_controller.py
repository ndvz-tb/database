from typing import List, Dict, Any, Optional


class GeneralController:
    """Базовий контролер, який приймає дані від Route, звертається до Service і повертає DTO-об'єкти."""

    _service = None

    def find_all(self) -> List[Dict[str, Any]]:
        return [obj.put_into_dto() for obj in self._service.find_all()]

    def find_by_id(self, key: int) -> Optional[Dict[str, Any]]:
        obj = self._service.find_by_id(key)
        return obj.put_into_dto() if obj else None

    def create(self, obj: object) -> Dict[str, Any]:
        created_obj = self._service.create(obj)
        return created_obj.put_into_dto()

    def update(self, key: int, in_obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updated_obj = self._service.update(key, in_obj)
        return updated_obj.put_into_dto() if updated_obj else None

    def delete(self, key: int) -> bool:
        return self._service.delete(key)
