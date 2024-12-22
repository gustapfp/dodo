FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Dodo/dodo

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

COPY . .