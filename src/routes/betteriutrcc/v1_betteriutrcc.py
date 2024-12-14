import os

from ...components.ratelimit import ratelimit
from sanic.response import HTTPResponse, file, json
from sanic import Blueprint, Request
from sanic_ext import openapi, render
from datetime import datetime
from pytz import timezone
from json import loads


bp = Blueprint(
    name="BetterIUTRCC",
    version=1,
    version_prefix="v"
)


# /assets/style.css
@bp.route("/assets/style.css", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getPageStyle(request: Request) -> HTTPResponse:
    """
    Retourne le style de la page.

    :return: Le style de la page
    """
    return await file(
        location="./static/app.css"
    )


# /menu
@bp.route("/menu", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getMenu(request: Request) -> HTTPResponse:
    """
    Retourne le menu de la page.

    :return: Le menu de la page
    """
    return await render(
        "crous.html",
        context={
            "theme": request.args.get("theme", "light").lower() if request.args.get("theme", "light").lower() in ["light", "dark"] else "light",
            "date": datetime.now(timezone("Europe/Paris")).strftime("%d-%m-%Y")
        }
    )


# /themes
@bp.route("/themes", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getThemes(request: Request) -> HTTPResponse:
    """
    Retourne la liste des thèmes disponibles.

    :return: La liste des thèmes disponibles
    """
    themes = []

    for theme in os.listdir("./themes"):
        with open(f"./themes/{theme}/metadata.json", "r", encoding="utf-8") as f:
            metadata = loads(f.read())
            metadata["style"] = "/v1/themes/" + theme + "/style.css"
            metadata["preview-light"] = "/v1/themes/" + theme + "/preview-light.png"
            metadata["preview-dark"] = "/v1/themes/" + theme + "/preview-dark.png"
            themes.append(metadata)

    return json(
        themes
    )


# /themes/<theme>/style.css
@bp.route("/themes/<theme>/style.css", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getThemeStyle(request: Request, theme: str) -> HTTPResponse:
    """
    Retourne le style du thème.

    :param theme: Le nom du thème
    :return: Le style du thème
    """
    return await file(
        location=f"./themes/{theme}/style.css"
    )


# /themes/<theme>/preview-light.png
@bp.route("/themes/<theme>/preview-light.png", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getThemePreview(request: Request, theme: str) -> HTTPResponse:
    """
    Retourne l'aperçu du thème.

    :param theme: Le nom du thème
    :return: L'aperçu du thème
    """
    return await file(
        location=f"./themes/{theme}/preview-light.png"
    )


# /themes/<theme>/preview-dark.png
@bp.route("/themes/<theme>/preview-dark.png", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
@ratelimit()
async def getThemePreviewDark(request: Request, theme: str) -> HTTPResponse:
    """
    Retourne l'aperçu du thème en mode sombre.

    :param theme: Le nom du thème
    :return: L'aperçu du thème en mode sombre
    """
    return await file(
        location=f"./themes/{theme}/preview-dark.png"
    )
