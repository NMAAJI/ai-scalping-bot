# ⚡ QUICK REFERENCE - AI Trading Bot v3.0

**Quick Start Guide | Fast Reference | Common Tasks**

---

## 🚀 GET STARTED IN 30 SECONDS

### Step 1: Start the Bot
```bash
python main.py
```

### Step 2: Open Dashboard
```
http://localhost:5000
```

### Step 3: Watch It Trade
- Click "▶ Start Trading" button
- Watch autonomous trades execute
- Monitor API health (green = online)
- View real-time data on dashboard

---

## 📊 DASHBOARD TABS

| Tab | Purpose | What to Look For |
|-----|---------|------------------|
| **Overview** | Main metrics | Balance, Price, AI Score, Trade Count |
| **Chart** | Price chart | TradingView BTCUSDT chart |
| **Trades** | Trade history | All executed trades with P&L |
| **Analytics** | Statistics | Win rate, P&L, Performance |
| **Health** | System status | API status, Response time |

---

## 🎛️ CONTROLS

### Start/Stop Trading
```
Dashboard → Click "▶ Start Trading" button
Dashboard → Click "⏹ Stop Trading" button
```

### View Status
```
Check API indicators: 🟢 = Online, 🔴 = Offline
Check "Bot Status" card: Running / Stopped
```

### Monitor Performance
```
Dashboard → Analytics tab
See: Win rate, Total P&L, Profit factor
```

---

## 🔧 QUICK CUSTOMIZATION

### Change Trading Parameters
```bash
# Edit trading settings
notepad config/settings.py

# Common settings to adjust:
CONFIDENCE_THRESHOLD = 70      # Min AI confidence (0-100)
POSITION_SIZE = 0.5            # Position size in BTC
STOP_LOSS = 2                  # Stop loss %
TAKE_PROFIT = 5                # Take profit %
MAX_POSITIONS = 3              # Max open positions
```

### Change API Keys
```bash
# Edit .env file
notepad .env

# Update these:
BINANCE_API_KEY=your_key_here
BINANCE_SECRET=your_secret_here
GEMINI_API_KEY=your_gemini_key_here
```

### Change Update Speed
```bash
# Edit settings.py
UPDATE_INTERVAL = 3            # Seconds between dashboard refresh
HEALTH_CHECK_INTERVAL = 30     # Seconds between health checks
```

---

## 🔍 TROUBLESHOOTING

### Problem: Bot won't start
```
✓ Check Python version: python --version
✓ Check dependencies: pip install -r requirements.txt
✓ Check .env file exists with API keys
✓ Check port 5000 not in use
```

### Problem: APIs show offline
```
✓ Check internet connection
✓ Check .env file has correct API keys
✓ Wait 30 seconds for health check
✓ Refresh dashboard (F5)
✓ Restart bot if still offline
```

### Problem: No trades executing
```
✓ Check "Bot Status" = Running (not Stopped)
✓ Check AI Score > 70 (confidence threshold)
✓ Check account balance is not zero
✓ Check market conditions (very volatile markets only)
✓ Check logs for errors: type logs\bot.log
```

### Problem: Dashboard not loading
```
✓ Check bot is running (should see Flask message)
✓ Check URL: http://localhost:5000
✓ Clear browser cache (Ctrl+Shift+Del)
✓ Try different browser
✓ Check port 5000 (use: netstat -ano | findstr :5000)
```

### Problem: High latency/slow updates
```
✓ Check internet connection speed
✓ Check CPU usage (Ctrl+Shift+Esc)
✓ Close other applications
✓ Check if bot is processing large data
```

---

## 📋 COMMON COMMANDS

```bash
# Start bot
python main.py

# Stop bot (Ctrl+C in terminal)
Press Ctrl+C

# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt

# View logs
type logs\bot.log

# Clear old trades database
del data\trades.db

# Reset to default settings
notepad config\settings.py
```

---

## 🎯 MONITORING CHECKLIST

### Daily Checks
- [ ] Bot is running (dashboard loads)
- [ ] APIs show online (🟢 green)
- [ ] Real balance shows (not dummy)
- [ ] Real prices show (not dummy)
- [ ] Trades executing (if market conditions good)

### Weekly Checks
- [ ] Win rate acceptable (>50% ideal)
- [ ] P&L positive or acceptable
- [ ] No error logs
- [ ] All APIs healthy
- [ ] Dashboard responsive

### Monthly Checks
- [ ] Review performance metrics
- [ ] Check database size
- [ ] Verify trades are logging
- [ ] Review AI scores
- [ ] Confirm settings still optimal

---

## 📊 INTERPRETING DASHBOARD

### Color Meanings
```
🟢 Green     = Online, Good, Profitable
🔴 Red       = Offline, Error, Loss
🟡 Yellow    = Warning, Caution (if used)
```

### Status Indicators
```
AI Score: 75/100
├─ 0-30:   Very risky, don't trade
├─ 30-70:  Risky, limited trades
└─ 70-100: Good, trade normally

Win Rate: 55%
├─ <40%:   Needs adjustment
├─ 40-60%: Acceptable
└─ >60%:   Excellent

P&L: +$500
├─ Negative: Losing money
├─ Small:    Testing phase
└─ Growing:  Working well
```

---

## 🔐 SECURITY TIPS

### Keep API Keys Safe
```
✓ Never share .env file
✓ Never commit .env to Git
✓ Use testnet keys (safe)
✓ Rotate real keys periodically
✓ Monitor account regularly
```

### Protect Your Computer
```
✓ Use Windows Defender
✓ Keep Windows updated
✓ Use firewall
✓ Don't run on public WiFi
✓ Backup your database
```

