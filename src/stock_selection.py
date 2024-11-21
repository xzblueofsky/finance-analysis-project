# src/stock_selection.py

import sys
import os

# 添加项目根目录到 sys.path
sys.path.append('.')

import pandas as pd
import numpy as np
from config import REPORT_DATES

def select_stocks():
    # 读取分析后的数据文件
    income_df = pd.read_csv('data/analysis/income_statement_analysis.csv', dtype={'股票代码': str})
    balance_df = pd.read_csv('data/analysis/balance_sheet_analysis.csv', dtype={'股票代码': str})
    dividend_df = pd.read_csv('data/analysis/dividend_analysis.csv', dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    income_df['股票代码'] = income_df['股票代码'].apply(lambda x: x.zfill(6))
    balance_df['股票代码'] = balance_df['股票代码'].apply(lambda x: x.zfill(6))
    dividend_df['股票代码'] = dividend_df['股票代码'].apply(lambda x: x.zfill(6))

    # 合并数据
    merged_df = pd.merge(income_df, balance_df, on=['股票代码', '股票简称', '报告期'], how='inner')
    merged_df = pd.merge(merged_df, dividend_df, on=['股票代码', '股票简称', '报告期'], how='inner')

    # 按照报告期排序
    merged_df.sort_values(by=['股票代码', '报告期'], inplace=True)

    # 将报告期转换为日期类型
    merged_df['报告期日期'] = pd.to_datetime(merged_df['报告期'], format='%Y%m%d')

    # 选择最近5个报告期的数据
    latest_report_dates = sorted(merged_df['报告期日期'].unique())[-5:]
    df_recent = merged_df[merged_df['报告期日期'].isin(latest_report_dates)]

    # 定义筛选标准
    def apply_criteria(df):
        criteria = pd.DataFrame()

        # 营业收入排名前30%
        revenue_threshold = df['营业收入'].quantile(0.7)
        criteria['营业收入'] = df['营业收入'] >= revenue_threshold

        # 总资产排名前30%
        asset_threshold = df['资产总额'].quantile(0.7)
        criteria['总资产'] = df['资产总额'] >= asset_threshold

        # 股息率 ≥ 3%
        criteria['股息率'] = df['股息率'] >= 0.03

        # 股利支付率 ≥ 30%
        criteria['股利支付率'] = df['股利支付率'] >= 0.3

        # 总体标准
        criteria['总计满足条件数'] = criteria.sum(axis=1)
        criteria['是否满足所有条件'] = criteria.drop(columns=['总计满足条件数']).all(axis=1)

        return criteria

    # 对每个报告期的数据应用筛选标准
    df_recent = df_recent.reset_index(drop=True)
    criteria_df = apply_criteria(df_recent)

    # 将筛选结果与原始数据合并
    df_recent = pd.concat([df_recent, criteria_df], axis=1)

    # 统计每个公司满足条件的次数
    group = df_recent.groupby('股票代码')

    def count_satisfy(group):
        count = group['是否满足所有条件'].sum()
        return pd.Series({'满足条件次数': count})

    satisfy_count = df_recent.groupby('股票代码').apply(count_satisfy).reset_index()

    # 选择满足条件次数 ≥ 4 的公司
    selected_stocks = satisfy_count[satisfy_count['满足条件次数'] >= 4]['股票代码']

    # 获取选中公司的信息
    selected_df = df_recent[df_recent['股票代码'].isin(selected_stocks)]
    selected_df = selected_df[['股票代码', '股票简称']].drop_duplicates()

    # 输出选中的股票
    print("选中的股票列表：")
    print(selected_df)

    # 保存结果
    output_file = 'data/analysis/selected_stocks.csv'
    selected_df.to_csv(output_file, index=False)
    print(f"筛选结果已保存至 {output_file}")

if __name__ == "__main__":
    select_stocks()