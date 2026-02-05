import os
import uuid
from typing import Optional
import httpx

import google.generativeai as genai
from openai import OpenAI
from app.config import settings

# Vector store path
CHROMA_PATH = "chroma_db"

# Financial knowledge base content
FINANCIAL_KNOWLEDGE = """
# Stock Market Investment Guide

## What is the Stock Market?
The stock market is a collection of exchanges where stocks (pieces of ownership in businesses) are bought and sold. It's a way for companies to raise money and for investors to potentially profit from company growth.

## How to Start Investing in Stocks

### Step 1: Open a Demat Account
A Demat (dematerialized) account holds your shares in electronic form. You need:
- PAN Card
- Aadhaar Card
- Bank Account
- Passport size photos
Popular brokers in India: Zerodha, Groww, Upstox, Angel One, ICICI Direct

### Step 2: Understand the Basics
- **BSE (Bombay Stock Exchange)**: India's oldest stock exchange, established in 1875
- **NSE (National Stock Exchange)**: Largest stock exchange in India by volume
- **SEBI**: Securities and Exchange Board of India - the regulator
- **Sensex**: Index of top 30 companies on BSE
- **Nifty 50**: Index of top 50 companies on NSE

### Step 3: Types of Investments
1. **Direct Stocks**: Buy shares of individual companies
2. **Mutual Funds**: Pool money with other investors, managed by professionals
3. **ETFs (Exchange Traded Funds)**: Trade like stocks but track an index
4. **SIP (Systematic Investment Plan)**: Invest fixed amount regularly

## Investment Strategies

### Value Investing
- Buy undervalued stocks
- Look for low P/E ratio
- Focus on fundamentals
- Long-term approach (5+ years)

### Growth Investing
- Focus on companies with high growth potential
- Accept higher valuations
- Technology and emerging sectors

### Dividend Investing
- Invest in companies paying regular dividends
- Generate passive income
- More stable, less volatile

## Risk Management

### Diversification
Don't put all eggs in one basket. Spread investments across:
- Different sectors (IT, Banking, Pharma, FMCG)
- Different market caps (Large cap, Mid cap, Small cap)
- Different asset classes (Stocks, Bonds, Gold, Real Estate)

### Emergency Fund
Keep 6-12 months of expenses in liquid savings before investing.

### Stop Loss
Set a price at which you'll sell to limit losses. Typically 10-15% below purchase price.

## Financial Calculators Explained

### Future Value Calculator
Calculates how much your investment will grow over time with compound interest.
Formula: FV = PV × (1 + r/n)^(n×t)
Where: PV = Present Value, r = interest rate, n = compounding frequency, t = time

### EMI Calculator
Calculates Equated Monthly Installment for loans.
Formula: EMI = P × r × (1+r)^n / ((1+r)^n - 1)
Where: P = Principal, r = monthly interest rate, n = number of months

### SIP Returns Calculator
Estimates returns from systematic investment plans.
With power of compounding, small regular investments can build significant wealth.

### Mortgage Calculator
Calculates monthly home loan payments including:
- Principal and Interest
- Property Tax
- Home Insurance
- PMI (if applicable)

## Tax Saving Investments in India

### Section 80C (up to ₹1.5 Lakh)
- ELSS Mutual Funds (3 year lock-in)
- PPF (Public Provident Fund)
- NSC (National Savings Certificate)
- Life Insurance Premiums
- 5-year Fixed Deposits

### Section 80D (Health Insurance)
- Self and family: up to ₹25,000
- Parents: additional ₹25,000-₹50,000

### Capital Gains Tax
- Short-term (held < 1 year): 15%
- Long-term (held > 1 year): 10% above ₹1 Lakh gain

## Common Mistakes to Avoid

1. **Timing the Market**: Time in the market beats timing the market
2. **Following Tips Blindly**: Do your own research
3. **Emotional Decisions**: Don't panic sell or greed buy
4. **Ignoring Fees**: Consider expense ratios and brokerage charges
5. **No Exit Strategy**: Know when to book profits or cut losses

## Finology Products

### Finology Recipe
Your personal financial planner for goal-based savings

### Finology Quest
Learn investing through gamified courses

### Finology Ticker
Track stock news and market updates

### Finology Select
Curated investment recommendations

### Finology Insider
Premium stock analysis and insights
"""

