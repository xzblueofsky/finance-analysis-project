# src/visualization.py

import sys
import os

# 添加项目根目录到 sys.path
sys.path.append('.')

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from config import COMPANY_CODES, STATEMENT_CONFIG

def visualize_income_statement(input_file, company_codes=None, company_names=None):
    """
    对指定公司，绘制利润表财务指标的时间序列图。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))

    # 设置字体和处理负号显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 指定字体路径（请根据你的系统调整路径）
    font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 苹方字体路径
    font_prop = FontProperties(fname=font_path)

    # 确保日期列为字符串类型，便于排序
    df['报告期'] = df['报告期'].astype(str)

    # 指标列表
    revenue_indicator = ['营业收入']
    ratio_indicators = ['毛利率', '费用率', '营业利润率', '毛利润费用占比']

    # 如果指定了公司代码，按照代码筛选
    if company_codes:
        df_selected = df[df['股票代码'].isin(company_codes)]
    elif company_names:
        df_selected = df[df['股票简称'].isin(company_names)]
    else:
        print("请指定公司代码列表或公司名称列表。")
        return

    # 按照报告期排序
    df_selected.sort_values(by='报告期', inplace=True)

    for company in df_selected['股票简称'].unique():
        df_company = df_selected[df_selected['股票简称'] == company]

        # 创建以公司名称命名的文件夹
        company_dir = os.path.join('data', 'analysis', company)
        os.makedirs(company_dir, exist_ok=True)

        # 绘制营业收入的变化趋势
        plt.figure(figsize=(12, 6))
        plt.plot(df_company['报告期'], df_company['营业收入'], marker='o', label='营业收入')
        plt.title(f'{company} 营业收入变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('营业收入（单位：万元）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = os.path.join(company_dir, f'{company}_营业收入变化趋势.png')
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

        # 绘制比值指标的变化趋势
        plt.figure(figsize=(12, 6))
        for indicator in ratio_indicators:
            plt.plot(df_company['报告期'], df_company[indicator], marker='o', label=indicator)
        plt.title(f'{company} 财务比率指标变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('比率（单位：小数）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = os.path.join(company_dir, f'{company}_财务比率指标变化趋势.png')
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

def visualize_cash_flow_statement(input_file, company_codes=None, company_names=None):
    """
    对指定公司，绘制现金流量指标的时间序列图。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))

    # 设置字体和处理负号显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 指定字体路径（请根据你的系统调整路径）
    font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 苹方字体路径
    font_prop = FontProperties(fname=font_path)

    # 确保日期列为字符串类型，便于排序
    df['报告期'] = df['报告期'].astype(str)

    # 指标列表，添加“自有经营现金净额”
    cash_flow_indicators = ['经营活动现金流净额', '投资活动现金流净额', '融资活动现金流净额', '自有经营现金净额']

    # 如果指定了公司代码，按照代码筛选
    if company_codes:
        df_selected = df[df['股票代码'].isin(company_codes)]
    elif company_names:
        df_selected = df[df['股票简称'].isin(company_names)]
    else:
        print("请指定公司代码列表或公司名称列表。")
        return

    # 按照报告期排序
    df_selected.sort_values(by='报告期', inplace=True)

    for company in df_selected['股票简称'].unique():
        df_company = df_selected[df_selected['股票简称'] == company]

        # 创建以公司名称命名的文件夹
        company_dir = os.path.join('data', 'analysis', company)
        os.makedirs(company_dir, exist_ok=True)

        # 绘制现金流量指标的变化趋势
        plt.figure(figsize=(12, 6))

        for indicator in cash_flow_indicators:
            plt.plot(df_company['报告期'], df_company[indicator], marker='o', label=indicator)

        # 标记 y=0 的水平线
        plt.axhline(y=0, color='black', linestyle='--', linewidth=1)

        plt.title(f'{company} 现金流量指标变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('现金流量净额（单位：万元）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = os.path.join(company_dir, f'{company}_现金流量指标变化趋势.png')
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

def visualize_balance_sheet(input_file, company_codes=None, company_names=None):
    """
    对指定公司，绘制资产负债表财务指标的时间序列图。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))

    # 设置字体和处理负号显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 指定字体路径（请根据你的系统调整路径）
    font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 苹方字体路径
    font_prop = FontProperties(fname=font_path)

    # 确保日期列为字符串类型，便于排序
    df['报告期'] = df['报告期'].astype(str)

    # 指标列表
    amount_indicators = ['资产总额', '负债总额', '股东权益']
    ratio_indicators = ['资产负债率', '产权比率', '流动比率', '速动比率', '现金比率']

    # 如果指定了公司代码，按照代码筛选
    if company_codes:
        df_selected = df[df['股票代码'].isin(company_codes)]
    elif company_names:
        df_selected = df[df['股票简称'].isin(company_names)]
    else:
        print("请指定公司代码列表或公司名称列表。")
        return

    # 按照报告期排序
    df_selected.sort_values(by='报告期', inplace=True)

    for company in df_selected['股票简称'].unique():
        df_company = df_selected[df_selected['股票简称'] == company]

        # 创建以公司名称命名的文件夹
        company_dir = os.path.join('data', 'analysis', company)
        os.makedirs(company_dir, exist_ok=True)

        # 绘制金额指标的变化趋势
        plt.figure(figsize=(12, 6))
        for indicator in amount_indicators:
            plt.plot(df_company['报告期'], df_company[indicator], marker='o', label=indicator)
        plt.title(f'{company} 资产、负债、股东权益变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('金额（单位：万元）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = os.path.join(company_dir, f'{company}_资产负债权益变化趋势.png')
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

        # 绘制比率指标的变化趋势
        plt.figure(figsize=(12, 6))
        for indicator in ratio_indicators:
            plt.plot(df_company['报告期'], df_company[indicator], marker='o', label=indicator)
        plt.title(f'{company} 财务比率指标变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('比率（单位：小数）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = os.path.join(company_dir, f'{company}_资产负债表比率指标变化趋势.png')
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

if __name__ == "__main__":
    # 可视化利润表
    config = STATEMENT_CONFIG['income_statement']
    input_file = os.path.join('data', 'analysis', config['analysis_file'])
    visualize_income_statement(input_file, company_codes=COMPANY_CODES)

    # 可视化现金流量表
    config = STATEMENT_CONFIG['cash_flow_statement']
    input_file = os.path.join('data', 'analysis', config['analysis_file'])
    visualize_cash_flow_statement(input_file, company_codes=COMPANY_CODES)

    # 可视化资产负债表
    config = STATEMENT_CONFIG['balance_sheet']
    input_file = os.path.join('data', 'analysis', config['analysis_file'])
    visualize_balance_sheet(input_file, company_codes=COMPANY_CODES)