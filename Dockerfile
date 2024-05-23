FROM python:3.10-bullseye

WORKDIR /app

RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY requirements/backend.txt requirements.txt

RUN pip install --no-cache-dir -r requirements/backend.txt
EXPOSE 8080

COPY . .

CMD ["uvicorn", "spaceship.main:app", "--host=0.0.0.0", "--port=8080"]