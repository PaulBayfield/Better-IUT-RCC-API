from .index.index import bp as RouteIndex
from .service.v1_service import bp as RouteService
from .betteriutrcc.v1_betteriutrcc import bp as RouteBetterIUTRCC
from .misc.v1_misc import bp as RouteMisc


__all__ = [
    "RouteIndex",
    "RouteService",
    "RouteBetterIUTRCC",
    "RouteMisc"
]
