# 📊 Chinese Interest Rate Monitor

> Monitor China bank deposit rates and government bond yields. Daily check with change alerts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green.svg)](https://openclaw.ai)

---

## Features

| Feature | Description |
|---------|-------------|
| 📈 Bank Deposit Rates | Track 1Y, 3Y, 5Y PBC benchmark rates |
| 📉 Bond Yields | Track 1Y and 10Y government bond yields |
| ⏰ Daily Check | Run automatically via cron |
| 🔔 Change Alert | Notify on any rate change |
| 🤫 Silent Mode | No notification when rates unchanged |

---

## Quick Start

### Install

```bash
openclaw skills install chinese-interest-rate
```

### On-Demand Check

Say: "Check interest rates" or "查一下利率"

---

## Tracked Data

### Bank Deposit Rates (基准利率)

| Tenor | Description |
|-------|-------------|
| 1-Year | 定期存款一年期基准 |
| 3-Year | 定期存款三年期基准 |
| 5-Year | 定期存款五年期基准 |

### Government Bond Yields (国债收益率)

| Tenor | Description |
|-------|-------------|
| 1-Year | 1年期国债收益率 |
| 10-Year | 10年期国债收益率 |

---

## Alert Format

When rates change:

```
📊 Interest Rate Update | 2026-03-29

🏦 Bank Deposit Rates
- 1Y: 0.95% (-0.05%)
- 3Y: 1.25% (unchanged)
- 5Y: 1.30% (+0.05%)

📈 Bond Yields
- 1Y: 1.24% (unchanged)
- 10Y: 1.82% (+0.01%)
```

---

## Data Sources

| Type | Source |
|------|--------|
| Bank Deposit Rates | 中国人民银行 (PBC) |
| Bond Yields | ChinaBond, TradingEconomics |

---

## Files

```
chinese-interest-rate/
├── SKILL.md              # Skill definition
├── _meta.json            # Version info
├── data/
│   └── rates.json       # Historical rates
└── scripts/
    └── check_rates.py   # Check script
```

---

## License

[MIT License](LICENSE) - Free to use, modify, and distribute
