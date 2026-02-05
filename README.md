<div align="center">

# 💰 FINOLOGY

### *Your AI-Powered Financial Companion*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square" alt="Made with Love">
</p>

---

**Finology is a modern fintech platform designed to simplify personal finance. Featuring smart calculators for SIP, EMI, FD, PPF & tax planning, an AI-powered chatbot for instant financial guidance, and comprehensive learning resources.**

[🚀 Live Demo](#) • [📖 Documentation](#installation) • [🐛 Report Bug](https://github.com/Piyu242005/finology/issues)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI Financial Assistant
RAG-powered chatbot providing instant, accurate answers to all your financial queries

### 🧮 Smart Calculators
- 📊 SIP Calculator
- 💳 EMI Calculator  
- 🏦 FD/PPF Calculator
- 🏠 Mortgage Calculator
- 📈 Investment Returns

</td>
<td width="50%">

### 📚 Learning Hub
Comprehensive guides on investing, mutual funds, taxes, and wealth building

### 🔐 Secure Authentication
JWT-based auth with bcrypt password hashing for maximum security

### 🎨 Modern UI/UX
Glassmorphism design with dark theme, smooth animations & responsive layout

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technologies |
|:---:|:---|
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) |
| **Frontend** | ![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) ![DaisyUI](https://img.shields.io/badge/DaisyUI-5A0EF8?style=flat-square&logo=daisyui&logoColor=white) ![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=flat-square&logo=alpine.js&logoColor=black) |
| **AI/ML** | ![LangChain](https://img.shields.io/badge/LangChain-121212?style=flat-square&logo=chainlink&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) |

</div>

---

## 📁 Project Structure

```
📦 finology_app
├── 📂 app
│   ├── 📄 config.py           # ⚙️ Settings & environment
│   ├── 📄 database.py         # 🗄️ Database setup
│   ├── 📄 schemas.py          # 📋 Pydantic models
│   ├── 📂 models
│   │   └── 📄 user.py         # 👤 User model
│   ├── 📂 routes
│   │   ├── 📄 auth.py         # 🔐 Authentication
│   │   ├── 📄 calculator.py   # 🧮 Calculator API
│   │   ├── 📄 chat.py         # 💬 RAG Chat
│   │   └── 📄 pages.py        # 📄 Page routes
│   └── 📂 services
│       ├── 📄 auth.py         # 🔑 Auth utilities
│       ├── 📄 calculator.py   # 📊 Calculator logic
│       └── 📄 rag.py          # 🤖 RAG service
├── 📂 templates               # 🎨 Jinja2 templates
├── 📂 static                  # 🖼️ Assets
├── 📄 main.py                 # 🚀 Entry point
└── 📄 requirements.txt        # 📦 Dependencies
```

---

## 🚀 Installation

<details>
<summary><b>📋 Prerequisites</b></summary>

- Python 3.10 or higher
- pip package manager
- Git

</details>

### Quick Start

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Piyu242005/finology.git
cd finology_app

# 2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment
copy .env.example .env
# Edit .env with your settings

# 5️⃣ Launch the app 🚀
uvicorn main:app --reload --port 8000
```

<div align="center">

### 🎉 Open [http://localhost:8000](http://localhost:8000) and start exploring!

</div>

---

## 📡 API Reference

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/api/auth/signup` | Register new user |
| `POST` | `/api/auth/login` | Login & get token |
| `POST` | `/api/auth/logout` | Logout |
| `GET` | `/api/auth/me` | Get current user |

</details>

<details>
<summary><b>🧮 Calculators</b></summary>

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/api/calculator/future-value` | Compound interest |
| `POST` | `/api/calculator/loan-emi` | EMI calculation |
| `POST` | `/api/calculator/savings-plan` | Savings growth |
| `POST` | `/api/calculator/mortgage` | Mortgage payments |
| `POST` | `/api/calculator/investment-return` | ROI calculation |

</details>

<details>
<summary><b>🤖 AI Chat</b></summary>

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/api/chat/ask` | Ask financial question |
| `GET` | `/api/chat/history` | Get chat history |

</details>

---

## 🤖 AI Configuration

The AI assistant uses **RAG (Retrieval Augmented Generation)** for accurate financial advice:

| Mode | Description |
|:---:|:---|
| **Basic** | Pattern-matching fallback responses (no API key needed) |
| **Full AI** | GPT-powered with context retrieval (requires OpenAI key) |

```bash
# To enable full AI capabilities:
# Add to your .env file:
OPENAI_API_KEY=your-openai-api-key-here
```

---

## 🎨 Screenshots

<div align="center">

| Feature | Preview |
|:---:|:---:|
| 🏠 **Dashboard** | Modern glassmorphism design |
| 🧮 **Calculators** | Interactive financial tools |
| 💬 **AI Chat** | Real-time financial guidance |
| 📱 **Responsive** | Works on all devices |

</div>

---

## 🤝 Contributing

Contributions are always welcome! 

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">

## 👨‍💻 Author

<a href="https://github.com/Piyu242005">
  <img src="https://github.com/Piyu242005.png" width="200" alt="Piyush Ramteke">
</a>

<br>

### **Piyush Ramteke**
*Founder & Developer*

<p align="center">
  <i>"Empowering financial literacy through technology"</i>
</p>

<br>

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Piyu242005)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/piyu24)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/my.life_24143/)

---

<p align="center">
  <b>⭐ Star this repo if you found it helpful! ⭐</b>
</p>

<p align="center">
  Made with ❤️ by Piyu | © 2026 Finology
</p>

</div>