# System prompt for financial advisor
SYSTEM_PROMPT = """You are a helpful and knowledgeable financial advisor assistant. Your role is to:

1. Provide clear, accurate financial advice based on the context provided
2. Explain complex financial concepts in simple terms
3. Be specific to Indian financial markets when relevant (NSE, BSE, SEBI regulations)
4. Always remind users to consult a certified financial advisor for major decisions
5. Be helpful, friendly, and professional

Use the following knowledge base to inform your responses:

{context}

Important guidelines:
- Give practical, actionable advice
- Use examples and numbers when helpful
- If you don't know something, say so honestly
- Never recommend specific stocks without proper disclaimers
- Encourage diversification and risk management
"""


class RAGService:
    def __init__(self):
        """Initialize the AI client (OpenAI, Gemini, or Ollama based on config)"""
        self.model = None
        self.openai_client = None
        self.ollama_available = False
        self.chat_sessions = {}
        self.provider = settings.ai_provider.lower()
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "ollama":
            self._init_ollama()
        else:
            self._init_gemini()
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if settings.openai_api_key and settings.openai_api_key != "your-openai-api-key-here":
            try:
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
                print("✅ OpenAI initialized successfully!")
            except Exception as e:
                print(f"⚠️ Failed to initialize OpenAI: {e}")
                self.openai_client = None
        else:
            print("⚠️ OpenAI API key not configured. Using fallback responses.")
    
    def _init_ollama(self):
        """Initialize Ollama client"""
        try:
            # Check if Ollama is running
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5.0)
            if response.status_code == 200:
                self.ollama_available = True
                print(f"✅ Ollama initialized successfully! Model: {settings.ollama_model}")
            else:
                print("⚠️ Ollama server not responding. Using fallback responses.")
        except Exception as e:
            print(f"⚠️ Failed to connect to Ollama: {e}")
            print("   Make sure Ollama is running: ollama serve")
            self.ollama_available = False
    
    def _init_gemini(self):
        """Initialize Gemini client"""
        if settings.gemini_api_key and settings.gemini_api_key != "your-gemini-api-key-here":
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-lite",
                    system_instruction=SYSTEM_PROMPT.format(context=FINANCIAL_KNOWLEDGE)
                )
                print("✅ Gemini AI initialized successfully!")
            except Exception as e:
                print(f"⚠️ Failed to initialize Gemini: {e}")
                self.model = None
        else:
            print("⚠️ Gemini API key not configured. Using fallback responses.")
    
    def add_documents(self, texts: list[str]):
        """Add new documents to the knowledge base"""
        # Placeholder for future implementation with vector DB
        pass
    
    async def get_answer(self, question: str, session_id: Optional[str] = None) -> dict:
        """Get answer using OpenAI, Gemini, Ollama, or fallback to pattern matching"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Try OpenAI if configured
        if self.provider == "openai" and self.openai_client:
            try:
                answer = await self._get_openai_response(question, session_id)
                return {
                    "answer": answer,
                    "sources": ["OpenAI GPT-4o Financial Advisor", "Financial Knowledge Base"],
                    "session_id": session_id
                }
            except Exception as e:
                print(f"OpenAI error: {e}")
        
        # Try Ollama if configured
        elif self.provider == "ollama" and self.ollama_available:
            try:
                answer = await self._get_ollama_response(question, session_id)
                return {
                    "answer": answer,
                    "sources": [f"Ollama {settings.ollama_model} Financial Advisor", "Financial Knowledge Base"],
                    "session_id": session_id
                }
            except Exception as e:
                print(f"Ollama error: {e}")
        
        # Try Gemini if configured
        elif self.provider == "gemini" and self.model:
            try:
                answer = await self._get_gemini_response(question, session_id)
                return {
                    "answer": answer,
                    "sources": ["Gemini AI Financial Advisor", "Financial Knowledge Base"],
                    "session_id": session_id
                }
            except Exception as e:
                print(f"Gemini error: {e}")
        
        # Fallback response
        answer = self._generate_fallback_response(question, FINANCIAL_KNOWLEDGE)
        
        return {
            "answer": answer,
            "sources": ["Financial Knowledge Base"],
            "session_id": session_id
        }
    
    async def _get_ollama_response(self, question: str, session_id: str) -> str:
        """Get response from Ollama with conversation history"""
        # Get or create chat session
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT.format(context=FINANCIAL_KNOWLEDGE)}
            ]
        
        # Add user message
        self.chat_sessions[session_id].append({"role": "user", "content": question})
        
        # Get response from Ollama
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "messages": self.chat_sessions[session_id],
                    "stream": False
                }
            )
            result = response.json()
            answer = result.get("message", {}).get("content", "Sorry, I couldn't generate a response.")
        
        # Add assistant response to history
        self.chat_sessions[session_id].append({"role": "assistant", "content": answer})
        
        return answer
    
    async def _get_openai_response(self, question: str, session_id: str) -> str:
        """Get response from OpenAI with conversation history"""
        # Get or create chat session
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT.format(context=FINANCIAL_KNOWLEDGE)}
            ]
        
        # Add user message
        self.chat_sessions[session_id].append({"role": "user", "content": question})
        
        # Get response from OpenAI
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_sessions[session_id],
            max_tokens=1000,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Add assistant response to history
        self.chat_sessions[session_id].append({"role": "assistant", "content": answer})
        
        return answer
    
    async def _get_gemini_response(self, question: str, session_id: str) -> str:
        """Get response from Gemini AI with conversation history"""
        # Get or create chat session
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = self.model.start_chat(history=[])
        
        chat = self.chat_sessions[session_id]
        
        # Send message and get response
        response = chat.send_message(question)
        
        return response.text
    
    def _generate_fallback_response(self, question: str, context: str) -> str:
        """Generate a simple response when Gemini is not available"""
        question_lower = question.lower()
        
        if "demat" in question_lower:
            return "A Demat account is required to hold shares in electronic form. To open one, you need your PAN Card, Aadhaar Card, and bank account. Popular brokers include Zerodha, Groww, Upstox, and Angel One."
        
        elif "sip" in question_lower or "systematic" in question_lower:
            return "SIP (Systematic Investment Plan) allows you to invest a fixed amount regularly in mutual funds. It helps average out market volatility and builds wealth through the power of compounding."
        
        elif "tax" in question_lower or "80c" in question_lower:
            return "Under Section 80C, you can save up to ₹1.5 Lakh through investments like ELSS Mutual Funds (3-year lock-in), PPF, NSC, and life insurance premiums. Capital gains tax is 15% for short-term (<1 year) and 10% for long-term gains above ₹1 Lakh."
        
        elif "mutual fund" in question_lower:
            return "Mutual funds pool money from multiple investors to invest in diversified portfolios. They're managed by professionals and are great for beginners. Start with index funds or large-cap funds for lower risk."
        
        elif "start" in question_lower or "begin" in question_lower or "how to invest" in question_lower:
            return "To start investing: 1) Open a Demat account with a broker like Zerodha or Groww. 2) Build an emergency fund (6-12 months expenses). 3) Start with SIPs in index funds or large-cap mutual funds. 4) Gradually learn about direct stock investing."
        
        elif "risk" in question_lower:
            return "Key risk management strategies: 1) Diversify across sectors and asset classes. 2) Never invest more than you can afford to lose. 3) Use stop-loss orders. 4) Maintain an emergency fund. 5) Invest for the long term to ride out volatility."
        
        else:
            return "I'm your financial advisor assistant! I can help you with:\n\n• **Getting Started** - Opening Demat accounts, first investments\n• **SIP & Mutual Funds** - Understanding systematic investment plans\n• **Tax Saving** - Section 80C, capital gains, tax-efficient investing\n• **Risk Management** - Diversification, stop-loss strategies\n• **Stock Market Basics** - NSE, BSE, Sensex, Nifty\n\n⚠️ Note: Gemini AI is not configured. Please add your GEMINI_API_KEY to the .env file for intelligent responses.\n\nWhat would you like to know about?"


# Global RAG service instance
rag_service = RAGService()
