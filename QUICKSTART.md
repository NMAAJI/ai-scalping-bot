# 🚀 QUICK START - 5 MINUTES TO AUTONOMOUS TRADING

## Step 1: Create .env File (1 minute)

In the project root directory, create a `.env` file:

```bash
# === REQUIRED ===
BINANCE_API_KEY=your_testnet_key_here
BINANCE_API_SECRET=your_testnet_secret_here
GEMINI_API_KEY=your_gemini_api_key_here

# === OPTIONAL (but recommended for backup) ===
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
TOGETHER_API_KEY=your_together_key_here

# === CONFIGURATION ===
AUTONOMOUS_MODE=true
ENABLE_BACKUP_APIS=true
```

**Where to get API keys:**
- **Binance Testnet:** https://testnet.binance.vision/
- **Gemini API:** https://makersuite.google.com/app/apikey
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/
- **Together AI:** https://www.together.ai/

## Step 2: Install Dependencies (1 minute)

```bash
pip install google-generativeai openai anthropic requests
```

## Step 3: Run the Bot (30 seconds)

```bash
python main.py
```

You should see:
```
========================================
🤖 AUTONOMOUS MODE ENABLED
========================================
✅ All services initialized successfully!
📈 Starting web dashboard on http://0.0.0.0:5000
🌐 Open your browser and navigate to http://localhost:5000
```

## Step 4: Monitor Dashboard (Ongoing)

Open in your browser:
```
http://localhost:5000
```

**That's it!** Your bot is now trading autonomously. 🎉

---

## What's Happening

Your bot is now:
- ✅ Fetching market data every 60 seconds
- ✅ Using Gemini AI to analyze markets
- ✅ Making autonomous trade decisions
- ✅ Executing trades automatically (when confident)
- ✅ Logging every decision to `logs/autonomous_trades.jsonl`
- ✅ Providing real-time status via web dashboard and API

---

## Key URLs

| URL | Purpose |
|-----|---------|
| http://localhost:5000 | Web Dashboard |
| http://localhost:5000/api/autonomous-status | Get status |
| http://localhost:5000/api/autonomous-history | View decisions |
| http://localhost:5000/api/backup-services-status | Check health |

---

## Monitoring Commands

```bash
# Watch autonomous decisions
tail -f logs/autonomous_trades.jsonl

# Check recent status
curl http://localhost:5000/api/autonomous-status

# View backup service health
curl http://localhost:5000/api/backup-services-status

# Count trades executed today
grep "$(date +%Y-%m-%d)" logs/autonomous_trades.jsonl | wc -l
```

---

## Next Steps

1. Monitor the bot for first 24 hours
2. Review audit trail: `logs/autonomous_trades.jsonl`
3. Check dashboard at http://localhost:5000
4. Adjust parameters if needed (see configuration guide)
5. Deploy to production (after successful testing)

---

## Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Add `GEMINI_API_KEY` to `.env` file

### Issue: "No trades executing"
**Solution:** Check confidence is >= 0.60. Lower threshold in `config/settings.py`:
```python
MIN_CONFIDENCE_FOR_TRADE = 0.50
```

### Issue: Dashboard won't load
**Solution:** Verify Flask is running and FLASK_PORT is correct:
```bash
curl http://localhost:5000
```

---

## For More Information

- **Setup Guide:** [AUTONOMOUS_AI_SETUP.md](AUTONOMOUS_AI_SETUP.md)
- **Technical Details:** [AUTONOMOUS_INTEGRATION_GUIDE.md](AUTONOMOUS_INTEGRATION_GUIDE.md)
- **Full Reference:** [AUTONOMOUS_AI_TRADING.md](AUTONOMOUS_AI_TRADING.md)
- **Executive Summary:** [README_AUTONOMOUS.md](README_AUTONOMOUS.md)
- **File Reference:** [FILE_REFERENCE.md](FILE_REFERENCE.md)
- **Completion Summary:** [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)

---

## Ready? Start Now! 🚀

```bash
python main.py
```

Your autonomous bot is trading!
