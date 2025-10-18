install:
	uv sync && cd app/frontend && uv run npm install && uv run npm run build

collectstatic:
	uv run manage.py collectstatic

migrate:
	uv run manage.py migrate

start-backend:
	uv run manage.py runserver

start-frontend:
	cd frontend && uv run npm run dev