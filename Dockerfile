# ================== BUILD =================
FROM python:3.11.9-slim-bookworm AS builder

RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    libpq-dev gcc build-essential

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements/* ./requirements/
RUN pip install -r requirements/common.txt

COPY app ./app/
COPY migrations ./migrations/
COPY config.py manage.py gunicorn_config.py ./

COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

# ================== PRODUCTION =================
FROM builder AS production

RUN pip install -r requirements/prod.txt

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "-c", "python:gunicorn_config", "manage:app"]

# ================== DEVELOPMENT =================
FROM builder as development

RUN pip install -r requirements/dev.txt

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["flask", "run", "--host", "0.0.0.0"]
