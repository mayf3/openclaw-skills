#!/usr/bin/env python3
"""
股票投资分析脚本
完成 Level 1 快速分析：四维度评分系统
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
import re

# ANSI 颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def get_stock_name_from_code(stock_code):
    """根据股票代码获取股票名称"""
    # 这里可以扩展为更准确的股票名称获取方式
    # 目前使用简单的映射
    stock_mappings = {
        "600519": "贵州茅台",
        "300558": "贝达药业",
        "688266": "泽璟制药",
        "688185": "康希诺"
    }
    return stock_mappings.get(stock_code, f"未知股票{stock_code}")

def fetch_financial_data(stock_code):
    """获取财务数据（模拟数据）"""
    print_info("获取财务数据...")
    
    # 这里应该接入真实的财务数据API
    # 目前使用模拟数据进行演示
    mock_data = {
        "300558": {
            "stock_code": "300558",
            "stock_name": "贝达药业",
            "roe": 22.5,  # ROE 22.5%
            "gross_margin": 85.2,  # 毛利率 85.2%
            "cash_flow_ratio": 1.8,  # 现金流/净利润 1.8
            "roa": 18.3,  # ROA 18.3%
            "pe": 45.6,  # PE 45.6倍
            "pb": 8.2,  # PB 8.2倍
            "peg": 2.1,  # PEG 2.1
            "dividend_yield": 0.0,  # 分红率 0%
            "debt_ratio": 12.3  # 资产负债率 12.3%
        },
        "688266": {
            "stock_code": "688266",
            "stock_name": "泽璟制药",
            "roe": 21.8,  # ROE 21.8%
            "gross_margin": 75.6,  # 毛利率 75.6%
            "cash_flow_ratio": 1.5,  # 现金流/净利润 1.5
            "roa": 16.2,  # ROA 16.2%
            "pe": 68.9,  # PE 68.9倍
            "pb": 12.3,  # PB 12.3倍
            "peg": 3.2,  # PEG 3.2
            "dividend_yield": 0.0,  # 分红率 0%
            "debt_ratio": 8.7  # 资产负债率 8.7%
        },
        "688185": {
            "stock_code": "688185",
            "stock_name": "康希诺",
            "roe": 23.4,  # ROE 23.4%
            "gross_margin": 68.5,  # 毛利率 68.5%
            "cash_flow_ratio": 0.8,  # 现金流/净利润 0.8
            "roa": 19.8,  # ROA 19.8%
            "pe": 52.3,  # PE 52.3倍
            "pb": 6.8,  # PB 6.8倍
            "peg": 2.6,  # PEG 2.6
            "dividend_yield": 0.0,  # 分红率 0%
            "debt_ratio": 15.2  # 资产负债率 15.2%
        }
    }
    
    return mock_data.get(stock_code)

def calculate_financial_quality_score(data):
    """计算财务质量得分 (30%)"""
    print_info("计算财务质量得分...")
    
    score = 0
    details = []
    
    # ROE (30分满分，阈值≥15%)
    if data["roe"] >= 15:
        roe_score = min(30, 30 * (data["roe"] - 10) / 20)  # 线性增长
        score += roe_score
        details.append(f"ROE {data['roe']}%: +{roe_score:.1f}分")
    else:
        roe_score = 30 * (data["roe"] / 15)  # 按比例扣分
        score += roe_score
        details.append(f"ROE {data['roe']}%: +{roe_score:.1f}分 (低于标准)")
    
    # 毛利率 (25分满分，阈值≥30%)
    if data["gross_margin"] >= 30:
        margin_score = min(25, 25 * (data["gross_margin"] / 50))  # 线性增长
        score += margin_score
        details.append(f"毛利率 {data['gross_margin']}%: +{margin_score:.1f}分")
    else:
        margin_score = 25 * (data["gross_margin"] / 30)
        score += margin_score
        details.append(f"毛利率 {data['gross_margin']}%: +{margin_score:.1f}分 (低于标准)")
    
    # 现金流/净利润 (25分满分，阈值≥1.0)
    if data["cash_flow_ratio"] >= 1.0:
        cash_score = min(25, 25 * min(data["cash_flow_ratio"] / 2, 1))
        score += cash_score
        details.append(f"现金流/净利润 {data['cash_flow_ratio']}: +{cash_score:.1f}分")
    else:
        cash_score = 25 * data["cash_flow_ratio"]
        score += cash_score
        details.append(f"现金流/净利润 {data['cash_flow_ratio']}: +{cash_score:.1f}分 (低于标准)")
    
    # ROA (20分满分，阈值≥8%)
    if data["roa"] >= 8:
        roa_score = min(20, 20 * (data["roa"] - 5) / 15)
        score += roa_score
        details.append(f"ROA {data['roa']}%: +{roa_score:.1f}分")
    else:
        roa_score = 20 * (data["roa"] / 8)
        score += roa_score
        details.append(f"ROA {data['roa']}%: +{roa_score:.1f}分 (低于标准)")
    
    return round(score, 1), details

def calculate_valuation_score(data):
    """计算估值得分 (30%)"""
    print_info("计算估值得分...")
    
    score = 0
    details = []
    
    # PE (40分满分，阈值≤30)
    if data["pe"] <= 30:
        pe_score = 40
        details.append(f"PE {data['pe']}倍: +{pe_score}分 (优秀)")
    elif data["pe"] <= 50:
        pe_score = 40 * (1 - (data["pe"] - 30) / 40)
        score += pe_score
        details.append(f"PE {data['pe']}倍: +{pe_score:.1f}分 (合理)")
    else:
        pe_score = 40 * max(0, (50 - data["pe"]) / 20)
        score += pe_score
        details.append(f"PE {data['pe']}倍: +{pe_score:.1f}分 (偏高)")
    
    # PB (30分满分，阈值≤5)
    if data["pb"] <= 5:
        pb_score = 30
        details.append(f"PB {data['pb']}倍: +{pb_score}分 (优秀)")
    elif data["pb"] <= 8:
        pb_score = 30 * (1 - (data["pb"] - 5) / 6)
        score += pb_score
        details.append(f"PB {data['pb']}倍: +{pb_score:.1f}分 (合理)")
    else:
        pb_score = 30 * max(0, (8 - data["pb"]) / 6)
        score += pb_score
        details.append(f"PB {data['pb']}倍: +{pb_score:.1f}分 (偏高)")
    
    # PEG (30分满分，阈值≤1.5)
    if data["peg"] <= 1.5:
        peg_score = 30
        details.append(f"PEG {data['peg']}: +{peg_score}分 (优秀)")
    elif data["peg"] <= 2.5:
        peg_score = 30 * (1 - (data["peg"] - 1.5) / 2)
        score += peg_score
        details.append(f"PEG {data['peg']}: +{peg_score:.1f}分 (合理)")
    else:
        peg_score = 30 * max(0, (2.5 - data["peg"]) / 2)
        score += peg_score
        details.append(f"PEG {data['peg']}: +{peg_score:.1f}分 (偏高)")
    
    return round(score, 1), details

def calculate_moat_score(data):
    """计算护城河得分 (25%)"""
    print_info("计算护城河得分...")
    
    score = 0
    details = []
    
    # 根据行业特点给护城河评分
    stock_code = data["stock_code"]
    
    if stock_code == "300558":  # 贝达药业
        # 创新药企，专利壁垒强
        score += 20  # 专利护城河
        score += 5   # 技术壁垒
        details.append("专利壁垒: +20分")
        details.append("技术壁垒: +5分")
    elif stock_code == "688266":  # 泽璟制药
        # 生物创新药，研发能力重要
        score += 18  # 研发能力
        score += 5   # 技术积累
        details.append("研发能力: +18分")
        details.append("技术积累: +5分")
    elif stock_code == "688185":  # 康希诺
        # 疫苗企业，技术平台重要
        score += 15  # 技术平台
        score += 8   # 监管壁垒
        details.append("技术平台: +15分")
        details.append("监管壁垒: +8分")
    
    # 调整总分到25分满分
    score = min(25, score * 0.8)  # 缩放到25分满分
    
    return round(score, 1), details

def calculate_management_score(data):
    """计算管理层得分 (15%)"""
    print_info("计算管理层得分...")
    
    score = 0
    details = []
    
    # 分红率评分
    if data["dividend_yield"] >= 30:
        dividend_score = 8
        details.append(f"分红率 {data['dividend_yield']}%: +{dividend_score}分 (优秀)")
    elif data["dividend_yield"] >= 20:
        dividend_score = 6
        details.append(f"分红率 {data['dividend_yield']}%: +{dividend_score}分 (良好)")
    elif data["dividend_yield"] >= 10:
        dividend_score = 4
        details.append(f"分红率 {data['dividend_yield']}%: +{dividend_score}分 (一般)")
    else:
        dividend_score = 2
        details.append(f"分红率 {data['dividend_yield']}%: +{dividend_score}分 (偏低)")
    
    score += dividend_score
    
    # 资产负债率评分（财务稳健性）
    if data["debt_ratio"] <= 30:
        debt_score = 7
        details.append(f"资产负债率 {data['debt_ratio']}%: +{debt_score}分 (优秀)")
    elif data["debt_ratio"] <= 50:
        debt_score = 5
        details.append(f"资产负债率 {data['debt_ratio']}%: +{debt_score}分 (良好)")
    else:
        debt_score = 3
        details.append(f"资产负债率 {data['debt_ratio']}%: +{debt_score}分 (偏高)")
    
    score += debt_score
    
    return round(score, 1), details

def get_investment_advice(total_score):
    """根据总分给出投资建议"""
    if total_score >= 90:
        return "强烈买入", "🔴"
    elif total_score >= 80:
        return "买入", "🟠"
    elif total_score >= 70:
        return "观望", "🟡"
    elif total_score >= 60:
        return "谨慎", "🟢"
    else:
        return "回避", "⚪"

def create_directory_structure(base_path, stock_code, stock_name):
    """创建目录结构"""
    print_info("创建目录结构...")
    
    stock_dir = base_path / f"{stock_code}-{stock_name}"
    data_dir = stock_dir / "data"
    financial_dir = stock_dir / "financial-reports"
    reports_dir = stock_dir / "reports"
    
    # 创建目录
    for dir_path in [stock_dir, data_dir, financial_dir, reports_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"创建目录: {dir_path}")
    
    return stock_dir, data_dir, reports_dir

def save_financial_data(data, data_dir):
    """保存财务数据"""
    print_info("保存财务数据...")
    
    # 保存综合财务数据
    financial_file = data_dir / "financial.json"
    with open(financial_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print_success(f"保存财务数据: {financial_file}")
    
    # 保存估值数据
    valuation_file = data_dir / "valuation.json"
    valuation_data = {
        "pe": data["pe"],
        "pb": data["pb"],
        "peg": data["peg"],
        "pe_industry_avg": 35.2,
        "pb_industry_avg": 6.8,
        "valuation_method": "相对估值法"
    }
    with open(valuation_file, "w", encoding="utf-8") as f:
        json.dump(valuation_data, f, ensure_ascii=False, indent=2)
    print_success(f"保存估值数据: {valuation_file}")

def save_metadata(stock_dir, stock_code, stock_name, total_score, advice, advice_emoji):
    """保存 metadata.json"""
    print_info("保存 metadata.json...")
    
    metadata = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "analysis_type": "Level 1",
        "total_score": total_score,
        "investment_advice": advice,
        "investment_emoji": advice_emoji,
        "analysis_levels": {
            "level_1": {
                "name": "四维度快速分析",
                "file": "reports/价值投资分析.md",
                "completed": True,
                "last_update": datetime.now().strftime("%Y-%m-%d")
            }
        },
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    metadata_file = stock_dir / "metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print_success(f"保存 metadata: {metadata_file}")

def generate_analysis_report(stock_dir, stock_data, financial_score, financial_details, 
                           valuation_score, valuation_details, moat_score, moat_details,
                           management_score, management_details, total_score, advice, advice_emoji):
    """生成分析报告"""
    print_info("生成分析报告...")
    
    report_file = stock_dir / "reports" / "价值投资分析.md"
    
    report_content = f"""# {stock_data['stock_name']} ({stock_data['stock_code']}) - 价值投资分析报告

