from sanic import Sanic, Request
from sanic.log import logger
from .config import AppConfig
from .components.ratelimit import Ratelimiter
from .components.statistics import PrometheusStatistics
from .routes import RouteIndex, RouteService, RouteBetterIUTRCC, RouteMisc
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
from os import environ
from textwrap import dedent


load_dotenv(dotenv_path=".env")


# Initialisation de l'application
app = Sanic(
    name="BetterIUTRCCAPI",
    config=AppConfig(),
)

app.ext.openapi.raw(
    {
        "servers": [
            {
                "url": f"{environ.get('API_DOMAIN')}",
                "description": "Serveur de production"
            }
        ],
    }
)

year = datetime.now(
    tz=timezone("Europe/Paris")
).year

app.ext.openapi.describe(
    title=app.name,
    version=f"v{app.config.API_VERSION}",
    description=dedent(
        f"""
            # 📝 • Introduction
            L'API de Better IUT RCC permet d'accéder aux données du projet Better IUT RCC.
            ⁣  
            # 📄 • Termes d'utilisation
            Il y a quelques règles à respecter pour toute utilisation de l'API :
            - Vous ne pouvez pas utiliser l'API à des fins commerciales.
            - Vous ne pouvez pas utiliser l'API pour des activités illégales / malveillantes.
            - Vous ne devez pas abuser de l'API (limite de 200 requêtes par minute), l'utilisation de plusieurs adresses IP pour contourner cette limite est interdite.  
               
            ⁣  
            ⚠️ ***Tout abus de l'API entraînera un bannissement de l'adresse IP.***  
            ⁣  
            # 📩 • Contact
            Pour toute question, suggestion, bug, ou problème n'hésitez pas à nous contacter !  
            - E-mail : [betteriutrcc@bayfield.dev](mailto:betteriutrcc@bayfield.dev)  
            - GitHub : [github.com/PaulBayfield](https://github.com/PaulBayfield)  
              
            ⁣  
            **Paul Bayfield © 2022 - {year} | Tous droits réservés.**  
        """
    ),
)


# Ajoute les statistiques Prometheus
PrometheusStatistics(app)


# Enregistrement du rate limiter
app.ctx.ratelimiter = Ratelimiter()


# Enregistrement des routes
app.blueprint(RouteIndex)
app.blueprint(RouteService)
app.blueprint(RouteBetterIUTRCC)
app.blueprint(RouteMisc)

app.static("/static", "./static")


@app.listener("before_server_start")
async def setup_app(app: Sanic, loop):
    logger.info("Démarrage de l'API Better IUT RCC...")


@app.listener("after_server_stop")
async def close_app(app: Sanic, loop):
    logger.info("Arrêt de l'API Better IUT RCC...")


@app.on_request
async def before_request(request: Request):
    request.ctx.start = datetime.now(timezone("Europe/Paris")).timestamp()


@app.on_response
async def after_request(request: Request, response):
    end = datetime.now(timezone("Europe/Paris")).timestamp()
    process = end - request.ctx.start

    logger.info(f"{request.headers.get('CF-Connecting-IP', request.client_ip)} - [{request.method}] {request.url} - {response.status} ({process * 1000:.2f}ms)")
