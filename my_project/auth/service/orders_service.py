from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao import department_dao, office_dao, employee_dao, employee_office_dao


class DepartmentService(GeneralService):
    _dao = department_dao


class OfficeService(GeneralService):
    _dao = office_dao


class EmployeeService(GeneralService):
    _dao = employee_dao


class EmployeeOfficeService(GeneralService):
    _dao = employee_office_dao
