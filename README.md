# Expense Intellect
AI-powered expense management for Hack Genesis '25.

## Setup
1. Download datasets to backend/data/ (links in history).
2. Run `python backend/train.py`.
3. `docker-compose up --build`.
4. Backend: http://localhost:8000/docs
5. Frontend: http://localhost:3000

## Roadmap Extensions
- Phase 1: Add React Native for mobile, multi-tenant with user auth (FastAPI Users).
- Phase 2: API endpoints for QuickBooks/Zoho integration.
- Phase 3: Add Prophet in train.py for forecasting.

For security: Add JWT auth, encryption (e.g., Fernet).