# 📊 Chinese Interest Rate Monitor

全面追踪中国利率数据，每日检查，有变化立即推送通知（中英文双语可配置）。

> Monitor China interest rates comprehensively. Daily check with change alerts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green.svg)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-v3.0-orange.svg)](https://clawhub.ai/skill/ryanbihai/chinese-interest-rate)
[![Downloads](https://img.shields.io/badge/Downloads-13+-blue.svg)](https://clawhub.ai/skill/ryanbihai/chinese-interest-rate)

**Keywords:** China interest rate | LPR | SHIBOR | bond yield | mortgage rate | PBC | bank deposit rate | 中国利率 | LPR贷款市场报价利率 | 国债收益率 | 房贷利率 | bilingual Chinese English

---

## ✨ 功能特色

| Feature | Description |
|---------|-------------|
| 🏦 基准利率 | 1Y/3Y/5Y 定期存款基准利率 |
| 📊 LPR | 1Y/5Y 贷款市场报价利率 |
| 📉 国债收益率 | 1Y/3Y/10Y 国债收益率 |
| 💧 SHIBOR | O/N, 1W, 1M, 3M 银行间拆借利率 |
| 🏠 房贷利率 | 5年期以上LPR |
| 🔄 逆回购利率 | 7天/14天公开市场操作 |
| 💰 存款准备金率 | 大型金融机构 |
| 🌐 中英双语 | 可配置语言（zh/en/bilingual） |
| ⏰ 每日自动检查 | 有变化才推送，无变化静默 |

---

## 语言配置

在 `data/config.json` 中设置：

```json
{
  "language": "bilingual"
}
```

| 值 | 通知语言 |
|----|---------|
| `zh` | 🇨🇳 全中文 |
| `en` | 🇺🇸 全英文 |
| `bilingual` | 🇨🇳🇺🇸 中英双语 |

---

## 安装

```bash
openclaw skills install chinese-interest-rate
```

---

## 适用场景

- 📊 金融从业者（银行、证券、基金）
- 🏠 房贷用户（LPR变动直接影响月供）
- 💼 投资理财（LPR是资本市场重要指标）
- 📈 经济研究者

---

## License

[MIT License](LICENSE)
