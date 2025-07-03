from sanic_ext import openapi


@openapi.component
class Theme:
    author = openapi.String(
        description="Auteur du thème",
        example="Better IUT RCC",
    )
    name = openapi.String(
        description="Nom du thème",
        example="Thème officiel de Better IUT RCC",
    )
    description = openapi.String(
        description="Description du thème",
        example="Le thème par défaut.",
    )
    version = openapi.String(
        description="Version du thème",
        example="1.0.0",
    )
    pinned = openapi.Boolean(
        description="Indique si le thème est épinglé en premier",
        example=True,
    )
    id = openapi.String(
        description="Identifiant du thème",
        example="default",
    )
    style = openapi.String(
        description="URL du fichier CSS du thème",
        example="/v1/themes/default/style.css",
    )
    preview_light = openapi.String(
        description="URL de l'aperçu du thème en mode clair",
        example="/v1/themes/default/preview-light.png",
    )
    preview_dark = openapi.String(
        description="URL de l'aperçu du thème en mode sombre",
        example="/v1/themes/default/preview-dark.png",
    )
    background_light = openapi.String(
        description="URL de l'image de fond du thème en mode clair",
        example="/v1/themes/default/background-light.png",
    )
    background_dark = openapi.String(
        description="URL de l'image de fond du thème en mode sombre",
        example="/v1/themes/default/background-dark.png",
    )
