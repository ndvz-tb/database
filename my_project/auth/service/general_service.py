from typing import List, Optional, Dict, Any


class GeneralService:
    """Базовий клас Service, який містить бізнес-логіку та викликає методи відповідного DAO."""

    _dao = None

    def find_all(self) -> List[object]:
        return self._dao.find_all()

    def find_by_id(self, key: int) -> Optional[object]:
        return self._dao.find_by_id(key)

    def create(self, obj: object) -> object:
        return self._dao.create(obj)

    def update(self, key: int, in_obj: Dict[str, Any]) -> Optional[object]:
        return self._dao.update(key, in_obj)

    def delete(self, key: int) -> bool:
        return self._dao.delete(key)
