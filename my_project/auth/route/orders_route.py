from http import HTTPStatus
from flask import Blueprint, jsonify, request, Response, make_response
from my_project.auth.domain.models import Department, Office, Employee, EmployeeOffice
from my_project.auth.controller import (
    department_controller,
    office_controller,
    employee_controller,
    employee_office_controller,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _register_crud_routes(bp: Blueprint, path: str, controller, model_cls):
    """Реєстрація 5 обов'язкових CRUD-маршрутів (GET all, GET by id, POST, PUT, DELETE)."""

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


# CRUD-маршрути для основних таблиць
_register_crud_routes(api_bp, "offices", office_controller, Office)
_register_crud_routes(api_bp, "employees", employee_controller, Employee)
_register_crud_routes(api_bp, "departments", department_controller, Department)
_register_crud_routes(api_bp, "employee-offices", employee_office_controller, EmployeeOffice)


# ==================== ЗВ'ЯЗОК M:1 (One-to-Many) ====================
@api_bp.route("/departments/with-employees", methods=["GET"])
def get_departments_with_employees() -> Response:
    """Вимога методички: вивід зі сторони зв'язку M:1 (для кожного відділу вивести працівників)."""
    return make_response(jsonify(department_controller.find_all_with_employees()), HTTPStatus.OK)


# ==================== СТИКУВАЛЬНА ТАБЛИЦЯ M:M (Many-to-Many) ====================
@api_bp.route("/employees/with-offices", methods=["GET"])
def get_employees_with_offices() -> Response:
    """Вимога методички: вивід зі стикувальної таблиці зв'язку M:M (для працівника вивести його офіси)."""
    return make_response(jsonify(employee_controller.find_all_with_offices()), HTTPStatus.OK)
