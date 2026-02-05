# Finology - Modern Fintech Platform with RAG

A modern financial technology platform built with FastAPI, featuring AI-powered financial assistant using RAG (Retrieval Augmented Generation), financial calculators, and educational resources.

## Features

- 🤖 **AI Financial Assistant** - RAG-powered chatbot for financial queries
- 🧮 **Financial Calculators** - EMI, SIP, Future Value, Mortgage, Investment Returns
- 📚 **Learning Resources** - Comprehensive guides on investing
- 👤 **User Authentication** - Secure login/signup with JWT tokens
- 🎨 **Modern UI** - Tailwind CSS + DaisyUI with glassmorphism effects

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy (async)
- **Frontend**: Jinja2 Templates, Tailwind CSS, DaisyUI, Alpine.js
- **AI/RAG**: LangChain, ChromaDB, HuggingFace Embeddings
- **Auth**: JWT tokens, bcrypt password hashing

## Project Structure

```
finology_app/
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings & environment variables
│   ├── database.py         # Database setup
│   ├── schemas.py          # Pydantic models
│   ├── models/
│   │   └── user.py         # SQLAlchemy models
│   ├── routes/
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── calculator.py   # Calculator API
│   │   ├── chat.py         # RAG chat endpoint
│   │   └── pages.py        # HTML page routes
│   └── services/
│       ├── auth.py         # Auth utilities
│       ├── calculator.py   # Calculator logic
│       └── rag.py          # RAG service
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, JS, images
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
└── .env.example           # Environment template
```

## Installation

### 1. Clone and Navigate
```bash
cd finology_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
copy .env.example .env
# Edit .env with your settings (especially OPENAI_API_KEY for full RAG functionality)
```

### 5. Run the Application
```bash
uvicorn main:app --reload
```

Visit: http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Calculators
- `POST /api/calculator/future-value` - Calculate compound interest
- `POST /api/calculator/loan-emi` - Calculate EMI
- `POST /api/calculator/savings-plan` - Calculate savings growth
- `POST /api/calculator/mortgage` - Calculate mortgage payments
- `POST /api/calculator/investment-return` - Calculate investment returns

### AI Chat
- `POST /api/chat/ask` - Ask a financial question
- `GET /api/chat/history` - Get chat history

## RAG Configuration

The AI assistant uses RAG (Retrieval Augmented Generation) to provide accurate financial advice:

1. **Without OpenAI Key**: Uses fallback responses based on pattern matching
2. **With OpenAI Key**: Full GPT-powered responses with context retrieval

To enable full RAG:
1. Get an OpenAI API key from https://platform.openai.com
2. Add to `.env`: `OPENAI_API_KEY=your-key-here`

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (future)
pytest
```

## Screenshots

The application features a modern dark theme with:
- Glassmorphism card effects
- Gradient text and buttons
- Responsive design for all devices
- Smooth animations and transitions

## License

MIT License - Feel free to use for educational purposes.

## Authors

- Piyush Ramteke - Founder & Developer
