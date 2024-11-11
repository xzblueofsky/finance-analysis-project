# src/data_clean.py

import pandas as pd

def clean_income_statements(input_file, output_file):
    """
    清洗利润表数据，处理缺失值和数据类型转换。
    :param input_file: 输入的原始数据文件路径
    :param output_file: 输出的清洗后数据文件路径
    """
    df = pd.read_csv(input_file)
    # 去除重复值
    df.drop_duplicates(inplace=True)
    # 填充缺失值为0
    df.fillna(0, inplace=True)
    # 数据类型转换
    amount_columns = ['净利润', '净利润同比', '营业总收入', '营业总收入同比',
                      '营业总支出-营业支出', '营业总支出-销售费用', '营业总支出-管理费用',
                      '营业总支出-财务费用', '营业总支出-营业总支出', '营业利润', '利润总额',
                      '营业成本']
    # 检查是否存在 '营业成本' 列，如果没有，则需要从其他列计算或获取
    if '营业成本' not in df.columns:
        # 假设 '营业总支出-营业支出' 为 '营业成本'
        df.rename(columns={'营业总支出-营业支出': '营业成本'}, inplace=True)
    for col in amount_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = 0.0  # 如果列不存在，填充为0.0
    df.to_csv(output_file, index=False)
    print(f"数据清洗完成，保存至 {output_file}")

if __name__ == "__main__":
    report_date = '20231231'
    input_file = f'data/raw/income_statements_{report_date}.csv'
    output_file = f'data/clean/income_statements_clean_{report_date}.csv'
    clean_income_statements(input_file, output_file)