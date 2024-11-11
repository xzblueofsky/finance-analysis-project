# src/data_clean.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from config import REPORT_DATES
import pandas as pd
import os

def clean_income_statements(report_dates, output_file):
    """
    清洗并整合指定报告期列表的利润表数据。
    :param report_dates: 报告日期列表
    :param output_file: 输出的清洗后数据文件路径
    """
    df_list = []
    for report_date in report_dates:
        input_file = f'data/raw/{report_date}/income_statements_{report_date}.csv'
        if os.path.exists(input_file):
            # 指定股票代码列的数据类型为字符串
            df = pd.read_csv(input_file, dtype={'股票代码': str})
            df['报告期'] = report_date  # 添加报告期列
            df_list.append(df)
        else:
            print(f"文件 {input_file} 不存在，跳过该报告期。")
    if not df_list:
        print("没有可用的数据进行清洗。")
        return
    combined_df = pd.concat(df_list, ignore_index=True)
    # 去除重复值
    combined_df.drop_duplicates(inplace=True)
    # 填充缺失值为0
    combined_df.fillna(0, inplace=True)
    # 数据类型转换
    amount_columns = ['净利润', '净利润同比', '营业总收入', '营业总收入同比',
                      '营业总支出-营业支出', '营业总支出-销售费用', '营业总支出-管理费用',
                      '营业总支出-财务费用', '营业总支出-营业总支出', '营业利润', '利润总额',
                      '营业成本']
    # 检查是否存在 '营业成本' 列，如果没有，则需要从其他列计算或获取
    if '营业成本' not in combined_df.columns:
        # 假设 '营业总支出-营业支出' 为 '营业成本'
        combined_df.rename(columns={'营业总支出-营业支出': '营业成本'}, inplace=True)
    for col in amount_columns:
        if col in combined_df.columns:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        else:
            combined_df[col] = 0.0  # 如果列不存在，填充为0.0
    combined_df.to_csv(output_file, index=False)
    print(f"数据清洗完成，保存至 {output_file}")

if __name__ == "__main__":
    output_file = 'data/clean/income_statements_clean.csv'
    clean_income_statements(REPORT_DATES, output_file)