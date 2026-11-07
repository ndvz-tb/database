from typing import Dict, Any
from datetime import date
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Office(db.Model, IDto):
    __tablename__ = "offices"

    office_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    employee_offices = db.relationship("EmployeeOffice", back_populates="office", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="office")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "office_id": self.office_id,
            "city": self.city,
            "address": self.address,
        }

    def put_into_dto_with_employees(self) -> Dict[str, Any]:
        """Вивід зі стикувальної таблиці M:M: для офісу вивести усіх прикріплених працівників."""
        return {
            "office_id": self.office_id,
            "city": self.city,
            "address": self.address,
            "attached_employees": [
                {
                    "employee_id": eo.employee.employee_id,
                    "first_name": eo.employee.first_name,
                    "last_name": eo.employee.last_name,
                    "email": eo.employee.email,
                    "room_number": eo.room_number,
                }
                for eo in self.employee_offices if eo.employee
            ],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Office":
        return cls(
            city=dto_dict.get("city"),
            address=dto_dict.get("address"),
        )


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
        """Вивід зі сторони зв'язку M:1: для кожного відділу вивести працівників, які в ньому працюють."""
        return {
            "department_id": self.department_id,
            "name": self.name,
            "employees": [emp.put_into_dto() for emp in self.employees],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Department":
        return cls(name=dto_dict.get("name"))


class Position(db.Model, IDto):
    __tablename__ = "positions"

    position_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)

    employees = db.relationship("Employee", back_populates="position")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "position_id": self.position_id,
            "title": self.title,
        }

    def put_into_dto_with_employees(self) -> Dict[str, Any]:
        """Вивід зі сторони зв'язку M:1: для кожної посади вивести працівників."""
        return {
            "position_id": self.position_id,
            "title": self.title,
            "employees": [emp.put_into_dto() for emp in self.employees],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Position":
        return cls(title=dto_dict.get("title"))


class Category(db.Model, IDto):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    equipment_list = db.relationship("Equipment", back_populates="category")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "category_id": self.category_id,
            "name": self.name,
        }

    def put_into_dto_with_equipment(self) -> Dict[str, Any]:
        """Вивід зі сторони зв'язку M:1: для кожної категорії вивести одиниці техніки."""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "equipment": [eq.put_into_dto() for eq in self.equipment_list],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Category":
        return cls(name=dto_dict.get("name"))


class Brand(db.Model, IDto):
    __tablename__ = "brands"

    brand_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    equipment_list = db.relationship("Equipment", back_populates="brand")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "brand_id": self.brand_id,
            "name": self.name,
        }

    def put_into_dto_with_equipment(self) -> Dict[str, Any]:
        """Вивід зі сторони зв'язку M:1: для кожного бренду вивести одиниці техніки."""
        return {
            "brand_id": self.brand_id,
            "name": self.name,
            "equipment": [eq.put_into_dto() for eq in self.equipment_list],
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Brand":
        return cls(name=dto_dict.get("name"))


class PcSpec(db.Model, IDto):
    __tablename__ = "pc_specs"

    spec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_model = db.Column(db.String(100), nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    storage_gb = db.Column(db.Integer, nullable=False)

    equipment_list = db.relationship("Equipment", back_populates="pc_spec")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "spec_id": self.spec_id,
            "cpu_model": self.cpu_model,
            "ram_gb": self.ram_gb,
            "storage_gb": self.storage_gb,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "PcSpec":
        return cls(
            cpu_model=dto_dict.get("cpu_model"),
            ram_gb=dto_dict.get("ram_gb"),
            storage_gb=dto_dict.get("storage_gb"),
        )


class Employee(db.Model, IDto):
    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.department_id"), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey("positions.position_id"), nullable=False)

    department = db.relationship("Department", back_populates="employees")
    position = db.relationship("Position", back_populates="employees")
    details = db.relationship("EmployeeDetail", back_populates="employee", uselist=False, cascade="all, delete-orphan")
    employee_offices = db.relationship("EmployeeOffice", back_populates="employee", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="employee")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "position_id": self.position_id,
            "position_title": self.position.title if self.position else None,
        }

    def put_into_dto_with_offices(self) -> Dict[str, Any]:
        """Вивід зі стикувальної таблиці M:M: для працівника вивести усі офіси, які приєднані до нього."""
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
            position_id=dto_dict.get("position_id"),
        )


