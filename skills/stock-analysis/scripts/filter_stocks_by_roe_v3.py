import requests
import pandas as pd
import time
from datetime import datetime
import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 新浪财经股票数据API
SINA_STOCK_API = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={}&num=40&sort=symbol&asc=1&node=hs_a"

# 新浪财经财务数据页面模板
SINA_FINANCE_PAGE = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{}/displaytype/4.phtml"

def setup_driver():
    """设置Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def get_stock_list():
    """获取股票列表及基础信息（包括行业）"""
    stock_list = []
    page = 1
    
    while True:
        url = SINA_STOCK_API.format(page)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                # 提取股票代码、名称和行业
                for stock in data:
                    stock_list.append({
                        'code': stock.get('code', ''),
                        'name': stock.get('name', ''),
                        'industry': stock.get('industry', '未知行业')
                    })
                page += 1
                time.sleep(0.5)  # 避免请求过于频繁
            else:
                break
        except Exception as e:
            print(f"获取股票列表时出错: {e}")
            break
    
    return stock_list

def get_roe_from_sina(stock_code, years, driver):
    """从新浪财经获取ROE数据"""
    try:
        url = SINA_FINANCE_PAGE.format(stock_code)
        driver.get(url)
        time.sleep(2)  # 等待页面加载
        
        # 查找包含财务指标的表格
        tables = driver.find_elements(By.TAG_NAME, "table")
        roe_data = {}
        
        current_year = datetime.now().year
        
        # 遍历表格查找ROE数据
        for table in tables:
            try:
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) > 1:
                        # 查找包含"净资产收益率"的行
                        if "净资产收益率" in cells[0].text:
                            # 获取最近N年的数据
                            for i in range(1, min(len(cells), years + 1)):
                                year = current_year - i
                                try:
                                    # 提取数值，去掉百分号
                                    value_text = cells[i].text.replace('%', '').strip()
                                    if value_text and value_text != '--':
                                        roe_data[str(year)] = float(value_text)
                                except ValueError:
                                    continue
                            break
                if roe_data:
                    break
            except Exception:
                continue
                
        return roe_data
    except Exception as e:
        print(f"获取 {stock_code} ROE数据时出错: {e}")
        return {}

def filter_stocks_by_roe(stock_list, years, min_roe):
    """根据ROE筛选股票"""
    driver = setup_driver()
    filtered_stocks = []
    
    try:
        for i, stock in enumerate(stock_list):
            stock_code = stock['code']
            stock_name = stock['name']
            industry = stock['industry']
            
            if not stock_code:
                continue
                
            try:
                print(f"正在处理 {stock_code} {stock_name} ({i+1}/{len(stock_list)})")
                roe_data = get_roe_from_sina(stock_code, years, driver)
                
                # 检查是否所有年份的ROE都满足条件
                if len(roe_data) >= years and all(roe >= min_roe for roe in roe_data.values()):
                    # 计算平均ROE
                    avg_roe = sum(roe_data.values()) / len(roe_data)
                    filtered_stocks.append({
                        'code': stock_code,
                        'name': stock_name,
                        'industry': industry,
                        'roe_data': roe_data,
                        'avg_roe': avg_roe
                    })
                    print(f"  符合条件: {stock_name} - 平均ROE: {avg_roe:.2f}%")
            except Exception as e:
                print(f"处理 {stock_code} 时出错: {e}")
            
            # 避免请求过于频繁
            time.sleep(1)
            
    finally:
        driver.quit()
    
    return filtered_stocks

def categorize_industries(stocks):
    """对行业进行分类统计"""
    industry_stats = {}
    
    for stock in stocks:
        industry = stock['industry']
        if industry not in industry_stats:
            industry_stats[industry] = {
                'count': 0,
                'stocks': [],
                'avg_roe': 0
            }
        
        industry_stats[industry]['count'] += 1
        industry_stats[industry]['stocks'].append(stock)
    
    # 计算各行业平均ROE
    for industry, stats in industry_stats.items():
        total_roe = sum(stock['avg_roe'] for stock in stats['stocks'])
        stats['avg_roe'] = total_roe / len(stats['stocks']) if stats['stocks'] else 0
    
    return industry_stats

def save_to_excel(stocks, industry_stats, filename):
    """将筛选结果保存到Excel文件"""
    # 创建股票数据DataFrame
    df_data = []
    for stock in stocks:
        row = {
            '股票代码': stock['code'],
            '股票名称': stock['name'],
            '行业': stock['industry'],
            '平均ROE': f"{stock['avg_roe']:.2f}%"
        }
        # 添加每年的ROE数据
        for year, roe in stock['roe_data'].items():
            row[f'ROE_{year}'] = f"{roe}%"
        df_data.append(row)
    
    df_stocks = pd.DataFrame(df_data)
    
    # 创建行业统计数据DataFrame
    industry_data = []
    for industry, stats in industry_stats.items():
        industry_data.append({
            '行业': industry,
            '公司数量': stats['count'],
            '平均ROE': f"{stats['avg_roe']:.2f}%"
        })
    
    df_industries = pd.DataFrame(industry_data)
    
    # 保存到Excel文件的不同工作表
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_stocks.to_excel(writer, sheet_name='符合条件的股票', index=False)
        df_industries.to_excel(writer, sheet_name='行业统计', index=False)
    
    print(f"筛选结果已保存到 {filename}")

def main():
    parser = argparse.ArgumentParser(description='筛选过去N年ROE持续大于指定值的公司')
    parser.add_argument('--years', type=int, default=5, help='过去几年的数据 (默认: 5)')
    parser.add_argument('--min_roe', type=float, default=20.0, help='ROE最小值 (默认: 20.0)')
    
    args = parser.parse_args()
    years = args.years
    min_roe = args.min_roe
    
    print(f"正在获取股票列表...")
    stock_list = get_stock_list()
    print(f"共获取到 {len(stock_list)} 只股票")
    
    print(f"正在筛选过去 {years} 年ROE持续大于 {min_roe}% 的公司...")
    filtered_stocks = filter_stocks_by_roe(stock_list, years, min_roe)
    
    # 按行业分类统计
    industry_stats = categorize_industries(filtered_stocks)
    
    # 保存结果到Excel文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"filtered_stocks_{timestamp}.xlsx"
    save_to_excel(filtered_stocks, industry_stats, filename)
    
    # 打印行业统计摘要
    print("\n行业统计摘要:")
    print("-" * 50)
    sorted_industries = sorted(industry_stats.items(), key=lambda x: x[1]['count'], reverse=True)
    for industry, stats in sorted_industries:
        print(f"{industry}: {stats['count']} 家公司, 平均ROE: {stats['avg_roe']:.2f}%")
    
    print(f"\n筛选完成，共找到 {len(filtered_stocks)} 家符合条件的公司")
    print(f"详细结果已保存到 {filename}")

if __name__ == "__main__":
    main()