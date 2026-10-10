FROM python:3.11-slim

WORKDIR /app

COPY ./files/ .

RUN pip install -r requirements.txt

RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "server.py"]
