# 💰 Finology

### AI-Powered Personal Finance Learning & Calculator Platform

Finology is a fintech-style web application combining **financial calculators, educational content, authentication and an AI financial assistant**.

> **Purpose:** I created Finology to build a practical product that makes common personal-finance calculations and learning resources accessible through one interface, while experimenting with RAG-powered AI assistance.

> ⚠️ **Disclaimer:** Financial information is educational only and should not be treated as personalized investment, tax or financial advice.

## ✨ Features

| Feature | Purpose |
|---|---|
| 🤖 AI Assistant | Answers configured financial questions using the application's AI/RAG layer |
| 🧮 Calculators | SIP, EMI, FD/PPF, mortgage and investment calculations |
| 📚 Learning Hub | Financial education and investing resources |
| 🔐 Authentication | JWT-based account access with password hashing |
| 🎨 Web UI | Responsive dark/glassmorphism interface |

## 🏗️ Architecture

```text
Browser
  ↓
FastAPI Application
  ├── Authentication
  ├── Calculator Services
  ├── RAG/AI Service
  └── Page Routes
        ↓
      SQLite
```

## 🛠️ Stack

**Python · FastAPI · SQLAlchemy · SQLite · LangChain · OpenAI · Tailwind CSS · DaisyUI · Alpine.js**

## 🚀 Run Locally

```bash
git clone https://github.com/Piyu242005/Financial-Superhero.git
cd Financial-Superhero
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Configure `.env` using the repository template. For full AI functionality, configure the required AI API key.

```bash
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000`.

## 🔌 API Areas

```text
/api/auth/*
/api/calculator/*
/api/chat/*
```

## 🔐 Security

- Never commit `.env` or API keys.
- Use a strong application secret in deployment.
- Do not expose provider keys to browser code.
- Validate financial inputs server-side.
- Treat the AI assistant as informational, not authoritative financial advice.

## 📸 Screenshots

The repository contains dashboard, AI assistant, calculator, learning and authentication screenshots under `static/Website Pic/`.

## 🗺️ Roadmap

- [ ] Production database
- [ ] Better RAG evaluation and source citations
- [ ] Automated API tests
- [ ] Production deployment
- [ ] Financial-data freshness controls
- [ ] Improved security/rate limiting

## 👨‍💻 Author

**Piyush Ramteke** — Data Scientist | AI Engineer | Python Developer

GitHub: https://github.com/Piyu242005
