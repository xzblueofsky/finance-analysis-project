# src/analysis.py

import sys
import os

# 添加项目根目录到 sys.path
sys.path.append('.')

import pandas as pd
import numpy as np
from config import STATEMENT_CONFIG

def analyze_income_statement(input_file, output_file):
    """
    计算利润表的财务指标，并输出结果。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))

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
    result_df = df[['股票代码', '股票简称', '报告期', '营业收入', '毛利率', '费用率', '营业利润率', '毛利润费用占比']]

    result_df.to_csv(output_file, index=False)
    print(f"利润表数据分析完成，保存至 {output_file}")

def analyze_cash_flow_statement(input_file, output_file):
    """
    计算现金流量表的指标，并输出结果。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))
    print(df.columns)

    # 计算需要的指标
    df['经营活动现金流净额'] = df['经营性现金流-现金流量净额']
    df['投资活动现金流净额'] = df['投资性现金流-现金流量净额']
    df['融资活动现金流净额'] = df['融资性现金流-现金流量净额']

    # 计算自有经营现金净额
    df['自有经营现金净额'] = df['经营活动现金流净额'] + df['投资活动现金流净额'] + df['融资活动现金流净额']

    # 将单位转换为万元（可选）
    df['经营活动现金流净额'] = df['经营活动现金流净额'] / 1e4
    df['投资活动现金流净额'] = df['投资活动现金流净额'] / 1e4
    df['融资活动现金流净额'] = df['融资活动现金流净额'] / 1e4
    df['自有经营现金净额'] = df['自有经营现金净额'] / 1e4

    # 选择需要的列
    result_df = df[['股票代码', '股票简称', '报告期', '经营活动现金流净额', '投资活动现金流净额', '融资活动现金流净额', '自有经营现金净额']]

    result_df.to_csv(output_file, index=False)
    print(f"现金流量表数据分析完成，保存至 {output_file}")

def analyze_balance_sheet(input_file, output_file):
    """
    计算资产负债表的财务指标，并输出结果。
    """
    df = pd.read_csv(input_file, dtype={'股票代码': str})

    # 确保股票代码长度为6位，填充前导零
    df['股票代码'] = df['股票代码'].apply(lambda x: x.zfill(6))

    # 计算财务指标
    df['资产总额'] = df['资产-总资产'] / 1e4  # 转换为万元
    df['负债总额'] = df['负债-总负债'] / 1e4  # 转换为万元
    df['股东权益'] = df['股东权益合计'] / 1e4  # 转换为万元

    # 资产负债率已存在，转换为小数
    df['资产负债率'] = df['资产负债率'] / 100

    # 计算产权比率 = 总负债 / 股东权益
    df['产权比率'] = df['负债总额'] / df['股东权益']

    # 计算流动比率 = （货币资金 + 应收账款 + 存货）/ （应付账款 + 预收账款）
    df['流动资产合计'] = df['资产-货币资金'] + df['资产-应收账款'] + df['资产-存货']
    df['流动负债合计'] = df['负债-应付账款'] + df['负债-预收账款']
    df['流动比率'] = df['流动资产合计'] / df['流动负债合计']

    # 计算速动比率 = （货币资金 + 应收账款）/ （应付账款 + 预收账款）
    df['速动资产合计'] = df['资产-货币资金'] + df['资产-应收账款']
    df['速动比率'] = df['速动资产合计'] / df['流动负债合计']

    # 计算现金比率 = 货币资金 / （应付账款 + 预收账款）
    df['现金比率'] = df['资产-货币资金'] / df['流动负债合计']

    # 选择需要的列
    result_df = df[['股票代码', '股票简称', '报告期', '资产总额', '负债总额', '股东权益',
                    '资产负债率', '产权比率', '流动比率', '速动比率', '现金比率']]

    # 处理无限值和缺失值
    result_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    result_df.fillna(0, inplace=True)

    result_df.to_csv(output_file, index=False)
    print(f"资产负债表数据分析完成，保存至 {output_file}")


if __name__ == "__main__":
    # 分析利润表（保持原有代码）
    config = STATEMENT_CONFIG['income_statement']
    input_file = os.path.join('data', 'clean', config['clean_file'])
    output_file = os.path.join('data', 'analysis', config['analysis_file'])
    analyze_income_statement(input_file, output_file)

    # 分析现金流量表
    config = STATEMENT_CONFIG['cash_flow_statement']
    input_file = os.path.join('data', 'clean', config['clean_file'])
    output_file = os.path.join('data', 'analysis', config['analysis_file'])
    analyze_cash_flow_statement(input_file, output_file)

    # 分析资产负债表
    config = STATEMENT_CONFIG['balance_sheet']
    input_file = os.path.join('data', 'clean', config['clean_file'])
    output_file = os.path.join('data', 'analysis', config['analysis_file'])
    analyze_balance_sheet(input_file, output_file)