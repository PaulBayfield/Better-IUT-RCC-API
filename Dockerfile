FROM sanicframework/sanic:lts-py3.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache git

COPY . ./BetterIUTRCCAPI

WORKDIR /BetterIUTRCCAPI

RUN uv sync --frozen  --no-dev

CMD ["uv", "run", "__main__.py"]
