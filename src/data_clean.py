# src/data_clean.py

import sys
import os

# 添加项目根目录到 sys.path
sys.path.append('.')

from config import REPORT_DATES, STATEMENT_TYPES, STATEMENT_CONFIG
import pandas as pd

def clean_financial_statements(report_dates, statement_type):
    """
    清洗并整合指定报告期列表的财务报表数据。
    """
    config = STATEMENT_CONFIG[statement_type]
    file_prefix = config['file_prefix']
    output_file = os.path.join('data', 'clean', config['clean_file'])

    df_list = []
    for report_date in report_dates:
        input_file = os.path.join('data', 'raw', file_prefix, report_date, f'{file_prefix}_{report_date}.csv')
        if os.path.exists(input_file):
            df = pd.read_csv(input_file, dtype={'股票代码': str})
            if '代码' in df.columns:
                df.rename(columns={'代码': '股票代码', '名称': '股票简称'}, inplace=True)
            df['报告期'] = report_date  # 添加报告期列
            df_list.append(df)
        else:
            print(f"文件 {input_file} 不存在，跳过该报告期。")
    if not df_list:
        print(f"没有可用的 {statement_type} 数据进行清洗。")
        return
    combined_df = pd.concat(df_list, ignore_index=True)
    # 去除重复值
    combined_df.drop_duplicates(inplace=True)
    # 填充缺失值为0
    combined_df.fillna(0, inplace=True)
    # 数据类型转换
    if statement_type == 'income_statement':
        amount_columns = ['净利润', '净利润同比', '营业总收入', '营业总收入同比',
                          '营业总支出-营业支出', '营业总支出-销售费用', '营业总支出-管理费用',
                          '营业总支出-财务费用', '营业总支出-营业总支出', '营业利润', '利润总额',
                          '营业成本']
        # 检查是否存在 '营业成本' 列，如果没有，则需要从其他列计算或获取
        if '营业成本' not in combined_df.columns:
            # 假设 '营业总支出-营业支出' 为 '营业成本'
            combined_df.rename(columns={'营业总支出-营业支出': '营业成本'}, inplace=True)
    elif statement_type == 'cash_flow_statement':
        amount_columns = ['净现金流-净现金流', '净现金流-同比增长', '经营性现金流-现金流量净额',
                          '经营性现金流-净现金流占比', '投资性现金流-现金流量净额', '投资性现金流-净现金流占比',
                          '融资性现金流-现金流量净额', '融资性现金流-净现金流占比']
    elif statement_type == 'balance_sheet':
        amount_columns = ['资产-货币资金', '资产-应收账款', '资产-存货', '资产-总资产', '资产-总资产同比',
                          '负债-应付账款', '负债-总负债', '负债-预收账款', '负债-总负债同比', '资产负债率', '股东权益合计']
    elif statement_type == 'dividend':
        amount_columns = ['送转股份-送转总比例', '送转股份-送转比例', '送转股份-转股比例',
                          '现金分红-现金分红比例', '现金分红-股息率', '每股收益', '每股净资产',
                          '每股公积金', '每股未分配利润', '净利润同比增长', '总股本']
    else:
        amount_columns = []

    for col in amount_columns:
        if col in combined_df.columns:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        else:
            combined_df[col] = 0.0  # 如果列不存在，填充为0.0
    combined_df.to_csv(output_file, index=False)
    print(f"{statement_type} 数据清洗完成，保存至 {output_file}")

if __name__ == "__main__":
    for statement_type in STATEMENT_TYPES:
        clean_financial_statements(REPORT_DATES, statement_type)