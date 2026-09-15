FROM python:3.14-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y curl && pip install Flask
EXPOSE 8000
CMD ["flask", "--app", "app:create_app()", "run", "--host=0.0.0.0", "--port=8000"]