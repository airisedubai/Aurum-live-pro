# Trading Agent Dashboard - Deployment Guide

## 🚀 Quick Deploy on Free Platforms

### Option 1: Deploy on Netlify (Recommended)

```bash
# 1. Create Netlify account at https://app.netlify.com
# 2. Clone your repo
git clone https://github.com/airisedubai/Aurum-live-pro.git
cd Aurum-live-pro

# 3. Deploy directly from GitHub
# - Go to Netlify Dashboard
# - Click "New site from Git"
# - Connect GitHub
# - Select this repo
# - Build command: (leave empty)
# - Publish directory: . (current directory)
# - Deploy!
```

**Share URL:** `https://[your-site-name].netlify.app`

### Option 2: Deploy on Vercel

```bash
# 1. Sign up at https://vercel.com
# 2. Import your GitHub repo
# 3. Click Deploy
```

**Share URL:** `https://[your-project-name].vercel.app`

### Option 3: Deploy on GitHub Pages

```bash
# 1. Push index.html to your repository
# 2. Go to Settings > Pages
# 3. Select "Deploy from a branch"
# 4. Choose main branch
# 5. Save
```

**Share URL:** `https://airisedubai.github.io/Aurum-live-pro`

### Option 4: Deploy with Python (Local/Server)

```bash
# Simple HTTP server
python -m http.server 8000

# Or with Node.js
npx http-server

# Or with Flask
flask run --port 5000
```

Then access at: `http://localhost:8000` or `http://your-server-ip:5000`

## 📊 Dashboard Features

✅ **Live Trading Signals**
- STRONG_BUY / BUY / HOLD / SELL / STRONG_SELL
- Real-time confidence scores
- Risk assessment

✅ **Market Analysis**
- Technical indicators (RSI, MACD, Trend)
- Global sentiment analysis
- Macroeconomic indicators

✅ **Weather Dashboard**
- Current conditions
- 7-day forecast
- Air quality monitoring
- Weather alerts

✅ **Recommendations**
- Actionable trading advice
- Position sizing guidance
- Risk management tips

## 🔗 Shareable URLs

### Netlify Example
```
https://trading-agent-dashboard.netlify.app
```

### GitHub Pages Example
```
https://airisedubai.github.io/Aurum-live-pro
```

### Vercel Example
```
https://trading-dashboard.vercel.app
```

## 📱 Responsive Design

✓ Desktop (1400px+)
✓ Tablet (768px - 1400px)
✓ Mobile (< 768px)

## 🎨 Customization

### Change Colors
Edit the CSS variables in `<style>`:

```css
:root {
    --primary: #1a1a2e;      /* Background */
    --accent: #00d4ff;       /* Highlight */
    --success: #51cf66;      /* Buy signals */
    --danger: #ff6b6b;       /* Sell signals */
}
```

### Update Company Name
Replace "Trading Agent Dashboard" with your company name

## 📊 Real Data Integration

To connect to real APIs:

```javascript
// Replace generateTradingData() with API call
async function fetchTradingData() {
    const response = await fetch('/api/predict');
    return await response.json();
}

// Replace generateWeatherData() with API call
async function fetchWeatherData() {
    const response = await fetch('/api/weather');
    return await response.json();
}
```

## 🔐 Security Notes

- This is a frontend-only application
- No sensitive data is stored
- API calls should be made from a backend server
- Use environment variables for API keys

## 📈 Performance

- Page load: < 2 seconds
- Updates every 30 seconds
- Optimized for mobile devices
- No external dependencies

## 🐛 Troubleshooting

### Dashboard not updating?
- Check browser console (F12)
- Ensure JavaScript is enabled
- Try clearing cache and reloading

### Styling looks wrong?
- Check if CSS is loading
- Verify browser compatibility
- Try a different browser

### Share button not working?
- Some browsers require HTTPS
- Check browser permissions
- Use manual copy-paste as fallback

## 📞 Support

- GitHub Issues: https://github.com/airisedubai/Aurum-live-pro/issues
- Email: support@airisedubai.com

## 📄 License

Apache License 2.0
