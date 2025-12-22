FROM python:3.13.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app"

RUN apt update &&  \
    apt install -y curl &&  \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/src

COPY ./src ./
COPY ./pyproject.toml ./
COPY ./uv.lock ./

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install uv && \
    uv pip install --system -r pyproject.toml
