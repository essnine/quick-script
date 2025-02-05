FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN adduser -D essnine

USER essnine

RUN mkdir /home/essnine/app

WORKDIR /home/essnine/app

COPY . .

RUN uv sync --frozen --no-dev --no-install-project

EXPOSE 8000

ENV PATH="/home/essnine/app/.venv/bin:$PATH"

ENTRYPOINT [ ]

CMD [ "python", "main.py" ]
