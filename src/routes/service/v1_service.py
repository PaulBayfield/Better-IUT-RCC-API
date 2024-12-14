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
@openapi.no_autodoc
@openapi.exclude()
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
