from typing import List, Optional, Dict, Any
from my_project import db


class GeneralDAO:
    """Базовий клас DAO (Data Access Object), який реалізує стандартні CRUD-методи роботи з БД."""

    _domain_type = None

    def find_all(self) -> List[object]:
        return db.session.query(self._domain_type).all()

    def find_by_id(self, key: int) -> Optional[object]:
        return db.session.get(self._domain_type, key)

    def create(self, obj: object) -> object:
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, key: int, in_obj: Dict[str, Any]) -> Optional[object]:
        domain_obj = db.session.get(self._domain_type, key)
        if not domain_obj:
            return None
        for col, val in in_obj.items():
            if hasattr(domain_obj, col):
                setattr(domain_obj, col, val)
        db.session.commit()
        return domain_obj

    def delete(self, key: int) -> bool:
        domain_obj = db.session.get(self._domain_type, key)
        if not domain_obj:
            return False
        db.session.delete(domain_obj)
        db.session.commit()
        return True
