FROM python:3.14-alpine
COPY . /app
WORKDIR /app
EXPOSE 8001
RUN apk upgrade --no-cache
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]