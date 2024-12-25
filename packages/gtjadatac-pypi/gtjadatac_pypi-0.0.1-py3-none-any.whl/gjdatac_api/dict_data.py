# 此文件中用于存放各种接口的字典数据


""" get_price(行情数据) 相关数据字典 """
# 频率字典--用于存放不同品种不同周期的K线类型
get_price_frequency_dict = {
    "future": {
        "d": "bar",
        "min": "bar",
        "min_gtja": "bar",
        "tick_l1": "tick",
        "tick_l2": "tick"
    },
    "option": {
        "d": "bar",
        "min": "bar",
        "tick": "tick"
    }
}

# 不同类型的数据需要返回的字段
get_price_data_type_dict = {
    "bar": {'trading_day': 'trading_day', 'trade_time': 'datetime', 'exchange_id': 'exchange_id',
            'instrument_id': 'order_book_ids', 'open_price': 'open', 'highest_price': 'high',
            'lowest_price': 'low', 'close_price': 'close', 'settlement_price': 'settlement',
            'upper_limit_price': 'limit_up', 'lower_limit_price': 'limit_down',
            'pre_settlement_price': 'prev_settlement',
            'volume': 'volume', 'turnover': 'total_turnover', 'open_interest': 'open_interest'},
    "tick": {'trading_day': 'trading_day', 'trade_time': 'datetime', 'exchange_id': 'exchange_id',
             'instrument_id': 'order_book_ids', 'last_price': 'last', 'open_price': 'open',
             'highest_price': 'high', 'lowest_price': 'low', 'close_price': 'close',
             'settlement_price': 'settlement', 'upper_limit_price': 'limit_up',
             'lower_limit_price': 'limit_down', 'pre_settlement_price': 'prev_settlement',
             'pre_close_price': 'prev_close', 'volume': 'volume', 'turnover': 'total_turnover',
             'open_interest': 'open_interest', 'ask_price1': 'a1', 'ask_price2': 'a2', 'ask_price3': 'a3',
             'ask_price4': 'a4', 'ask_price5': 'a5', 'ask_volume1': 'a1_v', 'ask_volume2': 'a2_v',
             'ask_volume3': 'a3_v', 'ask_volume4': 'a4_v', 'ask_volume5': 'a5_v', 'bid_price1': 'b1',
             'bid_price2': 'b2', 'bid_price3': 'b3', 'bid_price4': 'b4', 'bid_price5': 'b5',
             'bid_volume1': 'b1_v', 'bid_volume2': 'b2_v', 'bid_volume3': 'b3_v', 'bid_volume4': 'b4_v',
             'bid_volume5': 'b5_v'}
}

""" get_instruments(合约基础信息) 相关数据字典 """
# 不同合约类型对应的字段
get_instruments_type_dict = {
    "future": {
        "instrumentid": "order_book_id", "exchangeid": "exchange", 
        # "commodity": "commodity",
        "opendate": "listed_date", "expiredate": "maturity_date", "startdelivdate": "start_delivery_date",
        "enddelivdate": "end_delivery_date", "delistingdate": "de_listed_date",
        "volumemultiple": "contract_multiplier", "targetinstrid": "underlying_order_book_id",
        # "targetinstrid": "underlying_order_book_id", "volumemultiple": "contract_multiplier"
        # "trading_hour": "trading_hour"
    },

    "option": {
        "instrumentid": "order_book_id", "exchangeid": "exchange", 
        # "": "commodity",
        "opendate": "listed_date", "expiredate": "maturity_date", "deliverymonth": "delivery_month",
        "startdelivdate": "start_delivery", "enddelivdate": "end_delivery", "delistingdate": "de_listed_date",
        "optionstype": "option_type", "strikeprice": "strike_price", "targetinstrid": "underlying_order_book_id",
        "volumemultiple": "contract_multiplier", 
        # "trading_hour": "trading_hour"
    },
    
    "future_return_fields": [
        "order_book_id", "commodity", "listed_date", "de_listed_date", "type", "contract_multiplier", "underlying_order_book_id",
        "maturity_date", "exchange", "start_delivery_date", "end_delivery_date", "trading_hour"
    ],
    
    "option_return_fields": [
        "order_book_id", "commodity", "listed_date", "de_listed_date", "type", "contract_multiplier", "underlying_order_book_id",
        "maturity_date", "exchange", "strike_price", "option_type", "exercise_type", "delivery_month", "start_delivery", "end_delivery",
        "trading_hour"
    ]
}
