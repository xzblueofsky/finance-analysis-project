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
    # 处理缺失值，例如，用0填充
    df.fillna(0, inplace=True)
    # 数据类型转换，例如，将金额列转换为浮点型
    amount_columns = ['净利润', '净利润同比', '营业总收入', '营业总收入同比', '营业总支出-营业支出',
                      '营业总支出-销售费用', '营业总支出-管理费用', '营业总支出-财务费用', '营业总支出-营业总支出',
                      '营业利润', '利润总额']
    for col in amount_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.to_csv(output_file, index=False)
    print("数据清洗完成，保存至 {}".format(output_file))

if __name__ == "__main__":
    report_date = '20230331'  # 替换为你的报告期
    input_file = 'data/raw/income_statements_{}.csv'.format(report_date)
    output_file = 'data/clean/income_statements_clean_{}.csv'.format(report_date)
    clean_income_statements(input_file, output_file)