from typing import List, Dict, Any
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import (
    office_service,
    department_service,
    position_service,
    category_service,
    brand_service,
    pc_spec_service,
    employee_service,
    equipment_service,
    employee_detail_service,
    employee_office_service,
    assignment_service,
)


class OfficeController(GeneralController):
    _service = office_service

    def find_all_with_employees(self) -> List[Dict[str, Any]]:
        """Вивід даних зі стикувальної таблиці M:M (офіси -> усі прикріплені працівники)."""
        return [off.put_into_dto_with_employees() for off in self._service.find_all()]


class DepartmentController(GeneralController):
    _service = department_service

    def find_all_with_employees(self) -> List[Dict[str, Any]]:
        """Вивід даних зі сторони зв'язку M:1 (для кожного відділу вивести його працівників)."""
        return [dept.put_into_dto_with_employees() for dept in self._service.find_all()]


class PositionController(GeneralController):
    _service = position_service

    def find_all_with_employees(self) -> List[Dict[str, Any]]:
        """Вивід даних зі сторони зв'язку M:1 (для кожної посади вивести працівників)."""
        return [pos.put_into_dto_with_employees() for pos in self._service.find_all()]


class CategoryController(GeneralController):
    _service = category_service

    def find_all_with_equipment(self) -> List[Dict[str, Any]]:
        """Вивід даних зі сторони зв'язку M:1 (для кожної категорії вивести техніку)."""
        return [cat.put_into_dto_with_equipment() for cat in self._service.find_all()]


class BrandController(GeneralController):
    _service = brand_service

    def find_all_with_equipment(self) -> List[Dict[str, Any]]:
        """Вивід даних зі сторони зв'язку M:1 (для кожного бренду вивести техніку)."""
        return [br.put_into_dto_with_equipment() for br in self._service.find_all()]


class PcSpecController(GeneralController):
    _service = pc_spec_service


class EmployeeController(GeneralController):
    _service = employee_service

    def find_all_with_offices(self) -> List[Dict[str, Any]]:
        """Вивід даних зі стикувальної таблиці M:M (для кожного працівника вивести усі його офіси)."""
        return [emp.put_into_dto_with_offices() for emp in self._service.find_all()]


class EquipmentController(GeneralController):
    _service = equipment_service


class EmployeeDetailController(GeneralController):
    _service = employee_detail_service


class EmployeeOfficeController(GeneralController):
    _service = employee_office_service


class AssignmentController(GeneralController):
    _service = assignment_service
