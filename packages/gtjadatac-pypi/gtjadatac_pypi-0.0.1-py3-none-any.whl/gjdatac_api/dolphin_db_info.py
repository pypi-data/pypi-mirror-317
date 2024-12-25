# 此文件用于存放dolphinDB的相关信息，包括登录信息、数据库和表信息等。

""" 行情数据所在数据库和表 """

''' 期货 '''
# 历史期货行情数据 L1-tick数据
history_future_tick_db_path = "dfs://tick"  # 数据库路径
history_future_tick_db_table_name = "ctp_future_tick"  # 表名

# 历史期货行情数据 L2-tick数据
history_future_tick_l2_db_path = "dfs://tick_level2"  # 数据库路径
history_future_tick_l2_db_table_name = "t_future_tick"  # 表名

# 历史期货行情 L1-分钟k线
history_future_min_db_path = "dfs://minutek"  # 数据库路径
history_future_min_db_table_name = "ctp_future_mink"  # 表名

# 历史期货行情 L1-日k线
history_future_day_db_path = "dfs://dayk"  # 数据库路径
history_future_day_db_table_name = "ctp_future_dayk"  # 表名

# 历史期货实时分钟k线合成数据 1min_gtja
history_future_1min_gtja_db_path = "dfs://minutek"  # 数据库路径
history_future_1min_gtja_db_table_name = "t_trade_future_mink"  # 表名

''' 期权 '''
# 历史期权行情数据 tick数据
history_option_tick_db_path = "dfs://tick"  # 数据库路径
history_option_tick_db_table_name = "ctp_option_tick"  # 表名

# 历史期权行情数据 分钟k线
history_option_min_db_path = "dfs://minutek"  # 数据库路径
history_option_min_db_table_name = "ctp_option_mink"  # 表名

# 历史期权行情数据 5分钟k线
history_option_5min_db_path = "dfs://minutek"  # 数据库路径
history_option_5min_db_table_name = "ctp_future_mink5"  # 表名

# 历史期权行情数据 15分钟k线
history_option_15min_db_path = "dfs://minutek"  # 数据库路径
history_option_15min_db_table_name = "ctp_future_mink15"  # 表名

# 历史期权行情数据 日k线
history_option_day_db_path = "dfs://dayk"  # 数据库路径
history_option_day_db_table_name = "ctp_option_dayk"  # 表名

""" 基础信息 """

# 交易参数
trading_params_db_path = "dfs://basicinfo"  # 数据库路径
# trading_params_db_table_name = "b_calendar"  # 表名
trading_params_db_table_name = "t_nexttradeparam"  # 表名

# 期货-合约信息
future_contract_db_path = "dfs://basicinfo"  # 数据库路径
future_contract_db_table_name = "t_futinstrument"  # 表名

# 期权-合约信息
option_contract_db_path = "dfs://basicinfo"  # 数据库路径
option_contract_db_table_name = "t_optinstrument"  # 表名

# 交易日历
trading_dates_db_path = "dfs://basicinfo"  # 数据库路径
trading_dates_db_table_name = "b_calendar"  # 表名

# twap-分钟
twap_min_db_path = "dfs://minutek"  # 数据库路径
twap_min_db_table_name = "t_mink_metric"  # 表名

# twap-天
twap_day_db_path = "dfs://dayk"  # 数据库路径
twap_day_db_table_name = "t_day_metric"  # 表名

# vwap-分钟
vwap_min_db_path = "dfs://minutek"  # 数据库路径
vwap_min_db_table_name = "t_mink_metric"  # 表名

# vwap-天
vwap_day_db_path = "dfs://dayk"  # 数据库路径
vwap_day_db_table_name = "t_day_metric"  # 表名