# 📊 Chinese Interest Rate Monitor

Monitor China bank deposit rates and government bond yields. Daily check with change alerts.

> 追踪中国银行存款利率与国债收益率，每日检查，变动即通知

## Metadata

- **name**: chinese-interest-rate
- **version**: 1.0.0
- **description**: Monitor China bank deposit rates and government bond yields daily. Alert on any changes.
- **language**: en / zh-CN
- **tags**: finance, china, interest-rate, bank-deposit, bond-yield, monitor

---

## Overview

| Feature | Description |
|---------|-------------|
| Bank Deposit Rates | 1Y, 3Y, 5Y PBC benchmark rates |
| Bond Yields | 1Y and 10Y government bond yields |
| Daily Check | Run via cron or on-demand |
| Change Alert | Notify on any change (webhook/email/custom) |
| No Change = Silent | No notification when rates unchanged |

---

## Data Points Tracked

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

## Data Sources

| Type | Source |
|------|--------|
| Bank Deposit Rates | 中国人民银行 (PBC) official benchmark rates |
| Bond Yields | ChinaBond, TradingEconomics, 聚金数据 |

---

## Notification

### When Changed

When any rate changes, output the following format:

```
📊 利率变动提醒 | {date}

🏦 银行存款利率
- 1年: {rate}% ({change})
- 3年: {rate}% ({change})
- 5年: {rate}% ({change})

📈 国债收益率
- 1年: {rate}% ({change})
- 10年: {rate}% ({change})
```

### When Unchanged

No output (silent). Only output when at least one rate has changed.

---

## Configuration

Edit `data/rates.json` to set your baseline:

```json
{
  "updateDate": "2026-03-29",
  "depositRates": {
    "1year": "0.95",
    "3year": "1.25",
    "5year": "1.30"
  },
  "bondYields": {
    "1year": "1.24",
    "10year": "1.82"
  }
}
```

---

## Installation

```bash
# Install via OpenClaw
openclaw skills install chinese-interest-rate

# Or from GitHub
git clone https://github.com/ryanbihai/chinese-interest-rate.git
```

---

## Cron Schedule

Recommended: Run daily at 10:00 Beijing time

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  }
}
```

---

## Customization

### Change Notification Channel

Modify the notification logic in the cron payload to use:
- **Webhook**: POST to your endpoint
- **Email**: Send via SMTP
- **WeChat**: Use 企业微信 webhook
- **Custom**: Any channel OpenClaw supports

### Add More Rates

Edit SKILL.md and `data/rates.json` to track additional instruments:
- Wealth management products (理财产品)
- LPR (贷款市场报价利率)
- SHIBOR (上海银行间同业拆借利率)

---

## Files

```
chinese-interest-rate/
├── SKILL.md              # This file
├── _meta.json            # Version & metadata
├── README.md             # Full documentation
├── data/
│   └── rates.json        # Historical rates storage
└── scripts/
    └── check_rates.py    # Core check script
```

---

## License

MIT License - Free to use, modify, and distribute

---

_CN: 追踪利率变化，把握理财先机_
_EN: Track rate changes, stay ahead in finance_
