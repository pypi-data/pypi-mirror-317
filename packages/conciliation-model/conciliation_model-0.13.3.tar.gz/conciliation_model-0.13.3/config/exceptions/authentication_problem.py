from http import HTTPStatus

from config.exceptions.base_problem import BaseProblem


class AuthenticationProblem(BaseProblem):
    """Problemas relacionados con la autenticación del token de acceso."""

    title: str = "Problema de autenticación, acceso no autorizado."
    status: HTTPStatus = HTTPStatus.UNAUTHORIZED
