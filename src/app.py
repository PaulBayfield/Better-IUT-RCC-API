from sanic import Sanic, Request
from sanic.log import logger
from .config import AppConfig
from .components.ratelimit import Ratelimiter
from .components.statistics import PrometheusStatistics
from .routes import RouteIndex, RouteService, RouteBetterIUTRCC, RouteMisc
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone


load_dotenv(dotenv_path=".env")


# Initialisation de l'application
app = Sanic(
    name="BetterIUTRCCAPI",
    config=AppConfig(),
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
