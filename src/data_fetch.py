# src/data_fetch.py

import akshare as ak
import pandas as pd
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from config import REPORT_DATES

def fetch_income_statements(report_dates):
    """
    获取指定报告期列表的所有上市公司利润表数据。
    :param report_dates: 报告日期列表，格式为 ['YYYYMMDD', ...]
    """
    for report_date in report_dates:
        income_statement_df = ak.stock_lrb_em(date=report_date)
        # 创建报告期文件夹
        output_dir = f'data/raw/{report_date}'
        os.makedirs(output_dir, exist_ok=True)
        output_file = f'{output_dir}/income_statements_{report_date}.csv'
        income_statement_df.to_csv(output_file, index=False)
        print(f"报告期 {report_date} 的数据获取完成，保存至 {output_file}")

if __name__ == "__main__":
    fetch_income_statements(REPORT_DATES)