#!/usr/bin/env python3
"""
Day 12 — AI Stock Research Agent
25-Day AI Challenge
Stack: Groq + yFinance | Pattern: Agent
"""

import yfinance as yf
import json
import re
import sys
from groq import Groq
from datetime import datetime

# ─────────────────────────────────────────────
# ANSI Colors for CLI
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    DIM     = "\033[2m"

def header():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════╗
║        📈  AI Stock Research Agent  📈               ║
║        Day 12 · 25-Day AI Challenge                  ║
║        Stack: Groq + yFinance · Pattern: Agent       ║
╚══════════════════════════════════════════════════════╝{C.RESET}
""")

def divider(title=""):
    if title:
        print(f"\n{C.DIM}{'─'*10}{C.RESET} {C.BOLD}{title}{C.RESET} {C.DIM}{'─'*10}{C.RESET}")
    else:
        print(f"{C.DIM}{'─'*54}{C.RESET}")

# ─────────────────────────────────────────────
# Tool 1: Fetch Stock Data via yFinance
# ─────────────────────────────────────────────
def fetch_stock_data(ticker: str) -> dict:
    """Fetch comprehensive stock data using yFinance."""
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        # Historical price (last 5 days)
        hist = stock.history(period="5d")
        prices = []
        if not hist.empty:
            for date, row in hist.iterrows():
                prices.append({
                    "date": str(date.date()),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"])
                })

        # Recent news headlines
        news = stock.news[:5] if stock.news else []
        headlines = [n.get("content", {}).get("title", "") for n in news if n.get("content", {}).get("title")]

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice", "N/A"),
            "previous_close": info.get("previousClose", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "beta": info.get("beta", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "analyst_target": info.get("targetMeanPrice", "N/A"),
            "recommendation": info.get("recommendationKey", "N/A"),
            "price_history_5d": prices,
            "recent_news": headlines,
            "business_summary": (info.get("longBusinessSummary", "")[:500] + "...") if info.get("longBusinessSummary") else "N/A"
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


# ─────────────────────────────────────────────
# Tool 2: Calculate Technical Signals
# ─────────────────────────────────────────────
def calculate_technicals(ticker: str) -> dict:
    """Calculate basic technical indicators."""
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period="3mo")

        if hist.empty:
            return {"error": "No historical data"}

        closes = hist["Close"].tolist()
        current = closes[-1]

        # Simple Moving Averages
        sma20 = sum(closes[-20:]) / min(20, len(closes))
        sma50 = sum(closes[-50:]) / min(50, len(closes))

        # Price change
        change_1d = ((closes[-1] - closes[-2]) / closes[-2] * 100) if len(closes) >= 2 else 0
        change_1mo = ((closes[-1] - closes[-22]) / closes[-22] * 100) if len(closes) >= 22 else 0
        change_3mo = ((closes[-1] - closes[0]) / closes[0] * 100) if len(closes) >= 2 else 0

        # Volatility (std dev of daily returns)
        daily_returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        avg_return = sum(daily_returns) / len(daily_returns)
        variance = sum((r - avg_return) ** 2 for r in daily_returns) / len(daily_returns)
        volatility = (variance ** 0.5) * (252 ** 0.5) * 100  # annualized

        return {
            "current_price": round(current, 2),
            "sma_20": round(sma20, 2),
            "sma_50": round(sma50, 2),
            "above_sma20": current > sma20,
            "above_sma50": current > sma50,
            "change_1d_pct": round(change_1d, 2),
            "change_1mo_pct": round(change_1mo, 2),
            "change_3mo_pct": round(change_3mo, 2),
            "annualized_volatility_pct": round(volatility, 2),
            "trend": "BULLISH" if current > sma20 > sma50 else ("BEARISH" if current < sma20 < sma50 else "NEUTRAL")
        }
    except Exception as e:
        return {"error": str(e)}


# ─────────────────────────────────────────────
# Agent: Groq-powered Research & Analysis
# ─────────────────────────────────────────────
def run_agent(ticker: str, api_key: str):
    client = Groq(api_key=api_key)

    print(f"\n{C.CYAN}🤖 Agent activated for {C.BOLD}{ticker.upper()}{C.RESET}")

    # ── Step 1: Fetch Data ──
    divider("STEP 1 · Fetching Stock Data")
    print(f"  {C.DIM}→ Calling yFinance for {ticker.upper()}...{C.RESET}")
    stock_data = fetch_stock_data(ticker)

    if "error" in stock_data:
        print(f"{C.RED}❌ Error fetching data: {stock_data['error']}{C.RESET}")
        return

    print(f"  {C.GREEN}✅ {stock_data['company_name']} ({stock_data['ticker']}){C.RESET}")
    print(f"  {C.DIM}Sector: {stock_data['sector']} | Industry: {stock_data['industry']}{C.RESET}")

    # ── Step 2: Technical Analysis ──
    divider("STEP 2 · Technical Analysis")
    print(f"  {C.DIM}→ Calculating indicators...{C.RESET}")
    technicals = calculate_technicals(ticker)

    if "error" not in technicals:
        trend_color = C.GREEN if technicals["trend"] == "BULLISH" else (C.RED if technicals["trend"] == "BEARISH" else C.YELLOW)
        print(f"  Trend:       {trend_color}{C.BOLD}{technicals['trend']}{C.RESET}")
        print(f"  Price:       ${technicals['current_price']}")
        print(f"  SMA20:       ${technicals['sma_20']}  {'↑' if technicals['above_sma20'] else '↓'}")
        print(f"  SMA50:       ${technicals['sma_50']}  {'↑' if technicals['above_sma50'] else '↓'}")
        print(f"  1D Change:   {C.GREEN if technicals['change_1d_pct'] > 0 else C.RED}{technicals['change_1d_pct']}%{C.RESET}")
        print(f"  1M Change:   {C.GREEN if technicals['change_1mo_pct'] > 0 else C.RED}{technicals['change_1mo_pct']}%{C.RESET}")
        print(f"  3M Change:   {C.GREEN if technicals['change_3mo_pct'] > 0 else C.RED}{technicals['change_3mo_pct']}%{C.RESET}")
        print(f"  Volatility:  {technicals['annualized_volatility_pct']}% (annualized)")

    # ── Step 3: Fundamentals ──
    divider("STEP 3 · Fundamentals")
    def fmt(val, prefix="", suffix=""):
        if val in ("N/A", None): return "N/A"
        if isinstance(val, float): return f"{prefix}{val:.2f}{suffix}"
        if isinstance(val, int) and val > 1_000_000:
            return f"{prefix}{val/1_000_000_000:.2f}B" if val > 1_000_000_000 else f"{prefix}{val/1_000_000:.2f}M"
        return f"{prefix}{val}{suffix}"

    print(f"  Current Price:    {fmt(stock_data['current_price'], '$')}")
    print(f"  Market Cap:       {fmt(stock_data['market_cap'], '$')}")
    print(f"  P/E Ratio:        {fmt(stock_data['pe_ratio'])}")
    print(f"  Forward P/E:      {fmt(stock_data['forward_pe'])}")
    print(f"  52W High/Low:     ${stock_data['52w_high']} / ${stock_data['52w_low']}")
    print(f"  Dividend Yield:   {fmt(stock_data['dividend_yield'], suffix='%') if stock_data['dividend_yield'] != 'N/A' else 'N/A'}")
    print(f"  Beta:             {fmt(stock_data['beta'])}")
    print(f"  Profit Margin:    {fmt(stock_data['profit_margin'], suffix='%') if stock_data['profit_margin'] != 'N/A' else 'N/A'}")
    print(f"  Analyst Target:   {fmt(stock_data['analyst_target'], '$')}")
    print(f"  Recommendation:   {C.BOLD}{str(stock_data['recommendation']).upper()}{C.RESET}")

    # ── Step 4: Groq AI Analysis ──
    divider("STEP 4 · Groq AI Deep Analysis")
    print(f"  {C.DIM}→ Sending data to LLaMA 3 70B via Groq...{C.RESET}\n")

    prompt = f"""You are an expert stock research analyst. Analyze the following data for {stock_data['company_name']} ({ticker.upper()}) and produce a comprehensive research report.

