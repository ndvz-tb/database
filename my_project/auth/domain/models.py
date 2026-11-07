from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Department(db.Model, IDto):
    __tablename__ = "departments"

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    employees = db.relationship("Employee", back_populates="department")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "department_id": self.department_id,
            "name": self.name,
        }

    def put_into_dto_with_employees(self) -> Dict[str, Any]:
        """Вимога методички (M:1): для відділу вивести список працівників, які в ньому працюють."""
        return {
            "department_id": self.department_id,
            "name": self.name,
            "employees": [emp.put_into_dto() for emp in self.employees],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Department":
        return cls(name=dto_dict.get("name"))


class Office(db.Model, IDto):
    __tablename__ = "offices"

    office_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    employee_offices = db.relationship("EmployeeOffice", back_populates="office", cascade="all, delete-orphan")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "office_id": self.office_id,
            "city": self.city,
            "address": self.address,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Office":
        return cls(
            city=dto_dict.get("city"),
            address=dto_dict.get("address"),
        )


class Employee(db.Model, IDto):
    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.department_id"), nullable=False)
    position_id = db.Column(db.Integer, nullable=False, default=1)

    department = db.relationship("Department", back_populates="employees")
    employee_offices = db.relationship("EmployeeOffice", back_populates="employee", cascade="all, delete-orphan")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
        }

    def put_into_dto_with_offices(self) -> Dict[str, Any]:
        """Вимога методички (M:M): для працівника вивести усі офіси та кабінети, закріплені за ним."""
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "attached_offices": [
                {
                    "office_id": eo.office.office_id,
                    "city": eo.office.city,
                    "address": eo.office.address,
                    "room_number": eo.room_number,
                }
                for eo in self.employee_offices if eo.office
            ],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Employee":
        return cls(
            first_name=dto_dict.get("first_name"),
            last_name=dto_dict.get("last_name"),
            email=dto_dict.get("email"),
            department_id=dto_dict.get("department_id"),
            position_id=dto_dict.get("position_id", 1),
        )


class EmployeeOffice(db.Model, IDto):
    __tablename__ = "employee_offices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("offices.office_id"), nullable=False)
    room_number = db.Column(db.String(50), nullable=False)

    employee = db.relationship("Employee", back_populates="employee_offices")
    office = db.relationship("Office", back_populates="employee_offices")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "office_id": self.office_id,
            "room_number": self.room_number,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "EmployeeOffice":
        return cls(
            employee_id=dto_dict.get("employee_id"),
            office_id=dto_dict.get("office_id"),
            room_number=dto_dict.get("room_number"),
        )
