#!/usr/bin/env python3
"""
Chinese Interest Rate Monitor - Rate Check Script
追踪中国利率数据，对比历史，有变化则输出
"""

import json
import sys
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/rates.json')

def load_current_rates():
    """从文件加载当前利率数据"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_rates(data):
    """保存利率数据到文件"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_rates_from_search(search_results):
    """
    从web_search结果中解析利率数值
    返回提取到的利率字典
    """
    rates = {}
    text = ' '.join(search_results).lower() if isinstance(search_results, list) else search_results.lower()
    
    # LPR 解析 (如 "1年期LPR 3.45%" 或 "LPR 1年期 3.45%")
    lpr_patterns = [
        r'1年[期]?lpr[:\s]*(\d+\.?\d*)%',
        r'lpr.*1年[期]?[:\s]*(\d+\.?\d*)%',
        r'贷款市场报价利率.*1年[期]?[:\s]*(\d+\.?\d*)%',
        r'(\d+\.?\d*)%.*1年[期]?lpr',
    ]
    for pattern in lpr_patterns:
        import re
        m = re.search(pattern, text)
        if m:
            rates['LPR_1Y'] = m.group(1)
            break
    
    # 5年期LPR
    lpr5_patterns = [
        r'5年[期]?以上?lpr[:\s]*(\d+\.?\d*)%',
        r'lpr.*5年[期]?以上?[:\s]*(\d+\.?\d*)%',
        r'5年[期]?lpr[:\s]*(\d+\.?\d*)%',
    ]
    for pattern in lpr5_patterns:
        import re
        m = re.search(pattern, text)
        if m:
            rates['LPR_5Y'] = m.group(1)
            break
    
    # 存款基准利率
    deposit_patterns = [
        r'一年[期]?定期.*?[:\s]*(\d+\.?\d*)%',
        r'(\d+\.?\d*)%.*一年[期]?定期',
    ]
    for pattern in deposit_patterns:
        import re
        m = re.search(pattern, text)
        if m:
            rates['deposit_1Y'] = m.group(1)
            break
    
    # 国债收益率 10年
    bond10_patterns = [
        r'10年[期]?国债.*?收益率[:\s]*(\d+\.?\d*)%',
        r'10年[期]?收益率[:\s]*(\d+\.?\d*)%',
    ]
    for pattern in bond10_patterns:
        import re
        m = re.search(pattern, text)
        if m:
            rates['bond_10Y'] = m.group(1)
            break
    
    return rates

def compare_rates(old_data, new_rates):
    """对比旧数据和新数据，返回变化"""
    changes = []
    categories = {
        'depositRates': 'deposit',
        'LPR': 'LPR',
        'bondYields': 'bond',
        'SHIBOR': 'SHIBOR',
        'mortgageLPR': 'mortgage',
        'OMO': 'OMO',
        'RRR': 'RRR'
    }
    
    for category, prefix in categories.items():
        if category not in old_data:
            old_data[category] = {}
        if category not in new_rates:
            new_rates[category] = {}
        
        for key in set(list(old_data[category].keys()) + list(new_rates.get(category, {}).keys())):
            old_val = old_data[category].get(key, '')
            new_val = new_rates.get(category, {}).get(key, '')
            
            if old_val and new_val and old_val != new_val:
                try:
                    old_num = float(old_val)
                    new_num = float(new_val)
                    diff = new_num - old_num
                    diff_bp = round(diff * 100, 1)  # 转换为基点
                    changes.append({
                        'category': category,
                        'key': key,
                        'old': old_val,
                        'new': new_val,
                        'diff': f"{diff:+.2f}% ({diff_bp:+.0f}bp)"
                    })
                except:
                    pass
    
    return changes

def format_notification(changes, new_data):
    """格式化通知消息"""
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    msg = f"📊 中国利率变动日报 | {today}\n\n"
    
    # 按类别分组
    by_category = {}
    for c in changes:
        cat = c['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(c)
    
    # 存款利率
    if 'depositRates' in by_category:
        msg += "🏦 银行存款利率（基准）\n"
        for c in by_category['depositRates']:
            label = {'1year': '1年', '3year': '3年', '5year': '5年'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # LPR
    if 'LPR' in by_category:
        msg += "📊 LPR 贷款市场报价利率\n"
        for c in by_category['LPR']:
            label = {'1year': '1年期', '5yearPlus': '5年期以上'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # 国债
    if 'bondYields' in by_category:
        msg += "📉 国债收益率\n"
        for c in by_category['bondYields']:
            label = {'1year': '1年', '3year': '3年', '10year': '10年'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # SHIBOR
    if 'SHIBOR' in by_category:
        msg += "💧 SHIBOR 银行间拆借利率\n"
        for c in by_category['SHIBOR']:
            label = {'ON': 'O/N隔夜', '1W': '1W', '1M': '1M', '3M': '3M'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # 房贷
    if 'mortgageLPR' in by_category:
        msg += "🏠 房贷利率\n"
        for c in by_category['mortgageLPR']:
            msg += f"- 5年期以上LPR: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # 公开市场操作
    if 'OMO' in by_category:
        msg += "🔄 公开市场操作利率\n"
        for c in by_category['OMO']:
            label = {'repo7d': '7天逆回购', 'repo14d': '14天逆回购', 'MLF1Y': 'MLF 1年'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    # 存款准备金率
    if 'RRR' in by_category:
        msg += "💰 存款准备金率\n"
        for c in by_category['RRR']:
            label = {'large': '大型机构', 'small': '小型机构'}.get(c['key'], c['key'])
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    msg += "---\n"
    msg += "数据来源：中国人民银行、全国银行间同业拆借中心、中国债券信息网\n"
    
    return msg

def main():
    """
    主流程：
    1. 读取历史数据
    2. 接收新的利率数据（通过命令行参数）
    3. 对比变化
    4. 有变化则输出通知
    5. 更新数据文件
    """
    old_data = load_current_rates()
    
    # 从命令行参数获取新数据（JSON格式）
    if len(sys.argv) > 1:
        try:
            new_data = json.loads(sys.argv[1])
        except:
            print("Error: Invalid JSON input")
            sys.exit(1)
    else:
        # 无参数时，读取上次保存的数据作为"新数据"（演示用）
        new_data = old_data.copy()
        new_data['updateDate'] = datetime.now().strftime('%Y-%m-%d')
    
    # 对比变化
    changes = compare_rates(old_data, new_data)
    
    # 有变化则输出通知
    if changes:
        notification = format_notification(changes, new_data)
        print("[NOTIFY]")
        print(notification)
        print("[/NOTIFY]")
    
    # 更新数据文件
    new_data['updateDate'] = datetime.now().strftime('%Y-%m-%d')
    save_rates(new_data)
    
    if not changes:
        print("[OK] No changes detected. Data updated.")
    else:
        print(f"[OK] {len(changes)} rate(s) changed. Data updated.")

if __name__ == '__main__':
    main()
