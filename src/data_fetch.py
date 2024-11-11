# src/data_fetch.py

import akshare as ak
import pandas as pd

def fetch_income_statements(report_date):
    """
    获取指定报告期的所有上市公司利润表数据。
    :param report_date: 报告日期，格式为 'YYYY1231'，例如 '20231231'
    :return: 利润表数据的 DataFrame
    """
    income_statement_df = ak.stock_lrb_em(date=report_date)
    return income_statement_df

if __name__ == "__main__":
    report_date = '20231231'  # 2023年12月31日
    df = fetch_income_statements(report_date)
    output_file = f'data/raw/income_statements_{report_date}.csv'
    df.to_csv(output_file, index=False)
    print(f"数据获取完成，保存至 {output_file}")