### Safe Testing
```
✓ Use Binance testnet (default)
✓ Start with small positions
✓ Monitor first trades manually
✓ Verify before real money
✓ Keep stop losses tight
```

---

## 💾 BACKUP & RECOVERY

### Backup Your Data
```bash
# Backup trade history
copy data\trades.db data\trades.db.backup

# Backup settings
copy config\settings.py config\settings.py.backup

# Backup .env (CAREFUL!)
copy .env .env.backup
```

### Restore from Backup
```bash
# Restore trades
copy data\trades.db.backup data\trades.db

# Restore settings
copy config\settings.py.backup config\settings.py
```

---

## 🚀 SCALING OPTIONS

### For More Frequent Trading
```python
# Edit config/settings.py
UPDATE_INTERVAL = 1            # Every 1 second
CONFIDENCE_THRESHOLD = 60      # Lower threshold
```

### For More Aggressive Trading
```python
# Edit config/settings.py
POSITION_SIZE = 1.0            # Larger positions
MAX_POSITIONS = 5              # More concurrent
TAKE_PROFIT = 3                # Tighter targets
```

### For Conservative Trading
```python
# Edit config/settings.py
POSITION_SIZE = 0.1            # Smaller positions
MAX_POSITIONS = 1              # One at a time
STOP_LOSS = 5                  # Wider stops
```

---

## 📈 PERFORMANCE OPTIMIZATION

### Speed Up Dashboard
```
✓ Fewer trades in table (limit rows)
✓ Close other browser tabs
✓ Use Chrome/Edge (fastest)
✓ Disable browser extensions
```

### Reduce Bot Load
```
✓ Increase UPDATE_INTERVAL (slower refresh)
✓ Decrease MAX_POSITIONS (fewer trades)
✓ Clear old trades (archive data)
✓ Restart bot periodically
```

### Improve Reliability
```
✓ Monitor logs regularly
✓ Keep error logs backed up
✓ Verify API health often
✓ Restart bot daily
```

---

## 📞 EMERGENCY PROCEDURES

### If Bot Crashes
```bash
# 1. Check error in terminal
# 2. Kill bot process (Ctrl+C)
# 3. Check logs: type logs\bot.log
# 4. Fix issue in code if needed
# 5. Restart: python main.py
```

### If All Trades Go Wrong
```bash
# 1. Stop bot: Click "⏹ Stop Trading"
# 2. Close trades manually (if possible)
# 3. Check what happened in logs
# 4. Adjust parameters
# 5. Restart carefully
```

### If Dashboard Won't Load
```bash
# 1. Kill bot: Ctrl+C
# 2. Kill any Python processes
# 3. Wait 10 seconds
# 4. Start bot again: python main.py
# 5. Try dashboard: http://localhost:5000
```

---

## 🔄 DAILY ROUTINE

### Morning
```
1. Start bot: python main.py
2. Check dashboard loads
3. Verify APIs online (🟢)
4. Check overnight trades
5. Review P&L
```

### During Day
```
1. Monitor dashboard (browser open)
2. Check API health periodically
3. Verify trades executing
4. Keep eye on P&L
```

### Evening
```
1. Review daily performance
2. Check win rate
3. Verify all trades closed
4. Check error logs
5. Plan adjustments if needed
```

### Night/Weekend
```
1. Can leave bot running
2. Bot is autonomous
3. Dashboard always accessible
4. Check via mobile if needed
5. Restart daily for freshness
```

---

## 🎯 GOAL TRACKING

### Week 1: Familiarization
- [ ] Bot starts without errors
- [ ] Dashboard loads
- [ ] APIs go online
- [ ] First trade executes
- [ ] Understand each tab

### Week 2-4: Verification
- [ ] 10+ trades executed
- [ ] Win rate established
- [ ] P&L trending correct
- [ ] No major errors
- [ ] Confidence growing

### Month 2+: Optimization
- [ ] Adjust parameters
- [ ] Improve win rate
- [ ] Optimize position size
- [ ] Fine-tune thresholds
- [ ] Scale up gradually

---

## 📚 FILE REFERENCE

| File | Purpose |
|------|---------|
| main.py | Bot entry point |
| config/settings.py | Trading parameters |
| .env | API keys (SECRET) |
| web/templates/dashboard_v3.html | Web UI |
| logs/bot.log | Activity log |
| data/trades.db | Trade history |

---

## 🎓 LEARNING RESOURCES

### Understand the Bot
- Read PRODUCTION_READY_v3.md
- Check code comments
- Review logs
- Monitor dashboard

### Improve Trading
- Learn technical analysis
- Study AI Score meanings
- Understand indicators
- Practice with testnet

### Troubleshooting
- Check dashboard Health tab
- Review bot logs
- Check PRODUCTION_READY_v3.md
- Monitor API indicators

---

## ✅ SUCCESS CHECKLIST

- [x] Bot starts without errors
- [x] Dashboard accessible
- [x] APIs show online
- [x] Real data displaying
- [x] Trades executing
- [x] P&L calculating
- [x] Logs recording
- [x] System stable

**✅ You're ready to trade! 🚀**

---

## 🆘 NEED HELP?

### Quick Fixes
1. Check TROUBLESHOOTING section above
2. Check PRODUCTION_READY_v3.md
3. Review bot logs
4. Check dashboard Health tab

### If Still Stuck
1. Stop bot (Ctrl+C)
2. Check error message carefully
3. Review logs for clues
4. Google the error
5. Restart bot and try again

---

**Version: 3.0.0**  
**Last Updated: December 27, 2025**  
**Status: ✅ Production Ready**

**Start trading now: `python main.py` → http://localhost:5000**
