from typing import List, Dict, Any
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service import department_service, office_service, employee_service, employee_office_service


class DepartmentController(GeneralController):
    _service = department_service

    def find_all_with_employees(self) -> List[Dict[str, Any]]:
        """Вивід зі сторони зв'язку M:1 (для кожного відділу вивести працівників)."""
        return [dept.put_into_dto_with_employees() for dept in self._service.find_all()]


class OfficeController(GeneralController):
    _service = office_service


class EmployeeController(GeneralController):
    _service = employee_service

    def find_all_with_offices(self) -> List[Dict[str, Any]]:
        """Вивід зі стикувальної таблиці M:M (для працівника вивести усі офіси та кабінети)."""
        return [emp.put_into_dto_with_offices() for emp in self._service.find_all()]


class EmployeeOfficeController(GeneralController):
    _service = employee_office_service
