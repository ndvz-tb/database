from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.models import Department, Office, Employee, EmployeeOffice


class DepartmentDAO(GeneralDAO):
    _domain_type = Department


class OfficeDAO(GeneralDAO):
    _domain_type = Office


class EmployeeDAO(GeneralDAO):
    _domain_type = Employee


class EmployeeOfficeDAO(GeneralDAO):
    _domain_type = EmployeeOffice
