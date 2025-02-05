FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN mkdir /root/app

WORKDIR /root/app

COPY . .

RUN uv sync --frozen --no-dev --no-install-project

EXPOSE 80

ENV PATH="/root/app/.venv/bin:$PATH"

ENTRYPOINT [ ]

CMD [ "python", "main.py" ]
