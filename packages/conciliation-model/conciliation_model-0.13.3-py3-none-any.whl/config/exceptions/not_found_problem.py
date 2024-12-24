from http import HTTPStatus

from config.exceptions.base_problem import BaseProblem


class NotFound(BaseProblem):
    title: str = "Not Found"
    status: HTTPStatus = HTTPStatus.NOT_FOUND
