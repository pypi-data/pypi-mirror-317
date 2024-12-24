from http import HTTPStatus

from config.exceptions.base_problem import BaseProblem


class InvalidDatasourceProblem(BaseProblem):
    """Problems related with Datasource validation."""

    title: str = "Fuente de datos inválida."
    status: HTTPStatus = HTTPStatus.BAD_REQUEST
