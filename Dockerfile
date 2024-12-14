FROM sanicframework/sanic:lts-py3.11

RUN apk add --no-cache git

COPY . ./BetterIUTRCCAPI

WORKDIR /BetterIUTRCCAPI

RUN git submodule update --init --recursive

RUN git submodule foreach git pull origin main

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7001

CMD ["python", "__main__.py"]
