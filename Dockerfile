FROM python:3.9-alpine
# TODO: create minimialic image for tests by using alpine distribution
RUN   apk update && \
      apk add --no-cache

ENV PYTHONUNBUFFERED=1

EXPOSE 22

WORKDIR /
