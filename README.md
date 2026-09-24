# PocketSmart AI

Complete FastAPI + Jinja2 + SQLite + Gemini project based on the supplied PocketSmart AI documentation.

## What is included
- Home Interior Planner
- Party Budget Planner
- Jewelry Planner with optional outfit-image analysis
- Gemini integration through the current `google-genai` SDK
- Demo fallback recommendations when Gemini is not configured/unavailable
- Register/login/logout, JWT token endpoint
- Session info/data, recommendation history, recommendation detail
- Responsive frontend
- Docker support and pytest tests

## Important implementation note
The supplied document names Gemini 1.5 Flash Pro. Current Gemini API documentation lists newer supported Flash models, so the implementation keeps `GEMINI_MODEL` configurable and defaults to `gemini-2.5-flash`. Change it in `.env` if your account uses another supported model.

The project does not scrape Amazon, Flipkart, IKEA, Swiggy, Zomato, or OYO. It uses demo catalog estimates and platform search links so it remains runnable without private partner APIs. Prices are explicitly illustrative.

## Run on Windows
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Run tests
```bash
pytest -q
```

## Project structure
```text
PocketSmartAI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/{__init__.py,api.py,pages.py}
│   └── services/{__init__.py,catalog.py,gemini_service.py,recommendation_service.py}
├── templates/
├── static/{css/styles.css,js/app.js}
├── tests/test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
