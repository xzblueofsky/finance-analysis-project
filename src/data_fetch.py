# src/data_fetch.py

import akshare as ak
import pandas as pd

def fetch_all_income_statements(report_date):
    """
    获取指定报告期的所有上市公司利润表数据。
    :param report_date: 报告日期，格式为 'YYYYMMDD'，例如 '20230331'
    :return: 利润表数据的 DataFrame
    """
    income_statement_df = ak.stock_lrb_em(date=report_date)
    return income_statement_df

if __name__ == "__main__":
    report_date = '20230331'  # 替换为你需要的报告期
    df = fetch_all_income_statements(report_date)
    df.to_csv('data/raw/income_statements_{}.csv'.format(report_date), index=False)
    print("数据获取完成，保存至 ../data/raw/income_statements_{}.csv".format(report_date))