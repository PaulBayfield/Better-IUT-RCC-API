from ...components.ratelimit import ratelimit
from sanic.response import JSONResponse, json
from sanic import Blueprint, Request
from sanic_ext import openapi


bp = Blueprint(
    name="Service",
    version=1,
    version_prefix="v"
)


# /status
@bp.route("/status", methods=["GET"])
@openapi.definition(
    summary="Statut de l'API",
    description="Retourne le statut de l'API.",
    tag="Service"
)
@openapi.response(
    status=200,
    content={
        "application/json": openapi.Object(
            properties={
                "success": openapi.Boolean(description="Indique si l'API est en ligne.", example=True),
                "message": openapi.String(description="Message de statut.", example="L'API est en ligne.")
            },
            description="Statut de l'API."
        )
    },
    description="L'API est en ligne."
)
@openapi.response(
    status=429,
    content={
        "application/json": openapi.String(
            description="Statut de la requête",
            example="Vous avez envoyé trop de requêtes. Veuillez réessayer plus tard."
        )
    },
    description="Trop de requêtes, veuillez réessayer plus tard."
)
@ratelimit()
async def getStatus(request: Request) -> JSONResponse:
    """
    Retourne le statut de l'API.

    :return: JSONResponse
    """
    return json(
        {
            "success": True,
            "message": "L'API est en ligne."
        },
        status=200
    )
