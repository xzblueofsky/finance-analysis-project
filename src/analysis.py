# src/analysis.py

import pandas as pd
import numpy as np

def analyze_financial_indicators(input_file, output_file):
    """
    计算指定的财务指标，并对所有公司进行排序。
    :param input_file: 清洗后的数据文件路径
    :param output_file: 分析结果文件路径
    """
    df = pd.read_csv(input_file)

    # 计算财务指标
    df['营业收入'] = df['营业总收入']

    # 确保分母不为零，避免除零错误
    df['营业收入'].replace(0, np.nan, inplace=True)
    df['营业成本'].replace(0, np.nan, inplace=True)
    df['营业收入减营业成本'] = df['营业收入'] - df['营业成本']
    df['营业收入减营业成本'].replace(0, np.nan, inplace=True)

    # 毛利率 = （营业收入 - 营业成本） / 营业收入
    df['毛利率'] = (df['营业收入'] - df['营业成本']) / df['营业收入']

    # 对财务费用进行条件处理
    # 如果财务费用小于0，则设置为0（即不计入总费用）
    df['财务费用调整'] = df['营业总支出-财务费用'].apply(lambda x: x if x > 0 else 0)

    # 费用总额 = 销售费用 + 管理费用 + 财务费用调整
    df['费用总额'] = df['营业总支出-销售费用'] + df['营业总支出-管理费用'] + df['财务费用调整']

    # 费用率 = 费用总额 / 营业收入
    df['费用率'] = df['费用总额'] / df['营业收入']

    # 营业利润率 = 利润总额 / 营业收入
    df['营业利润率'] = df['利润总额'] / df['营业收入']

    # 毛利润费用占比 = 费用总额 / （营业收入 - 营业成本）
    df['毛利润费用占比'] = df['费用总额'] / (df['营业收入'] - df['营业成本'])

    # 恢复被替换为 NaN 的值
    df.fillna(0, inplace=True)

    # 选择需要的列
    result_df = df[['股票代码', '股票简称', '营业收入', '毛利率', '费用率', '营业利润率', '毛利润费用占比']]

    result_df.to_csv(output_file, index=False)
    print(f"数据分析完成，保存至 {output_file}")
    return result_df

if __name__ == "__main__":
    report_date = '20231231'
    input_file = f'data/clean/income_statements_clean_{report_date}.csv'
    output_file = f'data/analysis/financial_indicators_{report_date}.csv'
    analyze_financial_indicators(input_file, output_file)