**分析日期**: {datetime.now().strftime('%Y-%m-%d')}  
**分析类型**: Level 1 四维度快速分析  
**综合评分**: {total_score}/100  
**投资建议**: {advice_emoji} {advice}

---

## 📊 综合评分与投资建议

### 评分分布
- 财务质量: {financial_score}/30 (30% 权重)
- 估值水平: {valuation_score}/30 (30% 权重)  
- 护城河: {moat_score}/25 (25% 权重)
- 管理层: {management_score}/15 (15% 权重)
- **总分**: {total_score}/100

### 投资建议
{advice}

---

## 📈 财务质量分析 (30分)

### 核心指标
- **ROE**: {stock_data['roe']}%
- **毛利率**: {stock_data['gross_margin']}%
- **现金流/净利润**: {stock_data['cash_flow_ratio']}
- **ROA**: {stock_data['roa']}%

### 得分详情
{'\n'.join(f"- {detail}" for detail in financial_details)}

### 财务质量评估
{get_financial_quality_assessment(stock_data)}

---

## 💰 估值分析 (30分)

### 核心指标
- **PE**: {stock_data['pe']}倍
- **PB**: {stock_data['pb']}倍
- **PEG**: {stock_data['peg']}
- **行业平均PE**: 35.2倍

### 得分详情
{'\n'.join(f"- {detail}" for detail in valuation_details)}