class Equipment(db.Model, IDto):
    __tablename__ = "equipment"

    equip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_number = db.Column(db.String(100), nullable=False, unique=True)
    inventory_number = db.Column(db.String(100), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.brand_id"), nullable=False)
    spec_id = db.Column(db.Integer, db.ForeignKey("pc_specs.spec_id"), nullable=True)

    category = db.relationship("Category", back_populates="equipment_list")
    brand = db.relationship("Brand", back_populates="equipment_list")
    pc_spec = db.relationship("PcSpec", back_populates="equipment_list")
    assignments = db.relationship("Assignment", back_populates="equipment")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "equip_id": self.equip_id,
            "serial_number": self.serial_number,
            "inventory_number": self.inventory_number,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "brand_id": self.brand_id,
            "brand_name": self.brand.name if self.brand else None,
            "spec_id": self.spec_id,
            "cpu_model": self.pc_spec.cpu_model if self.pc_spec else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Equipment":
        return cls(
            serial_number=dto_dict.get("serial_number"),
            inventory_number=dto_dict.get("inventory_number"),
            category_id=dto_dict.get("category_id"),
            brand_id=dto_dict.get("brand_id"),
            spec_id=dto_dict.get("spec_id"),
        )


class EmployeeDetail(db.Model, IDto):
    __tablename__ = "employee_details"

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id", ondelete="CASCADE"), primary_key=True)
    passport_number = db.Column(db.String(20), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    employee = db.relationship("Employee", back_populates="details")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "employee_name": f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            "passport_number": self.passport_number,
            "phone_number": self.phone_number,
            "birth_date": str(self.birth_date) if self.birth_date else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "EmployeeDetail":
        b_date = dto_dict.get("birth_date")
        if isinstance(b_date, str):
            b_date = date.fromisoformat(b_date)
        return cls(
            employee_id=dto_dict.get("employee_id"),
            passport_number=dto_dict.get("passport_number"),
            phone_number=dto_dict.get("phone_number"),
            birth_date=b_date,
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
            "employee_name": f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            "office_id": self.office_id,
            "office_city": self.office.city if self.office else None,
            "room_number": self.room_number,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "EmployeeOffice":
        return cls(
            employee_id=dto_dict.get("employee_id"),
            office_id=dto_dict.get("office_id"),
            room_number=dto_dict.get("room_number"),
        )


class Assignment(db.Model, IDto):
    __tablename__ = "assignments"

    assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equip_id = db.Column(db.Integer, db.ForeignKey("equipment.equip_id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey("offices.office_id"), nullable=True)
    issue_date = db.Column(db.Date, nullable=False)

    equipment = db.relationship("Equipment", back_populates="assignments")
    employee = db.relationship("Employee", back_populates="assignments")
    office = db.relationship("Office", back_populates="assignments")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "assignment_id": self.assignment_id,
            "equip_id": self.equip_id,
            "serial_number": self.equipment.serial_number if self.equipment else None,
            "employee_id": self.employee_id,
            "employee_name": f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            "office_id": self.office_id,
            "office_city": self.office.city if self.office else None,
            "issue_date": str(self.issue_date) if self.issue_date else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> "Assignment":
        i_date = dto_dict.get("issue_date")
        if isinstance(i_date, str):
            i_date = date.fromisoformat(i_date)
        return cls(
            equip_id=dto_dict.get("equip_id"),
            employee_id=dto_dict.get("employee_id"),
            office_id=dto_dict.get("office_id"),
            issue_date=i_date,
        )
