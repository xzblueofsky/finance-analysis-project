# src/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

def visualize_top_companies(input_file):
    """
    可视化净利润率最高的前10家公司。
    :param input_file: 分析结果的数据文件路径
    """
    df = pd.read_csv(input_file)

    # 设置字体和处理负号显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 指定字体路径
    font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 苹方字体路径
    font_prop = FontProperties(fname=font_path)

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # 绘制柱状图
    ax = sns.barplot(x='股票简称', y='净利润率', data=df)

    # 设置标题和轴标签的字体
    plt.title('净利润率最高的前10家公司', fontproperties=font_prop)
    plt.xlabel('股票简称', fontproperties=font_prop)
    plt.ylabel('净利润率', fontproperties=font_prop)

    # 设置 x 轴刻度标签的字体
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)

    # 设置 y 轴刻度标签的字体（如果有中文）
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)

    plt.xticks(rotation=45)
    plt.tight_layout()
    output_image = 'data/analysis/top_10_profit_margin.png'
    plt.savefig(output_image)
    plt.show()
    print("可视化完成，图表保存至 {}".format(output_image))

if __name__ == "__main__":
    report_date = '20230331'  # 替换为你的报告期
    input_file = 'data/analysis/top_10_profit_margin_{}.csv'.format(report_date)
    visualize_top_companies(input_file)