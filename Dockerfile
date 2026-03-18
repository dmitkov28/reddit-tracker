FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /var/task

COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen 

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install awslambdaric

ENTRYPOINT [".venv/bin/python", "-m", "awslambdaric"]

CMD ["src.main.lambda_handler"]