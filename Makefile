.PHONY: setup seed dev test lint docker-up docker-down clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing AI services dependencies..."
	cd ai-services && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Setup complete!"

seed: ## Seed database with demo data
	cd backend && python seed_crimes.py

dev: ## Start all services (backend, ai-services, frontend)
	@echo "Starting services..."
	@echo "Backend: http://localhost:8000"
	@echo "AI Services: http://localhost:8002"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@echo "Starting backend..."
	cd backend && uvicorn main:app --port 8000 --reload &
	@echo "Starting AI services..."
	cd ai-services && uvicorn main:app --port 8002 --reload &
	@echo "Starting frontend..."
	cd frontend && npm run dev

test: ## Run all tests
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v
	@echo "Running AI services tests..."
	cd ai-services && python -m pytest tests/ -v

lint: ## Lint all code
	cd frontend && npx oxlint src/

docker-up: ## Start all services with Docker Compose
	docker compose up -d
	@echo "Services starting..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend: http://localhost:8000/docs"
	@echo "AI Services: http://localhost:8002/docs"

docker-down: ## Stop all Docker services
	docker compose down

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/data/*.db
