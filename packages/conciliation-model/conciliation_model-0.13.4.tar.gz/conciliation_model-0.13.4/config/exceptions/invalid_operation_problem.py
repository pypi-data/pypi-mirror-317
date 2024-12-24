from http import HTTPStatus

from config.exceptions.base_problem import BaseProblem


class InvalidOperation(BaseProblem):
    title: str = "Invalid Operation"
    status: HTTPStatus = HTTPStatus.BAD_REQUEST
