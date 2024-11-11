# src/visualization.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
from config import COMPANY_CODES, COMPANY_NAMES

def visualize_company_indicators(input_file, company_codes=None, company_names=None):
    """
    对指定公司，绘制财务指标的时间序列图。
    :param input_file: 分析结果的数据文件路径
    :param company_codes: 公司股票代码列表
    :param company_names: 公司股票简称列表
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
        
        # 绘制营业收入的变化趋势
        plt.figure(figsize=(12, 6))
        plt.plot(df_company['报告期'], df_company['营业收入'], marker='o', label='营业收入')
        plt.title(f'{company} 营业收入变化趋势', fontproperties=font_prop)
        plt.xlabel('报告期', fontproperties=font_prop)
        plt.ylabel('营业收入（单位：万元）', fontproperties=font_prop)
        plt.xticks(rotation=45)
        plt.legend(prop=font_prop)
        plt.tight_layout()
        output_image = f'data/analysis/{company}_营业收入变化趋势.png'
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
        output_image = f'data/analysis/{company}_财务比率指标变化趋势.png'
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

        # 可选：分别绘制每个比值指标的变化趋势
        for indicator in ratio_indicators:
            plt.figure(figsize=(12, 6))
            plt.plot(df_company['报告期'], df_company[indicator], marker='o', label=indicator)
            plt.title(f'{company} {indicator} 变化趋势', fontproperties=font_prop)
            plt.xlabel('报告期', fontproperties=font_prop)
            plt.ylabel(indicator, fontproperties=font_prop)
            plt.xticks(rotation=45)
            plt.legend(prop=font_prop)
            plt.tight_layout()
            output_image = f'data/analysis/{company}_{indicator}_变化趋势.png'
            plt.savefig(output_image)
            plt.show()
            print(f"可视化完成，图表保存至 {output_image}")

if __name__ == "__main__":
    input_file = 'data/analysis/financial_indicators.csv'
    visualize_company_indicators(input_file, company_codes=COMPANY_CODES)