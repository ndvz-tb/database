from http import HTTPStatus
from flask import Blueprint, jsonify, request, Response, make_response
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
from my_project.auth.controller import (
    office_controller,
    department_controller,
    position_controller,
    category_controller,
    brand_controller,
    pc_spec_controller,
    employee_controller,
    equipment_controller,
    employee_detail_controller,
    employee_office_controller,
    assignment_controller,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _register_crud_routes(bp: Blueprint, path: str, controller, model_cls):
    """Універсальна реєстрація CRUD-маршрутів (GET all, GET by id, POST, PUT, DELETE) для таблиці."""

    @bp.route(f"/{path}", methods=["GET"], endpoint=f"get_all_{path}")
    def get_all() -> Response:
        return make_response(jsonify(controller.find_all()), HTTPStatus.OK)

    @bp.route(f"/{path}/<int:item_id>", methods=["GET"], endpoint=f"get_by_id_{path}")
    def get_by_id(item_id: int) -> Response:
        dto = controller.find_by_id(item_id)
        if not dto:
            return make_response(jsonify({"error": f"{model_cls.__name__} not found"}), HTTPStatus.NOT_FOUND)
        return make_response(jsonify(dto), HTTPStatus.OK)

    @bp.route(f"/{path}", methods=["POST"], endpoint=f"create_{path}")
    def create_item() -> Response:
        content = request.get_json()
        obj = model_cls.create_from_dto(content)
        dto = controller.create(obj)
        return make_response(jsonify(dto), HTTPStatus.CREATED)

    @bp.route(f"/{path}/<int:item_id>", methods=["PUT"], endpoint=f"update_{path}")
    def update_item(item_id: int) -> Response:
        content = request.get_json()
        dto = controller.update(item_id, content)
        if not dto:
            return make_response(jsonify({"error": f"{model_cls.__name__} not found"}), HTTPStatus.NOT_FOUND)
        return make_response(jsonify(dto), HTTPStatus.OK)

    @bp.route(f"/{path}/<int:item_id>", methods=["DELETE"], endpoint=f"delete_{path}")
    def delete_item(item_id: int) -> Response:
        deleted = controller.delete(item_id)
        if not deleted:
            return make_response(jsonify({"error": f"{model_cls.__name__} not found"}), HTTPStatus.NOT_FOUND)
        return make_response(jsonify({"message": f"{model_cls.__name__} with ID {item_id} deleted successfully"}), HTTPStatus.OK)


# Реєстрація стандартних CRUD маршрутів для всіх 11 таблиць БД it_inventory_47
_register_crud_routes(api_bp, "offices", office_controller, Office)
_register_crud_routes(api_bp, "departments", department_controller, Department)
_register_crud_routes(api_bp, "positions", position_controller, Position)
_register_crud_routes(api_bp, "categories", category_controller, Category)
_register_crud_routes(api_bp, "brands", brand_controller, Brand)
_register_crud_routes(api_bp, "pc-specs", pc_spec_controller, PcSpec)
_register_crud_routes(api_bp, "employees", employee_controller, Employee)
_register_crud_routes(api_bp, "equipment", equipment_controller, Equipment)
_register_crud_routes(api_bp, "employee-details", employee_detail_controller, EmployeeDetail)
_register_crud_routes(api_bp, "employee-offices", employee_office_controller, EmployeeOffice)
_register_crud_routes(api_bp, "assignments", assignment_controller, Assignment)


# ==================== ЗВ'ЯЗОК M:1 (One-to-Many / Many-to-One) ====================
@api_bp.route("/departments/with-employees", methods=["GET"])
def get_departments_with_employees() -> Response:
    """Вивід даних зі сторони зв'язку M:1: для кожного відділу вивести працівників, які в ньому працюють."""
    return make_response(jsonify(department_controller.find_all_with_employees()), HTTPStatus.OK)


@api_bp.route("/positions/with-employees", methods=["GET"])
def get_positions_with_employees() -> Response:
    """Вивід даних зі сторони зв'язку M:1: для кожної посади вивести працівників."""
    return make_response(jsonify(position_controller.find_all_with_employees()), HTTPStatus.OK)


@api_bp.route("/categories/with-equipment", methods=["GET"])
def get_categories_with_equipment() -> Response:
    """Вивід даних зі сторони зв'язку M:1: для кожної категорії вивести одиниці техніки."""
    return make_response(jsonify(category_controller.find_all_with_equipment()), HTTPStatus.OK)


@api_bp.route("/brands/with-equipment", methods=["GET"])
def get_brands_with_equipment() -> Response:
    """Вивід даних зі сторони зв'язку M:1: для кожного бренду вивести одиниці техніки."""
    return make_response(jsonify(brand_controller.find_all_with_equipment()), HTTPStatus.OK)


# ==================== СТИКУВАЛЬНА ТАБЛИЦЯ M:M (Many-to-Many) ====================
@api_bp.route("/employees/with-offices", methods=["GET"])
def get_employees_with_offices() -> Response:
    """Вивід зі стикувальної таблиці M:M: для кожного працівника вивести усі офіси, які приєднані до нього."""
    return make_response(jsonify(employee_controller.find_all_with_offices()), HTTPStatus.OK)


@api_bp.route("/offices/with-employees", methods=["GET"])
def get_offices_with_employees() -> Response:
    """Вивід зі стикувальної таблиці M:M: для кожного офісу вивести усіх працівників, які приєднані до нього."""
    return make_response(jsonify(office_controller.find_all_with_employees()), HTTPStatus.OK)
