FROM python:3.10.12-slim

LABEL author=fx

ARG APP_HOME=/app
WORKDIR $APP_HOME

ADD . $APP_HOME

RUN apt-get update && \
    apt-get install -y libglib2.0-dev && \
    pip install -r $APP_HOME/requirements.txt && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

ENTRYPOINT ["python", "main.py"]