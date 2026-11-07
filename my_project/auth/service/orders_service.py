from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao import (
    office_dao,
    department_dao,
    position_dao,
    category_dao,
    brand_dao,
    pc_spec_dao,
    employee_dao,
    equipment_dao,
    employee_detail_dao,
    employee_office_dao,
    assignment_dao,
)


class OfficeService(GeneralService):
    _dao = office_dao


class DepartmentService(GeneralService):
    _dao = department_dao


class PositionService(GeneralService):
    _dao = position_dao


class CategoryService(GeneralService):
    _dao = category_dao


class BrandService(GeneralService):
    _dao = brand_dao


class PcSpecService(GeneralService):
    _dao = pc_spec_dao


class EmployeeService(GeneralService):
    _dao = employee_dao


class EquipmentService(GeneralService):
    _dao = equipment_dao


class EmployeeDetailService(GeneralService):
    _dao = employee_detail_dao


class EmployeeOfficeService(GeneralService):
    _dao = employee_office_dao


class AssignmentService(GeneralService):
    _dao = assignment_dao
