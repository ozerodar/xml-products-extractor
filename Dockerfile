FROM python:3.11-slim
LABEL maintainer="Daria"

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
EXPOSE 80

COPY ./requirements.txt /tmp/requirements.txt
COPY --chown=999 start.sh ./start.sh
COPY ./app /app
COPY ./tests /tests
WORKDIR /

RUN apt-get update
RUN chmod +x ./start.sh
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"

CMD ["./start.sh"]
