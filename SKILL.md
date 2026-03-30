# 📊 Chinese Interest Rate Monitor

全面追踪中国利率数据，每日检查，有变化立即推送通知。

> Monitor China interest rates comprehensively. Daily check with change alerts.

## Metadata

- **name**: chinese-interest-rate
- **version**: 2.0.0
- **description**: 全面追踪中国利率数据：LPR、存款基准利率、国债收益率、SHIBOR、房贷利率等，有变化立即推送
- **language**: zh-CN / en
- **tags**: finance, china, interest-rate, LPR, SHIBOR, bank-deposit, bond-yield, mortgage, monitor, 利率, 贷款市场报价利率, 国债收益率, 房贷利率

---

## Overview

| Feature | Description |
|---------|-------------|
| 🏦 基准利率 | 1Y/3Y/5Y 定期存款基准利率 |
| 📈 LPR | 1Y/5Y 贷款市场报价利率 |
| 📉 国债收益率 | 1Y/3Y/10Y 国债收益率 |
| 💧 SHIBOR | 隔夜/1周/1月/3月 银行间同业拆借利率 |
| 🏠 房贷利率 | 5年期以上LPR（基准房贷利率） |
| 🔄 逆回购 | 7天/14天 公开市场操作利率 |
| 💰 存款准备金 | 大型金融机构存款准备金率 |
| Daily Check | 每日自动检查 |
| Change Alert | 有变化立即推送，无变化静默 |

---

## Data Points Tracked

### 🏦 银行存款利率（基准）

| 期限 | 说明 |
|------|------|
| 1年 | 定期存款一年期基准利率 |
| 3年 | 定期存款三年期基准利率 |
| 5年 | 定期存款五年期基准利率 |

### 📊 LPR（贷款市场报价利率）

| 期限 | 说明 |
|------|------|
| 1年期 | 贷款市场报价利率（实体经济） |
| 5年期以上 | 贷款市场报价利率（房地产） |

### 📉 国债收益率

| 期限 | 说明 |
|------|------|
| 1年期 | 1年期国债收益率 |
| 3年期 | 3年期国债收益率 |
| 10年期 | 10年期国债收益率（重要风向标） |

### 💧 SHIBOR（上海银行间同业拆借利率）

| 期限 | 说明 |
|------|------|
| O/N 隔夜 | 隔夜拆借利率（最短资金成本） |
| 1W 一周 | 1周期限 |
| 1M 一月 | 1月期限 |
| 3M 三月 | 3月期限（重要参考） |

### 🏠 房贷利率

| 期限 | 说明 |
|------|------|
| 5年期以上 | 5年期以上贷款LPR，是房贷利率的基准 |

### 🔄 公开市场操作利率

| 期限 | 说明 |
|------|------|
| 7天逆回购 | 7天公开市场逆回购利率 |
| 14天逆回购 | 14天公开市场逆回购利率 |
| MLF | 中期借贷便利利率（1年期） |

---

## 数据来源

| 类型 | 来源 |
|------|------|
| 存款基准利率 | 中国人民银行 (PBC) |
| LPR | 全国银行间同业拆借中心 |
| 国债收益率 | 中国债券信息网 / CFETS |
| SHIBOR | 中国外汇交易中心 |
| 逆回购利率 | 中国人民银行 |
| 存款准备金率 | 中国人民银行 |

---

## 通知格式

### 有变化时

```
📊 中国利率变动日报 | {日期}

🏦 银行存款利率（基准）
- 1年: X.XX% (±Xbp)
- 3年: X.XX% (±Xbp)
- 5年: X.XX% (±Xbp)

📊 LPR 贷款市场报价利率
- 1年期: X.XX% (±Xbp)
- 5年期以上: X.XX% (±Xbp)

📉 国债收益率
- 1年: X.XX% (±Xbp)
- 3年: X.XX% (±Xbp)
- 10年: X.XX% (±Xbp)

💧 SHIBOR 银行间拆借利率
- O/N隔夜: X.XX% (±Xbp)
- 1W: X.XX% (±Xbp)
- 1M: X.XX% (±Xbp)
- 3M: X.XX% (±Xbp)

🏠 房贷相关
- 5年期以上LPR: X.XX% (±Xbp)

🔄 公开市场操作
- 7天逆回购: X.XX% (±Xbp)
- 14天逆回购: X.XX% (±Xbp)

💡 影响分析：简要说明变化对经济的影响
```

### 无变化时

静默，不发送任何通知。

---

## 数据文件格式

`data/rates.json`:

```json
{
  "updateDate": "2026-03-30",
  "depositRates": {
    "1year": "1.50",
    "3year": "2.00",
    "5year": "2.25"
  },
  "LPR": {
    "1year": "3.45",
    "5yearPlus": "4.20"
  },
  "bondYields": {
    "1year": "1.60",
    "3year": "1.85",
    "10year": "2.30"
  },
  "SHIBOR": {
    "ON": "1.75",
    "1W": "1.85",
    "1M": "2.00",
    "3M": "2.10"
  },
  "mortgageLPR": {
    "5yearPlus": "4.20"
  },
  "OMO": {
    "repo7d": "1.80",
    "repo14d": "1.95",
    "MLF1Y": "2.50"
  }
}
```

---

## 安装

```bash
openclaw skills install chinese-interest-rate
```

---

## 定时任务

建议每日 10:00（北京时间）执行：

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

## 文件结构

```
chinese-interest-rate/
├── SKILL.md              # 本文件
├── _meta.json            # 版本信息
├── data/
│   └── rates.json        # 历史利率数据
└── scripts/
    └── check_rates.py    # 利率检查脚本
```

---

## 扩展说明

如需添加更多利率指标，可修改：
1. `data/rates.json` — 添加新的利率字段
2. `scripts/check_rates.py` — 添加新的利率数据源
3. SKILL.md — 更新本说明文档

---

## 适用场景

- 📊 金融从业者（银行、证券、基金）
- 🏠 房贷用户（LPR变动直接影响月供）
- 💼 投资理财（LPR是资本市场重要指标）
- 📈 经济研究者（利率是宏观经济的核心变量）

---

## License

MIT License

---

_追踪利率变化，把握理财先机 📊_
