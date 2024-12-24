from http import HTTPStatus
from typing import Annotated

from pydantic import Field

from config.exceptions.base_problem import BaseProblem


class RequestValidationProblem(BaseProblem):
    """Este problema se utiliza para indicar que la petición no pudo ser procesada debido a errores de validación

    Ejemplo
    ```

    {
        "title": "Problema de validación de la petición.",
        "status": 422,
        "errors": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]

    }
    ```
    """

    title: str = "Problema de validación de la petición."
    status: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY
    errors: Annotated[list, Field(description="Lista de errores de validación.")]
