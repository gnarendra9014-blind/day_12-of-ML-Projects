# 📈 Day 12 — AI Stock Research Agent

> **25-Day AI Challenge** | Stack: **Groq + yFinance** | Pattern: **Agent**

An AI-powered stock research agent that fetches real-time market data, calculates technical indicators, and generates a comprehensive investment research report using LLaMA 3 via Groq.

---

## 🚀 What It Does

Given any stock ticker, the agent automatically:

1. **Fetches live stock data** — price, market cap, P/E ratio, 52-week range, analyst targets, and recent news via yFinance
2. **Calculates technical indicators** — SMA20, SMA50, 1D/1M/3M price change, annualized volatility, and trend (BULLISH / BEARISH / NEUTRAL)
3. **Generates an AI research report** — powered by LLaMA 3.3 70B via Groq with sections: Company Overview, Financial Health, Technical Outlook, Risk Factors, Investment Thesis, and a final **BUY / HOLD / SELL verdict**
4. **Shows recent headlines** — top 5 news articles for the stock

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Groq](https://console.groq.com) | LLM inference (LLaMA 3.3 70B) |
| [yFinance](https://github.com/ranaroussi/yfinance) | Real-time & historical stock data |
| Python 3.8+ | Core runtime |

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/gnarendra9014-blind/day_12-of-ML-Projects.git
cd day_12-of-ML-Projects
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) → API Keys → Create Key

### 4. Run the agent
```bash
python app.py
```

---

## 💻 Usage

```
🔑 Enter Groq API Key: <your-groq-api-key>

📈 Enter stock ticker (or 'q' to quit): AAPL
```

### Example tickers to try:
| Company | Ticker |
|---------|--------|
| Apple | `AAPL` |
| Google | `GOOGL` |
| Tesla | `TSLA` |
| Microsoft | `MSFT` |
| Nvidia | `NVDA` |
| Reliance (India) | `RELIANCE.NS` |
| TCS (India) | `TCS.NS` |

---

## 📊 Sample Output

```
────────── STEP 1 · Fetching Stock Data ──────────
  ✅ Apple Inc. (AAPL)
  Sector: Technology | Industry: Consumer Electronics

────────── STEP 2 · Technical Analysis ──────────
  Trend:       BULLISH
  Price:       $213.49
  SMA20:       $209.12  ↑
  SMA50:       $205.87  ↑
  1D Change:   +1.23%
  Volatility:  28.4% (annualized)

────────── STEP 3 · Fundamentals ──────────
  Market Cap:       $3.21T
  P/E Ratio:        34.12
  Analyst Target:   $240.00
  Recommendation:   BUY

────────── STEP 4 · Groq AI Deep Analysis ──────────
  [Full AI-generated research report with BUY/HOLD/SELL verdict]
```

---

## 📁 Project Structure

```
day12_stock_agent/
├── app.py              # Main agent script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Disclaimer

> This tool is for **educational purposes only** and does not constitute financial advice. Always do your own research before making investment decisions.

---

## 📅 Part of the 25-Day AI Challenge

Building one AI project every day for 25 days. Follow along on GitHub!
