ARG NODE_VERSION="3.13.7"
ARG SLIM_VERSION="slim"

# Docker basis
# FROM python:${NODE_VERSION}-${SLIM_VERSION} AS base 
FROM python:3.13-slim AS base 
WORKDIR /app

FROM base AS build
COPY . . 

# For end of line 
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix run_flask.sh && \
    chmod +x run_flask.sh && \
    apt-get remove -y dos2unix && \
    rm -rf /var/lib/apt/lists/*


# Variables environnement Flask
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

RUN pip install -r requirements.txt 
EXPOSE 8000

# "flask", "run" 
# CMD [  "./run_flask.sh" ] 
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
