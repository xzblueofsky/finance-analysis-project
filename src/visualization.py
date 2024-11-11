# src/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

def visualize_financial_indicators(input_file, report_date):
    """
    可视化财务指标，展示前10家公司。
    :param input_file: 分析结果的数据文件路径
    :param report_date: 报告日期，用于保存图表文件名
    """
    df = pd.read_csv(input_file)

    # 设置字体和处理负号显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 指定字体路径（请根据你的系统调整路径）
    font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 苹方字体路径
    font_prop = FontProperties(fname=font_path)

    # 定义指标和排序方式
    indicators = [
        {'name': '营业收入', 'ascending': False},       # 显示最高的10家公司
        {'name': '毛利率', 'ascending': False},         # 显示最高的10家公司
        {'name': '费用率', 'ascending': True},          # 显示最低的10家公司
        {'name': '营业利润率', 'ascending': False},     # 显示最高的10家公司
        {'name': '毛利润费用占比', 'ascending': True}    # 显示最低的10家公司
    ]

    for indicator_info in indicators:
        indicator = indicator_info['name']
        ascending = indicator_info['ascending']

        # 对指标进行排序，取前10家公司
        top10 = df.sort_values(by=indicator, ascending=ascending).head(10)

        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 8))

        ax = sns.barplot(x='股票简称', y=indicator, data=top10)

        # 设置标题和轴标签的字体
        if ascending:
            title_text = f'{indicator}最低的前10家公司'
        else:
            title_text = f'{indicator}最高的前10家公司'
        plt.title(title_text, fontproperties=font_prop)
        plt.xlabel('股票简称', fontproperties=font_prop)
        plt.ylabel(indicator, fontproperties=font_prop)

        # 设置 x 轴刻度标签的字体
        for label in ax.get_xticklabels():
            label.set_fontproperties(font_prop)

        plt.xticks(rotation=45)
        plt.tight_layout()
        output_image = f'data/analysis/top_10_{indicator}_{report_date}.png'
        plt.savefig(output_image)
        plt.show()
        print(f"可视化完成，图表保存至 {output_image}")

if __name__ == "__main__":
    report_date = '20231231'
    input_file = f'data/analysis/financial_indicators_{report_date}.csv'
    visualize_financial_indicators(input_file, report_date)