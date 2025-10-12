FROM python:3.13-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY . .

RUN uv sync

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]