### 估值评估
{get_valuation_assessment(stock_data)}

---

## 🏰 护城河分析 (25分)

### 得分详情
{'\n'.join(f"- {detail}" for detail in moat_details)}

### 护城河评估
{get_moat_assessment(stock_data)}

---

## 👥 管理层分析 (15分)

### 核心指标
- **分红率**: {stock_data['dividend_yield']}%
- **资产负债率**: {stock_data['debt_ratio']}%

### 得分详情
{'\n'.join(f"- {detail}" for detail in management_details)}

### 管理层评估
{get_management_assessment(stock_data)}

---

## ⚠️ 风险提示

{get_risk_warnings(stock_data)}

---

## 💡 投资策略建议

{get_investment_strategy(stock_data, total_score, advice)}

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*分析方法: 四维度价值投资评分系统*  
*免责声明: 本报告仅供参考，不构成投资建议*
"""
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print_success(f"生成分析报告: {report_file}")

def get_financial_quality_assessment(data):
    """财务质量评估"""
    assessment = []
    
    if data["roe"] >= 15:
        assessment.append("✅ ROE表现优秀，盈利能力强")
    else:
        assessment.append("❌ ROE偏低，盈利能力有待提升")
    
    if data["gross_margin"] >= 30:
        assessment.append("✅ 毛利率优秀，产品竞争力强")
    else:
        assessment.append("❌ 毛利率偏低，成本控制需要改善")
    
    if data["cash_flow_ratio"] >= 1.0:
        assessment.append("✅ 现金流健康，盈利质量高")
    else:
        assessment.append("⚠️ 现金流偏弱，盈利质量需要关注")
    
    return '\n'.join(f"  {item}" for item in assessment)

def get_valuation_assessment(data):
    """估值评估"""
    assessment = []
    
    if data["pe"] <= 30:
        assessment.append("✅ 估值合理，具有安全边际")
    elif data["pe"] <= 50:
        assessment.append("⚠️ 估值偏高，需要谨慎")
    else:
        assessment.append("❌ 估值过高，存在泡沫风险")
    
    if data["pb"] <= 5:
        assessment.append("✅ PB估值合理，股价相对便宜")
    elif data["pb"] <= 8:
        assessment.append("⚠️ PB估值偏高，需要关注")
    else:
        assessment.append("❌ PB估值过高，风险较大")
    
    return '\n'.join(f"  {item}" for item in assessment)

def get_moat_assessment(data):
    """护城河评估"""
    stock_code = data["stock_code"]
    
    if stock_code == "300558":  # 贝达药业
        return """  ✅ 拥有强大的专利壁垒，创新药研发能力强
  ✅ 技术积累深厚，新产品管线丰富
  ⚠️ 新药研发周期长，存在不确定性"""
    elif stock_code == "688266":  # 泽璟制药
        return """  ✅ 多平台技术路线，研发能力突出
  ✅ 产品线覆盖广，风险分散
  ⚠️ 竞争激烈，需要持续投入"""
    elif stock_code == "688185":  # 康希诺
        return """  ✅ 独特的腺病毒载体技术平台
  ✅ 在鼻喷疫苗领域有先发优势
  ⚠️ 疫苗行业竞争激烈，需求波动大"""
    else:
        return """  ⚠️ 护城河分析需要更多行业信息"""

def get_management_assessment(data):
    """管理层评估"""
    assessment = []
    
    if data["dividend_yield"] >= 30:
        assessment.append("✅ 分红积极，股东回报意识强")
    elif data["dividend_yield"] >= 20:
        assessment.append("✅ 分红稳定，关注股东回报")
    else:
        assessment.append("❌ 分红率低，股东回报意识弱")
    
    if data["debt_ratio"] <= 30:
        assessment.append("✅ 财务稳健，负债水平合理")
    elif data["debt_ratio"] <= 50:
        assessment.append("⚠️ 负债水平中等，需要关注")
    else:
        assessment.append("❌ 负债水平较高，财务风险大")
    
    return '\n'.join(f"  {item}" for item in assessment)

def get_risk_warnings(data):
    """风险提示"""
    stock_code = data["stock_code"]
    
    if stock_code == "300558":  # 贝达药业
        return """  - ⚠️ 新药研发失败风险
  - ⚠️ 集采政策变化风险
  - ⚠️ 竞争加剧风险
  - ⚠️ 估值偏高风险"""
    elif stock_code == "688266":  # 泽璟制药
        return """  - ⚠️ 研发投入大，短期内可能亏损
  - ⚠️ 产品商业化不及预期风险
  - ⚠️ 竞争激烈风险
  - ⚠️ 估值过高风险"""
    elif stock_code == "688185":  # 康希诺
        return """  - ⚠️ 疫苗需求波动大
  - ⚠️ 竞争激烈风险
  - ⚠️ 研发周期长风险
  - ⚠️ 估值波动大"""
    else:
        return """  - ⚠️ 行业竞争风险
  - ⚠️ 宏观经济影响
  - ⚠️ 监管政策变化"""

def get_investment_strategy(data, total_score, advice):
    """投资策略建议"""
    stock_code = data["stock_code"]
    
    if advice == "强烈买入":
        return f"""  📈 **建议立即建仓**
  
  - 买入区间: {get_buying_range(stock_code)}
  - 目标价位: {get_target_price(stock_code)}
  - 建议仓位: 8-12%
  - 持有周期: 长期(3-5年)
  
  💡 **操作建议**: 
  - 分批建仓，降低风险
  - 长期持有，享受成长红利
  - 定期关注财报变化"""
    elif advice == "买入":
        return f"""  📈 **建议逢低配置**
  
  - 理想买点: {get_buying_range(stock_code)}
  - 目标价位: {get_target_price(stock_code)}
  - 建议仓位: 5-8%
  - 持有周期: 中长期(2-3年)
  
  💡 **操作建议**: 
  - 等待估值回调
  - 分批建仓控制风险
  - 关注催化剂事件"""
    elif advice == "观望":
        return f"""  ⏳ **建议观望等待**
  
  - 观望条件: {get_watch_conditions(stock_code)}
  - 买入信号: 等待 {get_buy_signals(stock_code)}
  - 建议仓位: 暂不建仓
  
  💡 **操作建议**: 
  - 关注业绩改善信号
  - 等待估值回落
  - 谨慎乐观，暂不行动"""
    elif advice == "谨慎":
        return f"""  🛡️ **建议谨慎观望**
  
  - 风险点: {get_risk_points(stock_code)}
  - 建仓位: 暂不建仓或极小仓位(<3%)
  - 止损位: {get_stop_loss(stock_code)}
  
  💡 **操作建议**: 
  - 等待基本面改善
  - 极小仓位试错
  - 严格止损控制风险"""
    else:
        return """  ❌ **建议回避**
  
  - 主要风险: 基本面较差
  - 建议仓位: 0%
  - 关注替代标的
  
  💡 **操作建议**: 
  - 寻找更好的投资机会
  - 暂不考虑投资"""

def get_buying_range(stock_code):
    """获取建议买入区间"""
    ranges = {
        "300558": "85-95元",
        "688266": "45-55元", 
        "688185": "55-65元"
    }
    return ranges.get(stock_code, "待定")

def get_target_price(stock_code):
    """获取目标价位"""
    targets = {
        "300558": "110-130元",
        "688266": "70-90元",
        "688185": "80-100元"
    }
    return targets.get(stock_code, "待定")

def get_watch_conditions(stock_code):
    """获取观望条件"""
    conditions = {
        "300558": "PE回落至30-35倍",
        "688266": "估值回调至50倍以下",
        "688185": "业绩验证+估值回调"
    }
    return conditions.get(stock_code, "待定")

def get_buy_signals(stock_code):
    """获取买入信号"""
    signals = {
        "300558": "新药上市或医保谈判成功",
        "688266": "新产品商业化进展",
        "688185": "疫苗需求恢复"
    }
    return signals.get(stock_code, "待定")

def get_risk_points(stock_code):
    """获取主要风险点"""
    risks = {
        "300558": "估值偏高+研发风险",
        "688266": "商业化不确定性",
        "688185": "需求波动+竞争"
    }
    return risks.get(stock_code, "待定")

def get_stop_loss(stock_code):
    """获取止损位"""
    stops = {
        "300558": "70元",
        "688266": "35元",
        "688185": "45元"
    }
    return stops.get(stock_code, "待定")

def validate_structure(stock_dir):
    """验证目录结构"""
    print_info("验证目录结构...")
    
    # 导入验证脚本
    sys.path.append(str(Path(__file__).parent / "scripts"))
    from validate_structure import main as validate_main
    
    # 临时修改参数
    original_argv = sys.argv
    sys.argv = ["validate_structure.py", str(stock_dir)]
    
    try:
        validate_main()
        return True
    except SystemExit:
        return False
    finally:
        sys.argv = original_argv

def analyze_stock(stock_code):
    """分析单只股票"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}开始分析股票: {stock_code}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # 获取股票名称
    stock_name = get_stock_name_from_code(stock_code)
    
    # 获取财务数据
    stock_data = fetch_financial_data(stock_code)
    if not stock_data:
        print_error(f"无法获取股票 {stock_code} 的数据")
        return False
    
    print(f"📊 基本信息:")
    print(f"   股票代码: {stock_data['stock_code']}")
    print(f"   股票名称: {stock_data['stock_name']}")
    print(f"   ROE: {stock_data['roe']}%")
    print(f"   毛利率: {stock_data['gross_margin']}%")
    print(f"   PE: {stock_data['pe']}倍")
    print(f"   PB: {stock_data['pb']}倍")
    print()
    
    # 计算各维度得分
    financial_score, financial_details = calculate_financial_quality_score(stock_data)
    valuation_score, valuation_details = calculate_valuation_score(stock_data)
    moat_score, moat_details = calculate_moat_score(stock_data)
    management_score, management_details = calculate_management_score(stock_data)
    
    # 计算总分
    total_score = financial_score + valuation_score + moat_score + management_score
    total_score = round(total_score, 1)
    
    # 获取投资建议
    advice, advice_emoji = get_investment_advice(total_score)
    
    print(f"📈 各维度得分:")
    print(f"   财务质量: {financial_score}/30")
    print(f"   估值水平: {valuation_score}/30") 
    print(f"   护城河: {moat_score}/25")
    print(f"   管理层: {management_score}/15")
    print(f"   总分: {total_score}/100")
    print(f"   投资建议: {advice_emoji} {advice}")
    print()
    
    # 创建目录结构
    base_path = Path.home() / "workspace" / "blog" / "knowledge-base" / "docs" / "投资分析" / "stocks"
    stock_dir, data_dir, reports_dir = create_directory_structure(base_path, stock_code, stock_name)
    
    # 保存数据
    save_financial_data(stock_data, data_dir)
    save_metadata(stock_dir, stock_code, stock_name, total_score, advice, advice_emoji)
    
    # 生成分析报告
    generate_analysis_report(stock_dir, stock_data, financial_score, financial_details,
                           valuation_score, valuation_details, moat_score, moat_details,
                           management_score, management_details, total_score, advice, advice_emoji)
    
    # 验证结构
    if validate_structure(stock_dir):
        print_success("✅ 分析完成！目录结构验证通过")
    else:
        print_warning("⚠️ 分析完成，但目录结构验证有警告")
    
    print(f"\n{GREEN}股票 {stock_code} 分析完成！{RESET}")
    print(f"报告位置: {stock_dir}/reports/价值投资分析.md")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze_stock.py <股票代码>")
        print("示例: python3 analyze_stock.py 300558")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    
    # 分析股票
    success = analyze_stock(stock_code)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()