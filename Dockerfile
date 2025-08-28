ARG NODE_VERSION="3.13.7"
ARG SLIM_VERSION="slim"

# Docker basis
FROM python:${NODE_VERSION}-${SLIM_VERSION} AS base 
WORKDIR /app

FROM base AS build
COPY . .

RUN pip install -r requirements.txt 
EXPOSE 5000

CMD ["flask", "run"]