from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.models import (
    Office,
    Department,
    Position,
    Category,
    Brand,
    PcSpec,
    Employee,
    Equipment,
    EmployeeDetail,
    EmployeeOffice,
    Assignment,
)


class OfficeDAO(GeneralDAO):
    _domain_type = Office


class DepartmentDAO(GeneralDAO):
    _domain_type = Department


class PositionDAO(GeneralDAO):
    _domain_type = Position


class CategoryDAO(GeneralDAO):
    _domain_type = Category


class BrandDAO(GeneralDAO):
    _domain_type = Brand


class PcSpecDAO(GeneralDAO):
    _domain_type = PcSpec


class EmployeeDAO(GeneralDAO):
    _domain_type = Employee


class EquipmentDAO(GeneralDAO):
    _domain_type = Equipment


class EmployeeDetailDAO(GeneralDAO):
    _domain_type = EmployeeDetail


class EmployeeOfficeDAO(GeneralDAO):
    _domain_type = EmployeeOffice


class AssignmentDAO(GeneralDAO):
    _domain_type = Assignment
