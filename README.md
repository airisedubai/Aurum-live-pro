# Aurum-live-pro

AURUM PRO — Live Gold & Crypto Trading Dashboard for Dubai traders.

## Features
- 💰 Live price dashboard (Gold, Silver, Oil, Bitcoin, Ethereum, Solana, XRP, BNB)
- ⚜ Aurum Engine — SMC/ICT trading discipline: 10-rule checklist, risk calculator, trade log
- 📈 AI-powered analysis via Anthropic Claude (BYOK — bring your own key)
- 🔥 Quick trade Long/Short buttons for fast scalping execution
- 📊 ATR volatility-based position sizing
- 📋 Session-persistent trade log (survives page reload)

## Quick Start
Open `index.html` in a browser. No build step or server required.

### Local development server (recommended)
```
python -m http.server 8000
```
Then open `http://localhost:8000`.

### Setup AI analysis
1. Get an Anthropic API key at [console.anthropic.com](https://console.anthropic.com)
2. Click the 🔑 key icon in the dashboard
3. Paste your key — it's stored only in your browser's localStorage
4. Without a key, the dashboard shows rule-based estimates

## Deployment
Automatic deployment via GitHub Actions to GitHub Pages on push to `main`.
See `.github/workflows/deploy.yml`.

## Live Demo
After enabling GitHub Pages (Settings → Pages → Source: GitHub Actions), deploy at:
`https://airisedubai.github.io/Aurum-live-pro`

## Technology
- Vanilla JavaScript (no framework)
- TwelveData API (live forex/metals prices)
- CoinGecko API (live crypto prices)
- Anthropic Claude API (AI analysis — BYOK)
- HTML5 / CSS3 / JavaScript