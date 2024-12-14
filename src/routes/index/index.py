from ...components.ratelimit import ratelimit
from sanic.response import HTTPResponse
from sanic import Blueprint, Request
from sanic_ext import openapi, render


bp = Blueprint(
    name="Index"
)


# /
@bp.route("/", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getHomePage(request: Request) -> HTTPResponse:
    """
    Retourne la page d'accueil.

    :return: La page d'accueil
    """
    return await render(
        "index.html"
    )
