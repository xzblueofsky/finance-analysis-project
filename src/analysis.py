# src/analysis.py

import pandas as pd

def analyze_income_statements(input_file, output_file):
    """
    分析利润表数据，计算财务指标并进行排序、筛选等。
    :param input_file: 清洗后的数据文件路径
    :param output_file: 分析结果文件路径
    """
    df = pd.read_csv(input_file)
    # 计算净利润率 = 净利润 / 营业总收入
    df['净利润率'] = df['净利润'] / df['营业总收入']
    # 筛选净利润率最高的前10家公司
    top_10_profit_margin = df.sort_values(by='净利润率', ascending=False).head(10)
    top_10_profit_margin.to_csv(output_file, index=False)
    print("数据分析完成，保存至 {}".format(output_file))
    return top_10_profit_margin

if __name__ == "__main__":
    report_date = '20230331'  # 替换为你的报告期
    input_file = 'data/clean/income_statements_clean_{}.csv'.format(report_date)
    output_file = 'data/analysis/top_10_profit_margin_{}.csv'.format(report_date)
    analyze_income_statements(input_file, output_file)