FUNDAMENTAL DATA:
{json.dumps(stock_data, indent=2)}

TECHNICAL DATA:
{json.dumps(technicals, indent=2)}

Write a structured research report with these sections:

1. COMPANY OVERVIEW (2-3 sentences)
2. FINANCIAL HEALTH (key strengths and concerns from the fundamentals)
3. TECHNICAL OUTLOOK (what the price action and indicators suggest)
4. RISK FACTORS (3 bullet points)
5. INVESTMENT THESIS (bull case and bear case in 1-2 sentences each)
6. VERDICT: BUY / HOLD / SELL with a one-line rationale

Be specific, data-driven, and concise. Use the actual numbers from the data provided."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024
    )

    analysis = response.choices[0].message.content

    # Pretty print the analysis
    print(f"{C.CYAN}{analysis}{C.RESET}")

    # ── Step 5: Recent News ──
    if stock_data.get("recent_news"):
        divider("STEP 5 · Recent News")
        for i, headline in enumerate(stock_data["recent_news"], 1):
            if headline:
                print(f"  {C.DIM}{i}.{C.RESET} {headline}")

    divider()
    print(f"\n{C.DIM}Research completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
    print(f"{C.DIM}⚠️  This is not financial advice. For educational purposes only.{C.RESET}\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    header()

    # Get API key
    api_key = input(f"{C.BOLD}🔑 Enter Groq API Key:{C.RESET} ").strip()
    if not api_key:
        print(f"{C.RED}❌ API key required. Get one free at console.groq.com{C.RESET}")
        sys.exit(1)

    while True:
        print(f"\n{C.DIM}Examples: AAPL, TSLA, GOOGL, MSFT, NVDA, RELIANCE.NS, TCS.NS{C.RESET}")
        ticker = input(f"{C.BOLD}📈 Enter stock ticker (or 'q' to quit):{C.RESET} ").strip()

        if ticker.lower() in ("q", "quit", "exit"):
            print(f"\n{C.CYAN}👋 Goodbye!{C.RESET}\n")
            break

        if not ticker:
            print(f"{C.YELLOW}⚠️  Please enter a ticker symbol.{C.RESET}")
            continue

        run_agent(ticker, api_key)

        again = input(f"\n{C.BOLD}Analyze another stock? (y/n):{C.RESET} ").strip().lower()
        if again != "y":
            print(f"\n{C.CYAN}👋 Goodbye!{C.RESET}\n")
            break


if __name__ == "__main__":
    main()
