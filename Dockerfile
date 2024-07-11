FROM python:3.12.4-slim AS build-image
LABEL maintainer="jesse.t.guarino@gmail.com"
LABEL stage=compiler

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential gcc software-properties-common python3-dev && \
    apt-get autoremove && \
    apt-get clean

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -U --upgrade pip
RUN pip install wheel
COPY requirements.txt .
RUN pip install -r ./requirements.txt

RUN find /opt/venv -type f -name "*.pyc" -delete 2>/dev/null
RUN find /opt/venv -type f -name "*.pyo" -delete 2>/dev/null
RUN find /opt/venv -type d -name "test" -name "tests" -delete 2>/dev/null

FROM python:3.12.4-slim AS runtime-image

COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    supervisor nano curl && \
    apt-get autoremove && \
    apt-get clean

# Logs
RUN mkdir -p /code/logs/
VOLUME /code/logs/
RUN mkdir -p /var/log/supervisor

# Supervisor
ADD deploy/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
ADD deploy/supervisor/api.conf /etc/supervisor/conf.d/api.conf

# Gunicorn
COPY deploy/gunicorn.conf.py /code/gunicorn.conf.py

# Entrypoint
COPY deploy/entrypoint.sh /code/entrypoint.sh
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Core files
COPY stuff_factory /code/stuff_factory
COPY apps /code/apps
COPY manage.py /code/manage.py

WORKDIR /code/

ENTRYPOINT ["/code/entrypoint.sh"]
HEALTHCHECK --start-period=30s --interval=10s --timeout=5s --retries=10 CMD curl --fail http://localhost:$API_SERVE_PORT/health-check/ || exit 1
