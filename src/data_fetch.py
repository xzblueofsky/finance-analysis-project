# src/data_fetch.py

import sys
import os

# 添加项目根目录到 sys.path
sys.path.append('.')

from config import REPORT_DATES, STATEMENT_TYPES, STATEMENT_CONFIG
import akshare as ak
import pandas as pd

def fetch_financial_statements(report_dates, statement_type):
    """
    获取指定报告期列表的财务报表数据。
    """
    config = STATEMENT_CONFIG[statement_type]
    fetch_function_name = config['fetch_function']
    file_prefix = config['file_prefix']

    # 动态获取 AkShare 函数
    fetch_function = getattr(ak, fetch_function_name)

    for report_date in report_dates:
        # 对于分红数据，需要特殊处理，因为日期格式可能不同
        if statement_type == 'dividend':
            # 分红数据的日期格式为 'YYYY1231' 或 'YYYY0630'
            # 我们只获取每年的年末数据
            if report_date.endswith('1231'):
                date = report_date
            else:
                continue  # 跳过非年末的数据
            df = fetch_function(date=date)
        else:
            df = fetch_function(date=report_date)
        # 将股票代码转换为字符串，并填充前导零至6位
        df['股票代码'] = df['股票代码'].apply(lambda x: str(x).zfill(6)) if '股票代码' in df.columns else df['代码'].apply(lambda x: str(x).zfill(6))
        # 创建报告期文件夹
        output_dir = os.path.join('data', 'raw', file_prefix, report_date)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{file_prefix}_{report_date}.csv')
        df.to_csv(output_file, index=False)
        print(f"{statement_type} 报告期 {report_date} 的数据获取完成，保存至 {output_file}")

if __name__ == "__main__":
    for statement_type in STATEMENT_TYPES:
        fetch_financial_statements(REPORT_DATES, statement_type)