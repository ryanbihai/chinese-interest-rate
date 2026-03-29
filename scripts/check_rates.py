#!/usr/bin/env python3
"""
利率监测脚本 - 检查银行存款利率和国债收益率变动
每日执行，有变化立即推送微信通知
"""

import json
import re
import sys
from datetime import datetime, date
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_FILE = SKILL_DIR / "data" / "rates.json"

def load_rates():
    """读取历史利率数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_rates(data):
    """保存今日利率数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_percentage(text):
    """从文本中提取百分比数值"""
    patterns = [
        r'(\d+\.\d{2})%',
        r'(\d+\.\d+)%',
        r'(\d+\.?\d*)\s*%',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

def format_change(old_val, new_val):
    """计算变动值"""
    if old_val == "" or new_val == "":
        return ""
    try:
        diff = round(float(new_val) - float(old_val), 2)
        if diff > 0:
            return f"+{diff:.2f}%"
        elif diff < 0:
            return f"{diff:.2f}%"
        else:
            return "0.00%"
    except:
        return ""

def parse_rates_from_search(search_output):
    """从搜索结果文本中解析利率数据"""
    results = {
        "depositRates": {"1year": "", "3year": "", "5year": ""},
        "bondYields": {"1year": "", "10year": ""}
    }
    
    # 解析搜索结果
    text = str(search_output).lower()
    
    # 1年期定期存款利率 - 常见关键词
    for pattern in [
        r'1年.*?定期.*?(\d+\.\d{2})%',
        r'一年.*?定期.*?(\d+\.\d{2})%',
        r'一年期.*?存款.*?(\d+\.\d{2})%',
        r'定期1年.*?(\d+\.\d{2})%',
    ]:
        match = re.search(pattern, text)
        if match:
            results["depositRates"]["1year"] = match.group(1)
            break
    
    # 3年期定期存款利率
    for pattern in [
        r'3年.*?定期.*?(\d+\.\d{2})%',
        r'三年.*?定期.*?(\d+\.\d{2})%',
        r'三年期.*?存款.*?(\d+\.\d{2})%',
    ]:
        match = re.search(pattern, text)
        if match:
            results["depositRates"]["3year"] = match.group(1)
            break
    
    # 5年期定期存款利率
    for pattern in [
        r'5年.*?定期.*?(\d+\.\d{2})%',
        r'五年.*?定期.*?(\d+\.\d{2})%',
        r'五年期.*?存款.*?(\d+\.\d{2})%',
    ]:
        match = re.search(pattern, text)
        if match:
            results["depositRates"]["5year"] = match.group(1)
            break
    
    # 1年期国债收益率
    for pattern in [
        r'1年.*?国债.*?(\d+\.\d{2})%',
        r'一年.*?国债.*?收益率.*?(\d+\.\d{2})%',
        r'国债1年.*?(\d+\.\d{2})%',
    ]:
        match = re.search(pattern, text)
        if match:
            results["bondYields"]["1year"] = match.group(1)
            break
    
    # 10年期国债收益率
    for pattern in [
        r'10年.*?国债.*?(\d+\.\d{2})%',
        r'十年.*?国债.*?收益率.*?(\d+\.\d{2})%',
        r'国债10年.*?(\d+\.\d{2})%',
        r'10y.*?国债.*?(\d+\.\d{2})%',
    ]:
        match = re.search(pattern, text)
        if match:
            results["bondYields"]["10year"] = match.group(1)
            break
    
    return results

def compare_and_build_message(old_data, new_data):
    """比较新旧数据，有变化则构建通知消息"""
    changes = []
    
    # 检查存款利率变动
    deposit_items = [
        ("1年期", old_data.get("depositRates", {}).get("1year", ""), 
               new_data.get("depositRates", {}).get("1year", "")),
        ("3年期", old_data.get("depositRates", {}).get("3year", ""), 
               new_data.get("depositRates", {}).get("3year", "")),
        ("5年期", old_data.get("depositRates", {}).get("5year", ""), 
               new_data.get("depositRates", {}).get("5year", "")),
    ]
    
    # 检查国债收益率变动
    bond_items = [
        ("1年期", old_data.get("bondYields", {}).get("1year", ""), 
               new_data.get("bondYields", {}).get("1year", "")),
        ("10年期", old_data.get("bondYields", {}).get("10year", ""), 
               new_data.get("bondYields", {}).get("10year", "")),
    ]
    
    has_changes = False
    deposit_changes = []
    bond_changes = []
    
    for name, old_val, new_val in deposit_items:
        if new_val and new_val != old_val:
            change = format_change(old_val, new_val)
            deposit_changes.append(f"- {name}: {new_val}% （{change}）")
            has_changes = True
    
    for name, old_val, new_val in bond_items:
        if new_val and new_val != old_val:
            change = format_change(old_val, new_val)
            bond_changes.append(f"- {name}: {new_val}% （{change}）")
            has_changes = True
    
    if not has_changes:
        return None
    
    # 构建消息
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"📊 利率变动提醒 | 北京时间 {now}\n\n🏦 银行存款利率\n"
    
    if deposit_changes:
        message += "\n".join(deposit_changes) + "\n"
    else:
        message += "（无变动）\n"
    
    message += "\n📈 国债收益率\n"
    if bond_changes:
        message += "\n".join(bond_changes) + "\n"
    else:
        message += "（无变动）\n"
    
    message += "\n⚠️ 请注意利率变化，及时调整您的理财策略"
    
    return message

def main():
    """主函数"""
    print("=" * 50)
    print("🏦 利率监测开始执行...")
    print("=" * 50)
    
    # 1. 读取历史数据
    old_rates = load_rates()
    print(f"📂 历史数据: {old_rates}")
    
    # 2. 获取今日数据（从搜索结果解析）
    # 这里需要通过外部调用 web_search 获取数据
    # 脚本接收命令行参数传入搜索结果
    
    if len(sys.argv) > 1:
        search_results = " ".join(sys.argv[1:])
        new_rates = parse_rates_from_search(search_results)
    else:
        print("⚠️ 未提供搜索结果参数，请提供 web_search 返回的数据")
        return
    
    print(f"📥 今日数据: {new_rates}")
    
    # 3. 对比数据
    if old_rates:
        message = compare_and_build_message(old_rates, new_rates)
        if message:
            print("\n📨 检测到变动，准备发送通知...")
            print("-" * 50)
            print(message)
            print("-" * 50)
            # 输出标记，供外部捕获
            print(f"\n[NOTIFY]\n{message}\n[/NOTIFY]")
        else:
            print("\n✅ 今日利率无变动，不发送通知")
    else:
        print("\n📝 首次运行，初始化数据...")
    
    # 4. 更新数据文件
    today = date.today().strftime("%Y-%m-%d")
    new_data = {
        "updateDate": today,
        "depositRates": new_rates.get("depositRates", {}),
        "bondYields": new_rates.get("bondYields", {})
    }
    save_rates(new_data)
    print(f"\n💾 数据已保存至: {DATA_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
