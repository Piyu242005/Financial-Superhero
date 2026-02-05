import os
import uuid
from typing import Optional

from app.config import settings

# Simplified version without heavy dependencies
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


class RAGService:
    def __init__(self):
        # Simplified initialization without heavy ML dependencies
        pass
    
    def add_documents(self, texts: list[str]):
        """Add new documents to the knowledge base"""
        # Placeholder for future implementation
        pass
    
    async def get_answer(self, question: str, session_id: Optional[str] = None) -> dict:
        """Get answer using pattern matching fallback"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        answer = self._generate_fallback_response(question, FINANCIAL_KNOWLEDGE)
        
        sources = ["Financial Knowledge Base"]
        
        return {
            "answer": answer,
            "sources": sources,
            "session_id": session_id
        }
    
    def _generate_fallback_response(self, question: str, context: str) -> str:
        """Generate a simple response when LLM is not available"""
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
            return f"Based on the context I have:\n\n{context[:500]}...\n\nFor more specific advice, please consult a certified financial advisor. Would you like to know about SIP investing, opening a Demat account, or tax-saving investments?"


# Global RAG service instance
rag_service = RAGService()
