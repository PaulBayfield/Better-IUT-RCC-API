from sanic import Sanic, Request
from .config import AppConfig
from .components.ratelimit import Ratelimiter
from .components.statistics import PrometheusStatistics
from .routes import RouteService, RouteBetterIUTRCC, RouteMisc
from .utils.logger import Logger
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone


load_dotenv(dotenv_path=f".env")


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
app.blueprint(RouteService)
app.blueprint(RouteBetterIUTRCC)
app.blueprint(RouteMisc)


@app.listener("before_server_start")
async def setup_app(app: Sanic, loop):
    app.ctx.logs = Logger("logs")
    app.ctx.requests = Logger("requests")
    app.ctx.logs.info("API démarrée")


@app.listener("after_server_stop")
async def close_app(app: Sanic, loop):
    await app.ctx.pool.close()
    await app.ctx.session.close()

    app.ctx.logs.info("API arrêtée")


@app.on_request
async def before_request(request: Request):
    request.ctx.start = datetime.now(timezone("Europe/Paris")).timestamp()


@app.on_response
async def after_request(request: Request, response):
    end = datetime.now(timezone("Europe/Paris")).timestamp()
    process = end - request.ctx.start

    app.ctx.requests.info(f"{request.headers.get('CF-Connecting-IP', request.client_ip)} - [{request.method}] {request.url} - {response.status} ({process * 1000:.2f}ms)")
