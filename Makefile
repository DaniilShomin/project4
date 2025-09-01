install:
	uv sync && cd frontend && uv run npm install

migrate:
	uv run manage.py migrate

start-backend:
	uv run manage.py runserver

start-frontend:
	cd frontend && uv run npm run dev