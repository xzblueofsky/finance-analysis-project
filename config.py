# config.py

# 时间范围，列表格式，包含需要分析的报告期
REPORT_DATES = [
    '20101231',
    '20111231',
    '20121231',
    '20131231',
    '20141231',
    '20151231',
    '20161231',
    '20171231',
    '20181231',
    '20191231',
    '20201231',
    '20211231',
    '20221231',
    '20231231'
]

# 指定的公司列表，股票代码列表
COMPANY_CODES = ['600519', '000858', '601318']  # 示例公司

# 财务报表类型列表
STATEMENT_TYPES = ['income_statement', 'cash_flow_statement', 'balance_sheet', 'dividend']

# 财务报表配置映射，用于在不同模块中使用
STATEMENT_CONFIG = {
    'income_statement': {
        'fetch_function': 'stock_lrb_em',
        'file_prefix': 'income_statement',
        'clean_file': 'income_statement_clean.csv',
        'analysis_file': 'income_statement_analysis.csv',
        'analysis_function': 'analyze_income_statement',
        'visualization_function': 'visualize_income_statement',
    },
    'cash_flow_statement': {
        'fetch_function': 'stock_xjll_em',
        'file_prefix': 'cash_flow_statement',
        'clean_file': 'cash_flow_statement_clean.csv',
        'analysis_file': 'cash_flow_statement_analysis.csv',
        'analysis_function': 'analyze_cash_flow_statement',
        'visualization_function': 'visualize_cash_flow_statement',
    },
    'balance_sheet': {
        'fetch_function': 'stock_zcfz_em',
        'file_prefix': 'balance_sheet',
        'clean_file': 'balance_sheet_clean.csv',
        'analysis_file': 'balance_sheet_analysis.csv',
        'analysis_function': 'analyze_balance_sheet',
        'visualization_function': 'visualize_balance_sheet',
    },
    'dividend': {
        'fetch_function': 'stock_fhps_em',
        'file_prefix': 'dividend',
        'clean_file': 'dividend_clean.csv',
        'analysis_file': 'dividend_analysis.csv',
        'analysis_function': 'analyze_dividend',
        'visualization_function': 'visualize_dividend',
    },
}