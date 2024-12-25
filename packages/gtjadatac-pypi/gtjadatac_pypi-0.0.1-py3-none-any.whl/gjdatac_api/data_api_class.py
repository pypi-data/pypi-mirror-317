# 此文件用于编写数据接口---类方式实现

import datetime
import asyncio

import holidays
import pandas as pd
import dolphindb as ddb

from .dict_data import get_price_frequency_dict, get_price_data_type_dict, get_instruments_type_dict
from .dolphin_db_info import *


class GJDataC:
    # 初始化类
    def __init__(self, host, port, user_id, password):
        """
        用于定义一些不同接口所需的变量以及一些初始化操作
        :param host: 数据库地址
        :param port: 数据库端口
        :param user_id: 数据库用户名
        :param password: 数据库密码

        用户调用api时，需要提供dolphindb相关的用户信息，包括host、port、user_id、password，用于连接数据库
        """

        ''' 初始化校验 '''
        # 数据库参数
        self.host = host
        self.port = port
        self.user_id = user_id
        self.password = password

    def connect_db(self, table_name, db_path):
        """
        此方法用于根据不同的数据表及数据库获取数据，只返回Table对象，对应的数据处理在对应的数据接口处理
        :param table_name: 数据表路径
        :param db_path: 数据库路径
        :return 根据数据库和表路径获取的数据(Table对象), 会话信息(db_session)
        """

        # 连接数据库
        db_session = ddb.session()
        success = db_session.connect(self.host, self.port, self.user_id, self.password)
        if not success:
            raise Exception("please check your database connection information")

        # 从数据库中获取数据
        data = db_session.loadTable(tableName=table_name, dbPath=db_path)

        return data, db_session

    """ 通用方法 """

    @staticmethod
    def general_validate_params_required(param, param_name):
        """
        校验参数是否必填
        :param param: 参数值
        :param param_name: 参数名称
        :return: None （用于校验数据无需返回值）
        """
        if not param:
            raise ValueError(f"{param_name} is required")

    @staticmethod
    def general_validate_either_or(field_1_name, field_1_value, field_2_name, field_2_value):
        """
        此方法用于验证二选一的参数填写情况
        :param field_1_name: 参数1名称
        :param field_1_value: 参数1值
        :param field_2_name: 参数2名称
        :param field_2_value: 参数2值
        :return: None （用于校验数据无需返回值）
        """
        if not field_1_value and not field_2_value:
            raise ValueError(f"{field_1_name} or {field_2_name} is required")
        if field_1_value and field_2_value:
            raise ValueError(f"{field_1_name} and {field_2_name} cannot be both provided")

    def general_validate_date(self, date_str):
        """
        判断字符串是否为datetime.date, datetime.datetime格式。
        :param date_str: 待判断的字符串。

        Returns:
            True: 如果是日期格式，返回 True。
            False: 否则返回 False。
        """
        if not self.general_validate_date_str_is_datetime_type(date_str):
            return self.general_validate_date_str_is_date_type(date_str)
        return True

    @staticmethod
    def general_validate_date_str_is_datetime_type(date_data):
        """
        此方法用于验证日期字段是否为可以转换为datetime的类型
        :param date_data: 日期字符串

        :return : 如果可以转换为datetime类型，返回 True, 否则返回 False。
        """

        try:
            datetime.datetime.strptime(date_data, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def general_validate_date_str_is_date_type(date_data):
        """
        此方法用于验证日期字段是否为可以转换为date的类型
        :param date_data: 日期字符串

        :return : 如果可以转换为date类型，返回 True, 否则返回 False。
        """

        try:
            datetime.datetime.strptime(date_data, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def general_validate_field_str_or_list(field_value, field_name):
        """
        对参数的类型进行校验，判断是否为字符串或字符串列表。
        :param field_value: 待校验的参数值。
        :param field_name: 待校验的参数名称。
        :return: None （用于校验数据无需返回值）
        """

        if field_value and not isinstance(field_value, (str, list)):
            raise ValueError(f"{field_name} should be a string or a list of strings")

    @staticmethod
    def general_validate_param_is_str(param_name, param_value):
        """
        校验参数是否为str类型
        :param param_name: 参数名称
        :param param_value: 参数值
        :return: None （用于校验数据无需返回值）
        """

        if not isinstance(param_value, str):
            raise ValueError(f"{param_name} type error, please input str type")

    def general_validate_asset_type(self, asset_type):
        """
        对asset_type进行校验
        :param asset_type: str, 合约类型

        :return: None （用于校验数据无需返回值）
        """
        self.general_validate_params_required(asset_type, "asset_type")  # 校验必填参数
        if not isinstance(asset_type, str):
            raise ValueError("asset_type should be a string")
        if asset_type not in ["future", "option"]:
            raise ValueError("asset_type should be 'future' or 'option'")

    def general_validate_fields(self, data, fields):
        """
        根据用户选择的字段进行字段筛选
        :param fields: 字段列表--用户传入的需要返回的字段
        :param data: 数据
        :return data: 根据用户填写的字段筛选后的数据
        """

        ''' 校验fields '''
        # 如果没有传入fields, 则返回所有字段
        if not fields:
            return data
        self.general_validate_field_str_or_list(fields, "fields")

        ''' 根据fields进行处理 '''
        # 如果传入了fields，则根据传入的fields进行处理
        columns_list = data.columns.tolist()

        if isinstance(fields, str):
            self._deal_fields(fields, columns_list)
            data = data[[fields]]
        elif isinstance(fields, list):
            for field in fields:
                self._deal_fields(field, columns_list)
            data = data[fields]

        return data

    @staticmethod
    def _deal_fields(_field, columns_list):
        """
        判断用户选择的字段是否存在
        :param columns_list: 数据的所有字段
        :return: None （用于校验数据无需返回值）
        """
        if _field not in columns_list:
            raise ValueError(
                f"fields: got invalided value '{_field}', choose any in "
                f"{columns_list}")

    @staticmethod
    def general_filter_data_by_field(data, field_name, field_value):
        """
        根据指定的字段进行数据过滤
        :param data: pandas.DataFrame, 数据
        :param field_name: str, 过滤字段
        :param field_value: str or list, 过滤值

        :return 根据字段过滤后的数据
        """

        return data[data[field_name].isin(field_value)] if isinstance(
            field_value, list) else data[data[field_name] == field_value]

    def _general_filter_data_by_field(self, data, field_name, field_value):
        """
        根据自定字段进行类型校验以及数据筛选
        :param data: 需要处理的数据
        :param field_name: 字段名
        :param field_value: 字段值

        :return : 根据字段过滤后的数据
        """
        self.general_validate_field_str_or_list(field_value, field_name)
        return self.general_filter_data_by_field(data, field_name, field_value)

    def general_date_str_to_date(self, date_str):
        """
        将date类型的str转换成datetime.date类型
        :param date_str: str, 日期字符串
        """
        if not self.general_validate_date_str_is_date_type(date_str):
            raise ValueError("date_str is not a valid date string, please use the format 'YYYY-MM-DD")

        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    @staticmethod
    def general_date_str_to_datetime(date_str):
        """ 将date类型的str转换成datetime.datetime类型 """
        if isinstance(date_str, str):
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    """ get_price(获取行情数据接口) """

    def get_price(self, order_book_ids=None, asset_type="future", frequency=None, start_date=None, end_date=None,
                  fields=None, is_batch=False, batch_size=1000000):
        """
        行情数据接口
        :param order_book_ids: 合约代码--必填
        :param asset_type: 合约类型--必填, 默认为--'future'
        :param frequency: 频率--必填
        :param start_date: 开始日期--选填
        :param end_date: 结束日期--选填
        :param fields: 字段列表--选填
        :param is_batch: 是否分批获取--选填, 默认为--True
        :param batch_size: 每次分批获取的条数--选填, 默认为--1000000
        :return: 行情数据
        """

        # # 从数据库获取的数据是Table类型，需要转换为DataFrame类型, 并按照时间进行排序
        # self.get_price_data = self.get_price_data.sort_values(by='datetime', ascending=True)

        ''' 数据校验 (先对必填参数进行校验)'''
        # 对order_book_ids进行校验
        self.get_price_validate_order_book_ids(order_book_ids)

        # 对asset_type进行校验
        self.general_validate_asset_type(asset_type)

        # 对frequency进行校验
        self.get_price_validate_frequency(frequency)

        # 对 start_date 和 end_date 进行校验
        self.get_price_validate_start_end_date(start_date, end_date)

        ''' 参数校验完成后，开始根据参数从服务器获取数据 '''
        # 此处获取数据时已经根据order_book_ids筛选过一次数据了，所以后续不需要再对该字段进行筛选
        # data = self.get_price_data_get_data(order_book_ids, asset_type, frequency, start_date, end_date)
        # 从dolphindb获取所有满足条件的数据

        ''' 参数校验完成后再根据参数从dolphindb获取数据 '''
        # 获取数据库地址和表名
        db_table_name = self.get_price_get_db_table_name(asset_type, frequency)

        # 从dolphindb获取所有满足条件的数据
        total_data, db_session = self.get_price_data_get_data(order_book_ids, db_table_name, start_date, end_date)
        print("开始处理数据\n")
        print("总数据量: ", total_data.rows)

        if is_batch:  # 如果需要分批次处理数据
            for i in range(0, total_data.rows, batch_size):
                # 分批次从dolphindb获取数据，转换成dataframe（因为数据量过大时，同时将tables对象转换成dataframe比较耗时）
                data = total_data.limit([i, batch_size]).toDF()

                # 数据处理
                data = self.get_price_by_type_frequency(asset_type, frequency, data)
                data = self.get_price_filter_by_date(start_date, end_date, order_book_ids, data)
                data = self.get_price_validate_fields(fields, data)

                # 使用 yield from 将数据添加到列表中
                yield from [data]

            # 关闭数据库连接
            db_session.close()
        else:  # 如果不需要分批次处理数据
            # 分批将dolphindb获取的数据转换成dataframe
            data = self._get_price_get_data_todf(total_data)

            ''' 数据处理 '''
            # 根据frequency进行处理
            data = self.get_price_by_type_frequency(asset_type, frequency, data)

            # 根据start_date和end_date筛选数据
            data = self.get_price_filter_by_date(start_date, end_date, order_book_ids, data)

            # 对fields进行处理
            data = self.get_price_validate_fields(fields, data)

            yield data

            # 关闭数据库连接
            db_session.close()

    # @staticmethod
    def get_price_validate_order_book_ids(self, order_book_ids):
        """
        对order_book_ids 类型 以及 是否必填 进行校验
        :param order_book_ids: 合约类型

        :return: None
        """
        self.general_validate_params_required(order_book_ids, "order_book_ids")  # 校验必填参数
        self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")  # 校验参数类型

    def get_price_validate_frequency(self, frequency):
        """
        对frequency进行校验

        :param frequency: 频率
        :return: None
        """

        self.general_validate_params_required(frequency, "frequency")  # 校验必填参数
        if not isinstance(frequency, str):
            raise ValueError("frequency should be a string")

    def get_price_validate_start_end_date(self, start_date, end_date):
        """
        对 start_date 和 end_date 进行校验
        校验 start_date 和 end_date 是否同时提供，或者都不提供。

        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: None
        """
        if (start_date and not end_date) or (not start_date and end_date):
            raise ValueError("start_date and end_date should be both provided or not provided at all")
        if start_date and end_date:
            # 如果提供了，则进行进一步校验
            is_start_datetime = self._is_convertible_datetime(start_date)
            is_end_datetime = self._is_convertible_datetime(end_date)
            if not is_end_datetime or not is_start_datetime:
                raise ValueError(
                    "start_date and end_date should be datetime.datetime objects or "
                    "convertible to datetime.datetime objects")

            # 如果传入的数据类型符合要求，进行转换
            start_date, end_date = self._get_price_convert_start_end_date(start_date, end_date)
            if start_date > end_date:
                raise ValueError("start_date should be earlier than end_date")

    @staticmethod
    def _get_price_convert_start_end_date(start_date, end_date):
        """
        将 start_date 和 end_date 转换为 datetime 类型。

        :param start_date: 开始日期，可以是 datetime.datetime 对象或字符串。
        :param end_date: 结束日期，可以是 datetime.datetime 对象或字符串。
        :return: 转换后的 start_date 和 end_date。
        """

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') if isinstance(start_date, str) \
            else start_date
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') if isinstance(end_date, str) \
            else end_date

        return start_date, end_date

    @staticmethod
    def _is_convertible_datetime(date_data):
        """
        判断 date_data 是否是 datetime 类型或可以转换成 datetime 类型的字符串，并精确到秒。
        param: date_data: 要判断的值。

        Returns:
            True 如果 start_date 是 datetime 类型或可以转换成 datetime 类型的字符串，否则 False。
        """

        if isinstance(date_data, datetime.datetime):
            return True
        elif isinstance(date_data, str):
            try:
                datetime.datetime.strptime(date_data, "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def get_price_filter_by_date(start_date, end_date, order_book_ids, data):
        """
        根据start_date和end_date筛选数据
        此处order_book_ids参数用于处理未传递start_date和end_date的情况(根据order_book_ids返回距离当前时间最近的一条数据)

        :param start_date: 开始时间
        :param end_date: 结束时间
        :param order_book_ids: 合约代码
        :param data: 数据
        :return: 处理后的数据
        """
        # 将'date_time'列转换为datetime类型
        try:
            if data['datetime'].dtype != 'datetime64[ns]':
                data['datetime'] = pd.to_datetime(data['datetime'])
        except ValueError:
            raise ValueError("source data's datetime format is not correct")

        # 如果传递了start_date 和 end_date, 则返回时间段内的数据
        if start_date and end_date:
            data = data[
                (data['datetime'] >= start_date) & (data['datetime'] <= end_date)]

        # 如果没有传递start_date 和 end_date, 则根据传入的order_book_ids返回每个合约距离当前时间最近的一条数据
        elif not start_date and not end_date:
            date_time = datetime.datetime.now()
            data = data[
                data["datetime"] <= date_time]

            # 根据传入的order_book_ids进行处理
            if isinstance(order_book_ids, str):
                data = data.tail(1)
            else:
                # 将order_book_id作为分组键，并找到每个分组中距离当前时间最近的数据
                nearest_data = data.groupby('order_book_ids')
                # 使用 tail(1) 获取每个组的最后一条数据
                data = nearest_data.apply(lambda x: x.tail(1)).reset_index(drop=True)

        return data

    def get_price_validate_fields(self, fields, data):
        """
        根据用户选择的字段返回数据
        :param fields: 字段列表 -- 用户传入的需要返回的字段
        :param data: 数据 -- 需要筛选的数据

        :return : data -- 返回筛选后的数据

        """
        data = self.general_validate_fields(data, fields)

        return data

    def get_price_by_type_frequency(self, asset_type, frequency, data):
        """
        根据合约类型和frequency筛选数据

        :param asset_type: 合约类型
        :param frequency: 频率
        :param data: 数据
        :return: data: 返回筛选后的数据
        """
        # 判断asset_type是否存在
        if not get_price_frequency_dict.get(asset_type, None):
            raise ValueError(
                f"asset_type: got invalided value {asset_type}, choose any in {list(get_price_frequency_dict.keys())}")

        # frequency是否存在
        exists, suffix = self._ends_with(frequency, list(get_price_frequency_dict[asset_type].keys()))
        if not exists:
            raise ValueError(f"{frequency} is not a valid frequency for {asset_type} contract")
        # frequency存在再根据频率对数据做进一步处理
        else:
            bar_or_tick = get_price_frequency_dict[asset_type][suffix]  # 获取数据类型是bar还是tick，根据值处理字段
            data = self.get_price_data_rename_columns(bar_or_tick, data)  # 重命名字段

        return data

    @staticmethod
    def _ends_with(variable, suffixes):
        """判断变量是否以列表中的元素结尾。
        :param variable: 待判断的变量
        :param suffixes: 列表，元素为字符串，表示后缀
        :return: True or False
        """
        for suffix in suffixes:
            if variable.endswith(suffix):
                return True, suffix
        return False, ""

    @staticmethod
    def get_price_data_rename_columns(bar_or_tick, data):
        """
        将从数据库中获取的数据列名重命名

        :param bar_or_tick: 是bar类型数据还是tick类型(不同类型字段不同)
        :param data: 数据
        :return: 处理后的数据
        """

        new_columns = get_price_data_type_dict.get(bar_or_tick)
        data = data.rename(columns=new_columns)
        return data

    def _get_price_get_data(self, order_book_ids, table_name, db_path, start_date, end_date):
        """
        用于接收数据表以及数据库，获取数据
        : params order_book_ids: 合约代码
        : params table_name: 数据表路径
        : params db_path: 数据库路径
        : params start_date: 开始时间
        : params end_date: 结束时间

        : return filtered_data: 从数据库获取并根据合约代码筛选后的数据
        """

        get_price_data, db_session = self.connect_db(table_name, db_path)

        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            limit_data = get_price_data.where(f"instrument_id='{order_book_ids}'")
        else:
            limit_data = get_price_data.where(f"instrument_id in {order_book_ids}")

        # 将日期转换成 DolphinDB 识别的日期格式，用于筛选数据
        format_start_date = self.get_price_format_date(start_date)
        format_end_date = self.get_price_format_date(end_date)

        # 根据日期对数据再次进行筛选，最大程度减轻数据库压力
        limit_data = limit_data.where(f"trade_time >= {format_start_date} and trade_time <= {format_end_date}")

        return limit_data, db_session

    @staticmethod
    def get_price_format_date(date_str):
        """将日期字符串格式化为 'YYYY.MM.DD HH:mm:ss' 格式。
        : params date_str: 日期字符串，例如 '2018-01-04 09:01:00'。
        : return ：
            格式化后的日期字符串，例如 '2018.01.04 09:01:00'。
        """
        if isinstance(date_str, str):
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y.%m.%d %H:%M:%S')
        return date_str.strftime('%Y.%m.%d %H:%M:%S')

    @staticmethod
    def _get_price_get_data_todf(data):
        """
        用于接收从数据库获取的数据，并分批处理，将其转换成dataframe格式的数据返回
        : params data: 从数据库获取的数据
        : return : 转换成dataframe格式后的数据
        """

        result = pd.DataFrame()
        if data.rows > 1000000:
            chunk_size, start = 1000000, 0
            while start < data.rows:
                limit_data = data.limit([start, chunk_size]).toDF()
                result = limit_data if result.empty else pd.concat([result, limit_data], ignore_index=True)
                start += chunk_size

            return result
        return data.toDF()

    def get_price_data_get_data(self, order_book_ids, db_table_name, start_date, end_date):
        """
        根据参数获取数据库和表名，调用接口获取数据

        :param order_book_ids: 合约代码列表
        :param db_table_name: 数据库名称和表名
        :param start_date: 开始时间
        :param end_date: 结束时间
        :return: dolphin_data, db_session
        """

        dolphin_data, db_session = self._get_price_get_data(order_book_ids, *db_table_name, start_date, end_date)
        return dolphin_data, db_session

    @staticmethod
    def get_price_get_db_table_name(asset_type, frequency):
        if asset_type == "future":
            return {
                "tick_l1": (history_future_tick_db_table_name, history_future_tick_db_path),
                "1d": (history_future_day_db_table_name, history_future_day_db_path),
                "1min": (history_future_min_db_table_name, history_future_min_db_path),
                "1min_gtja": (history_future_1min_gtja_db_table_name, history_future_1min_gtja_db_path),
                "tick_l2": (history_future_tick_l2_db_table_name, history_future_tick_l2_db_path),
            }.get(frequency)
        elif asset_type == "option":
            return {
                "1d": (history_option_day_db_table_name, history_option_day_db_path),
                "1min": (history_option_min_db_table_name, history_option_min_db_path),
                "tick": (history_option_tick_db_table_name, history_option_tick_db_path),
            }.get(frequency)
        else:
            raise Exception("asset_type is not valid or frequency is not valid for this asset_type")

    """ get_instruments(合约基础信息) """

    def get_instruments(self, order_book_ids=None, commodity=None, asset_type=None, fields=None):
        """
        获取合约基础信息接口
        :param order_book_ids: str or list,合约代码 和 commodity_type 必填 二选一
        :param commodity: str or list, 合约品种  和 commodity_type 必填 二选一  若填写品种参数，则返回该品种所有合约基础信息
        :param asset_type: str, 合约类型--必填
        :param fields: str or list, 字段列表--选填，默认为全部字段
        :return: data:合约基础信息
        """

        ''' 数据校验 '''
        # 对order_book_ids和commodity是否必填进行校验

        self.get_instruments_validate_order_book_ids_commodity(order_book_ids, commodity)

        # 对asset_type进行校验
        self.general_validate_asset_type(asset_type)

        ''' 根据传入的asset_type以及order_book_ids获取数据 '''
        data = self.get_instruments_data_get_data(asset_type=asset_type, order_book_ids=order_book_ids,
                                                  commodity=commodity)

        # 重命名字段
        data = self.get_instruments_data_rename_columns(asset_type, data)

        # 从交易参数中填充commodity和trading_hour的值
        data = self.get_instruments_deal_commodity_trading_hour(data)

        ''' 按照文档筛选需要返回的字段 '''
        data = self.get_instruments_data_filter_return_fileds(asset_type, data)

        # 对fields进行校验并根据fields返回对应的字段
        data = self.get_instruments_validate_fields(fields, data)

        return data

    def get_instruments_validate_order_book_ids_commodity(self, order_book_ids, commodity):
        """
        对order_book_ids和commodity_type进行校验
        order_book_ids和commodity_type二选一，且只能二选一
        :param order_book_ids: str or list,合约代码
        :param commodity: str or list, 合约品种
        :return: None
        """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_ids", order_book_ids, "commodity", commodity)

        if order_book_ids:
            self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")
        if commodity:
            self.general_validate_field_str_or_list(commodity, "commodity")

    @staticmethod
    def get_instruments_data_filter_return_fileds(asset_type, data):
        """
        根据asset_type返回对应的字段(不同合约类型字段不同)
        :param asset_type: 合约类型，"future" or "option"
        :param data: 数据
        :return: data: 返回筛选后的数据
        """

        if asset_type == "future":
            data = data[get_instruments_type_dict.get("future_return_fields")]
        elif asset_type == "option":
            data = data[get_instruments_type_dict.get("option_return_fields")]

        return data

    def get_instruments_validate_fields(self, fields, data):
        """
        根据用户选择的字段返回数据
        :param fields: str or list, 字段列表
        :param data: 数据
        :return: data: 返回筛选后的数据
        """

        data = self.general_validate_fields(data, fields)

        return data

    def _get_instruments_data_get_data(self, order_book_ids, table_name, db_path):
        """
        用于接收数据表以及数据库，获取数据

        :param order_book_ids: 合约代码
        :param table_name: 数据表路径
        :param db_path: 数据库路径
        :return: 获取的数据
        """
        get_instruments_data, db_session = self.connect_db(table_name, db_path)

        filtered_data = pd.DataFrame()
        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            filtered_data = get_instruments_data.where(f"instrumentid='{order_book_ids}'").toDF()
        elif isinstance(order_book_ids, list):
            filtered_data = get_instruments_data.where(f"instrumentid in {order_book_ids}").toDF()

        # 关闭数据库连接
        db_session.close()

        return filtered_data

    def get_instruments_data_get_data(self, asset_type=None, order_book_ids=None, commodity=None):
        """
        根据参数获取数据库和表名，调用接口获取数据

        :param asset_type: 合约类型
        :param order_book_ids: 合约代码
        :param commodity: 合约品种
        :return: data: 获取的数据
        """

        # 如果传入的是commodity，需要获取参数品种下所有合约代码
        if commodity:
            # 如果传递的是品种信息，根据品种去交易参数表中查找出对对应的数据
            # 获取交易参数
            trading_param_data, db_session = self.connect_db(trading_params_db_table_name, trading_params_db_path)

            if isinstance(commodity, str):
                order_book_ids = list(set(
                    trading_param_data.select("contractcode").where(f"productcode = '{commodity}'").toDF()[
                        "contractcode"].to_list()))
            elif isinstance(commodity, list):
                order_book_ids = list(set(
                    trading_param_data.select("contractcode").where(f"productcode in {commodity}").toDF()[
                        "contractcode"].to_list()))

            # 关闭数据库连接
            db_session.close()

        ''' 期货行情数据 '''
        if asset_type == "future":
            data = self._get_instruments_data_get_data(order_book_ids,
                                                       future_contract_db_table_name,
                                                       future_contract_db_path)
            data["type"] = "future"
        elif asset_type == "option":
            data = self._get_instruments_data_get_data(order_book_ids,
                                                       option_contract_db_table_name,
                                                       option_contract_db_path)
            data["type"] = "option"
            data["exercise_type"] = data["optionstype"]
        else:
            raise Exception("asset_type is not valid")
        data["commodity"] = ""
        data["trading_hour"] = ""

        return data

    @staticmethod
    def get_instruments_data_rename_columns(asset_type, data):
        """
        将从数据库中获取的数据列名重命名为文档要求的名字

        :param asset_type: 合约类型
        :param data: 数据
        :return: data
        """

        new_columns = get_instruments_type_dict.get(asset_type)
        data = data.rename(columns=new_columns)

        return data

    def get_instruments_deal_commodity_trading_hour(self, data):
        """
        用于处理commodity和trading_hour
        :param data: 数据
        :return: data: 处理后的数据
        """

        try:
            # 获取交易参数
            trading_param_data, db_session = self.connect_db(trading_params_db_table_name, trading_params_db_path)

            for index, row in data.iterrows():
                match = trading_param_data.toDF()[trading_param_data.toDF()['contractcode'] == row['order_book_id']]
                if not match.empty:
                    data.loc[index, 'commodity'] = match['productcode'].iloc[0]
                    data.loc[index, 'trading_hour'] = match['tradesection'].iloc[0]
            db_session.close()
        except ValueError as e:
            print(e)
            pass

        return data

    """   get_trading_dates(交易日历)  """

    def get_trading_dates(self, date=datetime.date.today(), n=None, start_date=None, end_date=None):
        """
        获取交易日历接口
        :param date: str--选填, 日期
        :param n: str--必填，根据不同值获取对应的交易日历
        :param start_date: str（datetime.date, datetime.datetime）--选填, 开始日期
        :param end_date: str（datetime.date, datetime.datetime）--选填, 结束日期
        若填写【date、n】为入参，则无法填写【start_date、end_date】，反之依然
        :return: data:交易日历
        """

        """ 校验参数 """
        data = self.get_trading_dates_validate_date_n_start_end(date, n, start_date, end_date)

        return data

    def get_trading_dates_validate_date_n_start_end(self, date, n, start_date, end_date):
        """
        校验date、n和start_date、end_date有效性

        :param date: str-- 日期
        :param n: str--根据不同值获取对应的交易日历
        :param start_date: str（datetime.date, datetime.datetime）--开始日期
        :param end_date: str（datetime.date, datetime.datetime）--结束日期
        :return: 如果校验通过，就返回对应的数据，否则抛出异常
        """

        if (date and n) and (start_date and end_date):
            raise ValueError("date、n and start_date、end_date can only be selected one at a time")
        if n and (start_date or end_date):
            raise ValueError("parameter error: cannot pass date、n and start_date、end_date at the same time")
        elif date and n:  # 根据date和n获取交易日历
            return self.get_trading_dates_by_date_n(date, n)
        elif start_date and end_date:  # 根据start_date和end_date获取交易日历
            return self.get_trading_dates_by_start_end(start_date, end_date)
        else:
            raise ValueError("parameter error: please pass date、n or start_date、end_date")

    def get_trading_dates_by_date_n(self, date, n):
        """
        校验 date 和 n
        :param date: str--选填, 日期
        :param n: str--必填，根据不同值获取对应的交易日历
        :return: 根据date和n筛选后的数据
        """

        if not isinstance(n, str):
            raise ValueError("n parameter error, type should be str")
        if n not in ["0", "1", "2", "3", "4", "5", "6"]:
            raise ValueError("n parameter error, value range should be [0, 1, 2, 3, 4, 5, 6]")
        if not isinstance(date, (str, datetime.date)):
            raise ValueError("date parameter error, type should be str or datetime.date")

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        return self.get_dates_in_n(date, n)

    def get_trading_dates_by_start_end(self, start_date, end_date):
        """
        根据start_date和end_date获取交易日历
        :param start_date: str（datetime.date, datetime.datetime）--选填, 开始日期
        :param end_date: str（datetime.date, datetime.datetime）--选填, 结束日期

        :return: data:根据start_date和end_date筛选后的数据
        """

        trading_params_data = self.get_trading_dates_get_data()

        # 校验日期类型
        if self.check_date_type(start_date, end_date):
            # 如果类型校验通过，则将start_date和end_date处理成对应的时间数据类型
            if isinstance(start_date, str):
                start_date = self._get_trading_dates_by_start_end(start_date)
            if isinstance(end_date, str):
                end_date = self._get_trading_dates_by_start_end(end_date)
            # 筛选 tradingday 列在 start_date 和 end_date 之间的数据
            filtered_df = trading_params_data.loc[
                (trading_params_data['tradingday'] >= start_date) & (trading_params_data['tradingday'] <= end_date)]

            # 筛选 tradeflag 列等于 T 的数据（是交易日的数据）
            final_df = filtered_df.loc[filtered_df['tradeflag'] == 'T']
            data = sorted(final_df["tradingday"].tolist())
            return data
        else:
            raise ValueError(
                "start_date or end_date type error, please input str, datetime.date or datetime.datetime type")

    @staticmethod
    def _get_trading_dates_by_start_end(time_data):
        """
        将时间str数据处理成对应的时间类型（例如：date类型的str，处理成datetime.date类型）

        :param time_data: 时间数据
        :return: 转换后的时间数据类型
        """
        try:
            time_data = datetime.datetime.strptime(time_data, "%Y-%m-%d").date()
            return time_data
        except ValueError:
            try:
                time_data = datetime.datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S").date()
                return time_data
            except ValueError:
                raise ValueError("parameter type error")

    def check_date_type(self, _start_date, _end_date):
        """
        判断start_date和end_date是否为str，datetime.date, datetime.datetime三种类型，
        其中，如果是str类型，还要判断是否是datetime.date, datetime.datetime两种类型的字符串.
        :params _start_date: 开始日期
        :params _end_date: 结束日期

        :return: 如果类型正确，返回 True。否则返回 False，并打印错误信息
        """
        if isinstance(_start_date, (str, datetime.date, datetime.datetime)) and \
                isinstance(_end_date, (str, datetime.date, datetime.datetime)):
            if isinstance(_start_date, str) and not self.general_validate_date(_start_date):
                raise ValueError("start_date is not a valid date string format")
            if isinstance(_end_date, str) and not self.general_validate_date(_end_date):
                raise ValueError("end_date is not a valid date string format")
            return True
        else:
            raise ValueError(
                "start_date or end_date type error, please input str, datetime.date or datetime.datetime type")

    def get_trading_dates_get_data(self):
        """
        从dolphindb获取交易日历
        :return: 交易日历数据
        """

        params_data, db_session = self.connect_db(trading_dates_db_table_name, trading_dates_db_path)
        trading_params_data = params_data.toDF()
        trading_params_data["tradingday"] = pd.to_datetime(trading_params_data["tradingday"], format="%Y%m%d").dt.date
        db_session.close()
        return trading_params_data

    @staticmethod
    def get_date_get_week_month_year(data, start_date, end_date):
        """
        用于获取当前日期所在周、月、年的交易日数据

        :param data: 交易日历数据
        :param start_date: 开始日期
        :param end_date: 结束日期

        :return: 交易日历数据

        """

        # 获取开始日期和结束日期
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d").date()

        # 筛选出时间段内的所有数据
        filtered_df = data.loc[(data['tradingday'] >= start_date) & (data['tradingday'] <= end_date)]
        # 筛选出时间段内的所有交易日
        final_df = filtered_df.loc[filtered_df['tradeflag'] == 'T']

        return sorted(final_df["tradingday"].tolist())

    def get_dates_in_n(self, _date, _n):
        """
        获取选定日期, 根据n值获取对应的交易日历。

        :param _date: 选定的日期，可以是 datetime.date 或 datetime.datetime 对象
        :param _n: 时间段，可以是 'week'、'month' 或 'year'
        :return: 一个包含所有日期的列表
        """

        trading_params_data = self.get_trading_dates_get_data()

        cn_holidays = holidays.CN()  # 创建中国节假日对象

        time_period_mapping_dict = {
            "0": _date in cn_holidays,
            "1": trading_params_data.loc[trading_params_data["tradingday"] == _date]["nexttrdday"].iloc[0],
            "2": trading_params_data.loc[trading_params_data["tradingday"] == _date]["prevtrdday"].iloc[0],
            "3": self.get_date_get_week_month_year(trading_params_data,
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "firsttrddayweek"].iloc[0],
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "lasttrddayweek"].iloc[0]),
            "4": self.get_date_get_week_month_year(trading_params_data,
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "firsttrddaymonth"].iloc[0],
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "lasttrddaymonth"].iloc[0]),
            "5": self.get_date_get_week_month_year(trading_params_data,
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "firsttrddayyear"].iloc[0],
                                                   trading_params_data.loc[trading_params_data["tradingday"] == _date][
                                                       "lasttrddayyear"].iloc[0]),
            "6": trading_params_data.loc[trading_params_data["tradingday"] == _date]["nightday"].iloc[0],
        }

        if _n not in time_period_mapping_dict:
            raise ValueError("n parameter error, value range should be [0, 1, 2, 3, 4, 5, 6]")

        return time_period_mapping_dict[_n]

    """ get_margin_ratio 期货保证金 """

    def get_margin_ratio(self, order_book_id=None, commodity=None, date=datetime.datetime.now(), exchange=None):
        """
        获取期货保证金信息接口
        :param order_book_id: str--选填（和commodity二选一），合约代码
        :param commodity: str--选填（和order_book_id二选一），合约品种,如果入参为品种，则返回该品种条件下所有合约的保证金list
        :param date: datetime--必填（默认今天)，日期
        :param exchange: str--必填，交易所
        :return: 期货保证金数据
        """

        """ 校验数据 """
        # 校验order_book_id和commodity
        data = self.get_margin_ratio_validate_order_book_id_commodity(order_book_id, commodity)

        # 校验exchange
        self.get_margin_ratio_validate_exchange(exchange)

        # 校验date
        self.get_margin_ratio_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        data = self.get_margin_ratio_data_by_date(date, data)

        # 根据exchange筛选数据
        data = self.get_margin_ratio_data_by_exchange(exchange, data)

        return data[["order_book_id", "commodity", "date", "exchange"]]

    def get_margin_ratio_validate_exchange(self, exchange):
        """
        校验exchange
        :param exchange: str--必填，交易所
        :return: None
        """

        self.general_validate_params_required(exchange, "exchange")  # 校验必填参数

        if not isinstance(exchange, str):
            raise ValueError("exchange should be str")

    def get_margin_ratio_validate_order_book_id_commodity(self, order_book_id, commodity):
        """
        校验order_book_id和commodity
        :param order_book_id: str--二选一，合约代码
        :param commodity: str--二选一，品种
        :return: data: 期货保证金数据
        """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_id", order_book_id, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''

        data, db_session = self.get_margin_ratio_get_data()
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_id:
            data = self._general_filter_data_by_field(data, "order_book_id", order_book_id)
        if commodity:
            data = self._general_filter_data_by_field(data, "commodity", commodity)
        return data

    def get_margin_ratio_get_data(self):
        """
        获取数据
        :return: data: 期货保证金数据
        """

        table_name, db_path = "sfsfsd", "asfdsdf"
        data, db_session = self.connect_db(table_name, db_path)

        return data, db_session

    # def get_margin_ratio_get_data_filter_data_from_dolphindb(self, data, field):
    #     """
    #     从dolphindb中筛选数据
    #     :param data: 期货保证金数据
    #     :param field: str--筛选字段
    #     :return: data: 期货保证金数据
    #     """

    #     # 使用 DolphinDB 的 where 子句筛选数据
    #     if isinstance(order_book_ids, str):
    #         limit_data = get_price_data.where(f"instrument_id='{order_book_ids}'")
    #     else:
    #         limit_data = get_price_data.where(f"instrument_id in {order_book_ids}")

    #     # 将日期转换成 DolphinDB 识别的日期格式，用于筛选数据
    #     format_start_date = self.get_price_format_date(start_date)
    #     format_end_date = self.get_price_format_date(end_date)

    #     # 根据日期对数据再次进行筛选，最大程度减轻数据库压力
    #     limit_data = limit_data.where(f"trade_time >= {format_start_date} and trade_time <= {format_end_date}")

    #     return limit_data, db_session

    def get_margin_ratio_validate_date(self, date):
        """
        校验date
        :param date: datetime--日期
        :return: None
        """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date is not a valid date string format")
            # return True
        else:
            raise ValueError("date type error, please pass in str, datetime.date or datetime.datetime type")

    @staticmethod
    def get_margin_ratio_data_by_date(date, data):
        """
        根据date筛选数据
        :param date: datetime--日期
        :param data: 期货保证金数据
        :return: data: 期货保证金数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return data[data["date"] == date]

    @staticmethod
    def get_margin_ratio_data_by_exchange(exchange, data):
        """
        根据exchange筛选数据
        :param exchange: str--交易所
        :param data: 期货保证金数据
        :return: data: 期货保证金数据
        """

        return data[data["exchange"] == exchange]

    """ get_fee 期货交割手续费 """

    def get_fee(self, order_book_id=None, commodity=None, date=datetime.datetime.now(), exchange=None):
        """
        获取期货交割手续费信息接口
        :param order_book_id: str--选填（和commodity二选一），合约代码
        :param commodity: str--选填（和order_book_id二选一），合约品种,如果入参为品种，则返回该品种条件下所有合约的交割手续费list
        :param date: datetime--必填（默认今天)，日期
        :param exchange: str--必填，交易所
        :return: 期货交割手续费
        """

        """ 校验数据 """
        # 校验order_book_id和commodity
        data = self.get_fee_validate_order_book_id_commodity(order_book_id, commodity)

        # 校验exchange
        self.get_fee_validate_exchange(exchange)

        # 校验date
        self.get_fee_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        data = self.get_fee_data_by_date(date, data)

        # 根据exchange筛选数据
        data = self.get_fee_data_by_exchange(exchange, data)

        return data[["order_book_id", "commodity", "date", "exchange"]]

    def get_fee_validate_exchange(self, exchange):
        """
        校验exchange
        :param exchange: str--必填，交易所
        :return: None
        """
        # 是否必填
        self.general_validate_params_required(exchange, "exchange")

        if not isinstance(exchange, str):
            raise ValueError("exchange should be str")

    def get_fee_validate_order_book_id_commodity(self, order_book_id, commodity):
        """
        校验order_book_id和commodity
        :param order_book_id: str--二选一，合约代码
        :param commodity: str--二选一，品种
        :return: data:期货交割手续费数据
        """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_id", order_book_id, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''

        data = self.get_fee_get_data()
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_id:
            data = self._general_filter_data_by_field(data, "order_book_id",
                                                      order_book_id)
        if commodity:
            data = self._general_filter_data_by_field(data, "commodity",
                                                      commodity)

        return data

    def get_fee_get_data(self):
        """
        获取期货交割手续费数据
        :return: data:期货交割手续费数据
        """
        table_name, db_path = "sfsdf", "sfdfs"
        data = self.connect_db(table_name, db_path)
        return data

    def get_fee_validate_date(self, date):
        """
        校验date
        :param date: datetime--日期
        :return: None
        """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date is not a valid date string format")
            # return True
        else:
            raise ValueError("date type error, please pass in str, datetime.date or datetime.datetime type")

    @staticmethod
    def get_fee_data_by_date(date, data):
        """
        根据date筛选数据
        :param date: datetime--日期
        :param data: 期货交割手续费数据
        :return: data:期货交割手续费数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return data[data["date"] == date]

    @staticmethod
    def get_fee_data_by_exchange(exchange, data):
        """
        根据exchange筛选数据
        :param exchange: str--交易所
        :param data: 期货交割手续费数据
        :return: data:期货交割手续费数据
        """

        return data[data["exchange"] == exchange]

    """ get_limit_position 期货限仓数据 """

    def get_limit_position(self, order_book_ids=None, commodity=None, date=datetime.date.today()):
        """
        获取期货限仓数据接口
        :param order_book_ids: str or list--选填（和commodity二选一），合约代码
        :param commodity: str or list--选填（和order_book_ids二选一），合约品种
        :param date: datetime.date--选填（默认今天)，日期
        :return: 期货限仓数据

        """

        """ 校验数据 """
        # 校验order_book_ids和commodity
        data = self.get_limit_position_validate_order_book_ids_commodity(order_book_ids, commodity)

        # 校验date
        self.get_limit_position_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        data = self.get_limit_position_data_by_date(date, data)

        return data

    def get_limit_position_validate_order_book_ids_commodity(self, order_book_ids, commodity):
        """
        对order_book_ids和commodity_type进行校验
        :param order_book_ids: str or list--选填（和commodity二选一），合约代码
        :param commodity: str or list--选填（和order_book_ids二选一），合约品种
        :return: data: 期货限仓数据
        """
        self.general_validate_either_or("order_book_ids", order_book_ids, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''
        data = self.get_limit_position_get_data()
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_ids:
            data = self._general_filter_data_by_field(data, "order_book_ids", order_book_ids)
        if commodity:
            data = self._general_filter_data_by_field(data, "commodity", commodity)

        return data

    def get_limit_position_get_data(self):
        """
        获取数据
        :return: 期货限仓数据
        """
        table_name, db_path = "sfsf", "sfd"
        return self.connect_db(table_name, db_path)

    def get_limit_position_validate_date(self, date):
        """
        校验date
        :param date: datetime.date--选填，日期
        :return: None
        """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date is not a valid date string format")
            # return True
        else:
            raise ValueError("date type error, please pass in str, datetime.date or datetime.datetime type")

    @staticmethod
    def get_limit_position_data_by_date(date, data):
        """
        根据date筛选数据
        :param date: datetime.date--选填，日期
        :param data: 期货限仓数据
        :return :筛选后的期货限仓数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return data[data["date"] == date]

    """ get_active_contract 主力/次主力合约 """

    def get_active_contract(self, code=None, begin_date=None, start_date=datetime.date.today(),
                            end_date=datetime.date.today(), asset_type=None,
                            fields=None, source="3"):
        """
        获取主力/次主力合约信息接口
        :param code: str or str list--必填，品种
        :param begin_date: datetime--必填，指定日期
        :param start_date: date--必填，默认当天
        :param end_date: date--必填，默认当天
        :param asset_type: str--必填，active指主力；next_active次主力
        :param fields: str or str list--选填，返回字段，默认全部
        :param source: str--选填，数据源，默认研究所, 3个来源可选：1-数据中台, 2-米筐, 3-研究所

        :return: 主力/次主力合约
        """

        """ 校验参数 """
        # 校验必填参数
        self.get_active_contract_validate_required_params(code, begin_date, start_date, end_date, asset_type)

        # 校验日期参数类型
        self.get_active_contract_validate_date_type(begin_date, start_date, end_date)

        """ 校验code类型 """
        self.get_active_contract_validate_code(code)

        """ 筛选数据 """

        # 根据code筛选数据
        data = self.get_active_contract_filter_by_code(code)

        # 根据日期数据筛选数据
        data = self.get_active_contract_filter_by_date(begin_date, start_date, end_date, data)

        # 根据asset_type筛选数据
        data = self.get_active_contract_filter_by_asset_type(asset_type, data)

        # 根据fields筛选数据
        data = self.get_active_contract_filter_data_by_fields(fields, data)

        # 根据source筛选数据
        data = self.get_active_contract_data_by_source(source, data)

        return data

    def get_active_contract_validate_required_params(self, code, begin_date, start_date, end_date, asset_type):
        """
        校验参数是否必填
        :param code: str or str list--必填，品种
        :param begin_date: datetime--必填，指定日期
        :param start_date: date--必填，默认当天
        :param end_date: date--必填，默认当天
        :param asset_type: str--必填，active指主力；next_active次主力
        :return: None
        """

        params_dict = {
            "code": code,
            "begin_date": begin_date,
            "start_date": start_date,
            "end_date": end_date,
            "asset_type": asset_type
        }
        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)  # 校验必填参数

    def get_active_contract_validate_code(self, code):
        """
        校验code 类型
        :param code: str or str list--必填，品种
        :return: None
        """
        self.general_validate_field_str_or_list(code, "code")

    def get_active_contract_filter_by_code(self, code):
        """
        根据code过滤数据
        :param code: str or str list--必填，品种
        :return: 主力/次主力合约数据
        """

        data = self.get_active_contract_get_data()
        data = data[
            data["code"].isin(code)] if isinstance(code, list) else \
            data[data["code"] == code]

        return data

    def get_active_contract_get_data(self):
        """
        获取数据
        :return: 主力/次主力合约数据
        """

        table_name, db_path = "sfsf", "sfd"
        data, db_session = self.connect_db(table_name, db_path)

        return data, db_session

    def get_active_contract_validate_date_type(self, begin_date, start_date, end_date):
        """
        校验日期数据的类型
        :param begin_date: datetime--必填，指定日期
        :param start_date: date--必填，默认当天
        :param end_date: date--必填，默认当天
        :return: None
        """
        # 校验start_date 和 end_date 是否为datetime.date类型或者可以转换成该类型的str
        if isinstance(start_date, (str, datetime.date)) and isinstance(end_date, (str, datetime.date)):
            if isinstance(start_date, str) and not self.general_validate_date_str_is_date_type(start_date):
                raise ValueError("start_date type error， please enter datetime.date type")
            if isinstance(end_date, str) and not self.general_validate_date_str_is_date_type(end_date):
                raise ValueError("start_date type error， please enter datetime.date type")
        else:
            raise ValueError("start_date or end_date type error, please enter datetime.date type")

        # 校验begin_date 是否为datetime.datetime类型或者为可以转换为该类型的字符串
        if isinstance(begin_date, (str, datetime.datetime)):
            if isinstance(begin_date, str) and not self.general_validate_date_str_is_datetime_type(begin_date):
                raise ValueError("begin_date type error， please enter datetime.datetime type")
        else:
            raise ValueError("begin_date type error， please enter datetime.datetime type")

    def get_active_contract_filter_by_date(self, begin_date, start_date, end_date, data):
        """
        根据日期筛选数据
        :param begin_date: datetime--必填，指定日期
        :param start_date: date--必填，默认当天
        :param end_date: date--必填，默认当天
        :param data: 主力/次主力合约数据
        :return: 筛选后的数据
        """

        if start_date > end_date:
            raise ValueError("start_date should be earlier than end_date")

        # 根据start_date 和 end_date 筛选数据
        start_date = self.general_date_str_to_date(start_date)
        end_date = self.general_date_str_to_date(end_date)
        data = data[
            (data["date"] >= start_date) & (data["date"] <= end_date)]

        return data

    def get_active_contract_filter_by_asset_type(self, asset_type, data):
        """
        根据asset_type筛选数据
        :param asset_type: str--必填，active指主力；next_active次主力
        :param data: 主力/次主力合约数据
        :return: 筛选后的数据
        """

        return self.general_filter_data_by_field(data, "active_type", asset_type)

    @staticmethod
    def get_active_contract_filter_data_by_fields(fields, data):
        """
        根据fields筛选数据
        :param fields: str or str list--选填，返回字段，默认全部
        :param data: 主力/次主力合约数据
        :return: 筛选后的数据
        """

        if isinstance(fields, (str, list)):
            data = data[fields] if isinstance(fields, str) else \
                data[[field for field in fields]]

        return data

    @staticmethod
    def get_active_contract_data_by_source(source, data):
        """
        根据数据源筛选数据
        :param source: str--选填，数据源，默认研究所, 3个来源可选：1-数据中台, 2-米筐, 3-研究所
        :param data: 主力/次主力合约数据
        :return: 筛选后的数据
        """

        if not isinstance(source, str):
            raise ValueError("source 类型错误，请传入 str 类型")

        if source == "1":
            print("数据中台")
        elif source == "2":
            print("米筐")
        elif source == "3":
            print("研究所")
        else:
            raise ValueError("source 参数错误，取值范围应该在 [1, 2, 3]")

        return data

    """ get_basic_data 库存/基差/现货价格-数据（日频） """

    def get_basic_data(self, order_book_id, asset_type, start_date, end_date):
        """
        获取库存/基差/现货价格-数据（日频）接口
        :param order_book_id: str--必填，合约代码
        :param asset_type: str--必填，枚举值：库存、基差、现货
        :param start_date: str, datetime.date, datetime.datetime, pandasTimestamp--必填，开始日期
        :param end_date: str, datetime.date, datetime.datetime, pandasTimestamp--必填，结束日期
        :return: 库存/基差/现货价格-数据（日频）
        """

        """ 校验参数 """

        # 校验必填参数
        self.get_basic_data_validate_required_params(order_book_id, asset_type, start_date, end_date)

        # 校验order_book_id 类型
        self.get_basic_data_validate_order_book_id(order_book_id)

        # 校验asset_type 类型
        self.get_basic_data_validate_asset_type(asset_type)

        # 校验start_date 和 end_date 类型
        self.get_basic_data_validate_date(start_date, end_date)

        """ 获取数据 """
        table_name, db_path = "dfs://afafaf", "test_db"
        data = self.get_basic_data_get_data(order_book_id, table_name, db_path)

        """ 筛选数据 """
        # 根据start_date 和 end_date 筛选数据
        data = self.get_basic_data_filter_data_by_date(start_date, end_date, data)

        # 根据asset_type 筛选数据
        data = self.get_basic_data_filter_data_by_asset_type(asset_type, data)

        return data

    def get_basic_data_validate_required_params(self, order_book_id, asset_type, start_date, end_date):
        params_dict = {
            "order_book_id": order_book_id,
            "asset_type": asset_type,
            "start_date": start_date,
            "end_date": end_date
        }
        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)  # 校验必填参数

    def get_basic_data_validate_order_book_id(self, order_book_id):
        """
        校验order_book_id 类型
        :param order_book_id: str--必填，合约代码
        :return: None
        """

        self.general_validate_param_is_str("order_book_id", order_book_id)

    def get_basic_data_validate_asset_type(self, asset_type):
        """
        校验asset_type 类型
        :param asset_type: str--必填，枚举值：库存、基差、现货
        :return: None
        """

        self.general_validate_param_is_str("asset_type", asset_type)

    def get_basic_data_validate_date(self, start_date, end_date):
        """
        校验start_date 和 end_date 类型
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: None
        """
        error_msg = "start_date or end_date type error, datetime.date, datetime.datetime, pandasTimestamp type or can be converted to the type"

        # 校验start_date 和 end_date 是否为datetime.date, datetime.datetime, pandasTimestamp类型或者可以转换成该类型的str
        if isinstance(start_date, (str, datetime.date, datetime.datetime, pd.Timestamp)) and isinstance(end_date, (
                str, datetime.date, datetime.datetime, pd.Timestamp)):
            if isinstance(start_date, str) and not self.general_validate_date(start_date):
                raise ValueError(error_msg)
            if isinstance(end_date, str) and not self.general_validate_date(end_date):
                raise ValueError(error_msg)
        else:
            raise ValueError(error_msg)

    # @staticmethod
    def get_basic_data_get_data(self, order_book_ids, table_name, db_path):
        """
        获取get_basic_data数据
        :param order_book_ids: 合约代码
        :param table_name: 表名
        :param db_path: 数据库路径
        :return: 从对应数据库中获取的数据

        """

        get_basic_data_data, db_session = self.connect_db(table_name, db_path)
        get_basic_data_data = pd.DataFrame()  # 测试，用了数据库信息后需要替换成上面的代码

        filtered_data = pd.DataFrame()
        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            filtered_data = get_basic_data_data.where(f"instrumentid='{order_book_ids}'").toDF()
        elif isinstance(order_book_ids, list):
            filtered_data = get_basic_data_data.where(f"instrumentid in {order_book_ids}").toDF()

        # 关闭数据库连接
        # db_session.close()  # 用了数据库信息后，需要取消注释

        return filtered_data, db_session

    def get_basic_data_filter_data_by_date(self, start_date, end_date, data):
        """
        根据日期过滤get_basic_data数据
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param data: 数据

        :return: 过滤后的数据
        """

        start_date = self._get_basic_data_filter_data_by_date_conversion(start_date)
        end_date = self._get_basic_data_filter_data_by_date_conversion(end_date)

        # 根据转换后的日期过滤数据
        data = data[
            (data['date'] >= start_date) & (data['date'] <= end_date)]

        return data

    def _get_basic_data_filter_data_by_date_conversion(self, date_str):
        """
        将日期字符串转换成对应格式的日期数据
        :param date_str: 日期字符串
        :return: 转换后的日期数据
        """

        if isinstance(date_str, str):
            if self.general_validate_date_str_is_datetime_type(date_str):
                return self.general_date_str_to_datetime(date_str)
            if self.general_validate_date_str_is_date_type(date_str):
                return self.general_date_str_to_date(date_str).date()

        return date_str

    @staticmethod
    def get_basic_data_filter_data_by_asset_type(asset_type, data):
        """
        根据数据类型过滤数据
        :param asset_type: 数据类型
        :param data: 数据
        :return: 过滤后的数据
        """
        data = data[data['type'] == asset_type]
        return data

    """ get_warehouse_stocks_future 仓单数据 """

    def get_warehouse_stocks_future(self, commodity=None, start_date=None,
                                    end_date=datetime.date.today() - datetime.timedelta(days=1)):
        """
        获取仓单数据
        :param commodity: str--必填，期货合约品种
        :param start_date: str--必填，开始日期
        :param end_date: str--必填，结束日期 (默认为策略当天日期的前一天)
        :return: 仓单数据
        """

        """ 校验必填参数 """
        # 校验commodity, start_date, end_date 是否为必填参数
        self.get_warehouse_stocks_future_validate_required_params(commodity, start_date, end_date)

        # 校验commodity, start_date, end_date 是否为str类型
        self.get_warehouse_stocks_future_validate_type_str(commodity, start_date, end_date)

        """ 获取数据 """
        # 从数据库中获取数据
        data = self.get_warehouse_stocks_future_get_data(commodity)

        """ 筛选数据 """
        # 根据日期筛选数据
        data = self.get_warehouse_stocks_future_filter_data_by_date(start_date, end_date, data)

        return data

    def get_warehouse_stocks_future_validate_required_params(self, commodity, start_date, end_date):
        """
        校验仓单数据必填参数
        :param commodity: str--必填，期货合约品种
        :param start_date: str--必填，开始日期
        :param end_date: str--必填，结束日期 (默认为策略当天日期的前一天)
        :return: None
        """

        params_dict = {
            "commodity": commodity,
            "start_date": start_date,
            "end_date": end_date
        }

        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)

    def get_warehouse_stocks_future_validate_type_str(self, commodity, start_date, end_date):
        """
        校验参数类型是否为str
        :param commodity: str--必填，期货合约品种
        :param start_date: str--必填，开始日期
        :param end_date: str--必填，结束日期 (默认为策略当天日期的前一天)
        :return: None
        """

        params_dict = {
            "commodity": commodity,
            "start_date": start_date,
            "end_date": end_date
        }

        for key, value in params_dict.items():
            self.general_validate_param_is_str(key, value)

    @staticmethod
    def get_warehouse_stocks_future_get_data(commodity):
        """
        获取get_basic_data数据
        :param commodity: 期货合约品种
        :return: 从对应数据库中获取的数据

        """

        # get_warehouse_stocks_future_data, db_session = self.connect_db(table_name, db_path)
        get_warehouse_stocks_future_data = pd.DataFrame()  # 测试，用了数据库信息后需要替换成上面的代码

        filtered_data = pd.DataFrame()
        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(commodity, str):
            filtered_data = get_warehouse_stocks_future_data.where(f"instrumentid='{commodity}'").toDF()
        elif isinstance(commodity, list):
            filtered_data = get_warehouse_stocks_future_data.where(f"instrumentid in {commodity}").toDF()

        # 关闭数据库连接
        # db_session.close()  # 用了数据库信息后，需要取消注释

        return filtered_data

    def get_warehouse_stocks_future_filter_data_by_date(self, start_date, end_date, data):
        """
        根据日期过滤get_basic_data数据
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param data: 数据

        :return: 过滤后的数据
        """

        start_date = self._get_warehouse_stocks_future_date_conversion(start_date)
        end_date = self._get_warehouse_stocks_future_date_conversion(end_date)

        # 根据转换后的日期过滤数据
        data = data[
            (data['date'] >= start_date) & (
                    data['date'] <= end_date)]

        return data

    def _get_warehouse_stocks_future_date_conversion(self, date_str):
        """
        将日期字符串转换成对应格式的日期数据
        :param date_str: 日期字符串
        :return: 转换后的日期数据
        """

        if isinstance(date_str, str):
            if self.general_validate_date_str_is_datetime_type(date_str):
                return self.general_date_str_to_datetime(date_str)
            if self.general_validate_date_str_is_date_type(date_str):
                return self.general_date_str_to_date(date_str).date()

        return date_str

    """ get_vwap 获取vwap成交量加权价格指标 """

    def get_vwap(self, order_book_ids=None, start_date=None, end_date=None, frequency='1d', is_batch=False,
                 batch_size=1000000):
        """
        获取vwap成交量加权价格指标
        :param order_book_ids: str OR str list--必填, 合约代码
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :param frequency: str--必填, 历史数据的频率
        :param is_batch: bool--非必填, 是否批量获取数据
        :param batch_size: int--非必填, 批量获取数据时，每次获取数据的条数
        :return: vwap成交量加权价格指标
        """

        """ 校验必填参数 """
        # 校验oder_book_ids, start_date, end_date, frequency 是否为必填参数
        self.get_vwap_validate_required_params(order_book_ids, start_date, end_date, frequency)

        # 校验order_book_ids是否为str OR str list
        self.get_vwap_validate_order_book_ids(order_book_ids)

        # 校验start_date, end_date是否为datetime 或 对应格式的字符串
        self.get_vwap_validate_date_type(start_date, end_date)

        # 校验frequency是否为str
        self.get_vwap_validate_frequency(frequency)

        """  获取数据 """
        # 根据frequency获取数据
        total_data, db_session = self.get_vwap_get_data(frequency, order_book_ids, start_date, end_date)

        if is_batch:  # 如果需要分批次处理数据
            for i in range(0, total_data.rows, batch_size):
                # 分批次从dolphindb获取数据，转换成dataframe（因为数据量过大时，将tables对象转换成dataframe比较耗时）
                data = total_data.limit([i, batch_size]).toDF()

                # 重命名字段
                data = self.rename_vwap_columns(data)

                # 使用 yield from 将数据添加到列表中
                yield from [data[["order_book_id", "date", "vwap_value"]]]

            # 关闭数据库连接
            db_session.close()
        else:  # 如果不需要分批次处理数据
            # 分批将dolphindb获取的数据转换成dataframe
            data = self._get_vwap_data_todf(total_data)

            ''' 数据处理 '''
            # 重命名字段
            data = self.rename_vwap_columns(data)

            yield data[["order_book_id", "date", "vwap_value"]]

            # 关闭数据库连接
            db_session.close()

    @staticmethod
    def _get_vwap_data_todf(data):
        """
        用于接收从数据库获取的数据，并分批处理，将其转换成dataframe格式的数据返回
        : params data: 从数据库获取的数据
        : return : 转换成dataframe格式后的数据
        """

        result = pd.DataFrame()
        if data.rows > 1000000:
            chunk_size, start = 1000000, 0
            while start < data.rows:
                limit_data = data.limit([start, chunk_size]).toDF()
                result = limit_data if result.empty else pd.concat([result, limit_data], ignore_index=True)
                start += chunk_size

            return result
        return data.toDF()

    def get_vwap_validate_required_params(self, order_book_ids, start_date, end_date, frequency):
        """
        校验必填参数
        :param order_book_ids: str OR str list--必填, 合约代码
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :param frequency: str--必填, 历史数据的频率
        :return: None
        """

        params_dict = {
            "order_book_ids": order_book_ids,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency
        }

        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)

    def get_vwap_validate_order_book_ids(self, order_book_ids):
        """
        校验order_book_ids参数类型是否为str OR str list
        :param order_book_ids: str OR str list--必填, 合约代码
        :return: None
        """

        self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")

    def get_vwap_validate_date_type(self, start_date, end_date):
        """
        校验start_date和end_date参数类型是否为datetime
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :return: None
        """

        self._get_vwap_validate_date_type(start_date, "start_date")
        self._get_vwap_validate_date_type(end_date, "end_date")

    def _get_vwap_validate_date_type(self, date_str, date_str_name):
        """
        校验date_str参数类型是否为datetime格式的字符串
        :param date_str: str, 日期
        :return: None
        """

        if isinstance(date_str, str) and not self.general_validate_date_str_is_datetime_type(date_str):
            raise ValueError(f"{date_str_name} type error, datetime.datetime type or can be converted to the type")
        if not isinstance(date_str, str) and not isinstance(date_str, datetime.datetime):
            raise ValueError(f"{date_str_name} type error, datetime.datetime type or can be converted to the type")

    def _get_vwap_date_conversion(self, date_str):
        """
        将日期字符串转换成对应格式的日期数据
        :param date_str: 日期字符串
        :return: 转换后的日期数据
        """

        if isinstance(date_str, str):
            if self.general_validate_date_str_is_datetime_type(date_str):
                return self.general_date_str_to_datetime(date_str)
            if self.general_validate_date_str_is_date_type(date_str):
                return self.general_date_str_to_date(date_str).date()

        return date_str

    def get_vwap_get_data(self, frequency, order_book_ids, start_date, end_date):
        """
        获取vwap数据
        :param frequency: 频率
        :param order_book_ids: 合约代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: vwap数据
        """

        vwap_dict = {
            "1m": {
                "table_name": vwap_min_db_table_name,
                "db_path": vwap_min_db_path
            },
            "1d": {
                "table_name": vwap_day_db_table_name,
                "db_path": vwap_day_db_path
            }
        }

        table_result = vwap_dict.get(frequency, (None, None))
        table_name = table_result["table_name"]
        db_path = table_result["db_path"]

        data, db_session = self._get_vwap_get_data(order_book_ids, table_name, db_path, start_date, end_date)

        return data, db_session

    @staticmethod
    def get_vwap_format_date(date_str):
        """将日期字符串格式化为 'YYYY.MM.DD HH:mm:ss' 格式。
        : params date_str: 日期字符串，例如 '2018-01-04 09:01:00'。
        : return ：
            格式化后的日期字符串，例如 '2018.01.04 09:01:00'。
        """
        if isinstance(date_str, str):
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y.%m.%d %H:%M:%S')
        return date_str.strftime('%Y.%m.%d %H:%M:%S')

    def _get_vwap_get_data(self, order_book_ids, table_name, db_path, start_date, end_date):
        """
        用于接收数据表以及数据库，获取数据
        : params order_book_ids: 合约代码
        : params table_name: 数据表路径
        : params db_path: 数据库路径
        : params start_date: 开始时间
        : params end_date: 结束时间

        : return limit_data: 从数据库获取并根据合约代码筛选后的数据
        """

        get_vwap_data, db_session = self.connect_db(table_name, db_path)

        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            limit_data = get_vwap_data.where(f"instrument_id='{order_book_ids}'")
        else:
            limit_data = get_vwap_data.where(f"instrument_id in {order_book_ids}")

        # 将日期转换成 DolphinDB 识别的日期格式，用于筛选数据
        format_start_date = self.get_vwap_format_date(start_date)
        format_end_date = self.get_vwap_format_date(end_date)

        # 根据日期对数据再次进行筛选，最大程度减轻数据库压力
        limit_data = limit_data.where(f"trade_time >= {format_start_date} and trade_time <= {format_end_date}").where(
            "metric='vwap'")

        return limit_data, db_session

    # 重命名字段名称
    @staticmethod
    def rename_vwap_columns(data):
        """
        此方法用于重命名字段名称
        :param data: 数据
        :return: 重命名后的数据

        """

        vwap_fields_dict = {
            "instrument_id": "order_book_id", "trade_time": "date", "value": "vwap_value"
        }

        rename_data = data.rename(columns=vwap_fields_dict)

        return rename_data

    def get_vwap_validate_frequency(self, frequency):
        """
        校验frequency参数类型是否为str格式的字符串
        :param frequency: str, 历史数据的频率
        :return: None
        """

        self.general_validate_param_is_str("frequency", frequency)

    """ get_twap 获取twap时间加权价格 """

    def get_twap(self, order_book_ids=None, start_date=None, end_date=None, frequency='1d', is_batch=False,
                 batch_size=1000000):
        """
        获取twap成交量加权价格指标
        :param order_book_ids: str OR str list--必填, 合约代码
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :param frequency: str--必填, 历史数据的频率
        :param is_batch: bool--选填, 是否批量获取数据
        :param batch_size: int--选填, 批量获取数据时每次获取的条数
        :return: twap成交量加权价格指标
        """

        """ 校验必填参数 """
        # 校验oder_book_ids, start_date, end_date, frequency 是否为必填参数
        self.get_twap_validate_required_params(order_book_ids, start_date, end_date, frequency)

        # 校验order_book_ids是否为str OR str list
        self.get_twap_validate_order_book_ids(order_book_ids)

        # 校验start_date, end_date是否为datetime 或 对应格式的字符串
        self.get_twap_validate_date_type(start_date, end_date)

        # 校验frequency是否为str
        self.get_twap_validate_frequency(frequency)

        """  获取数据 """
        # 根据frequency获取数据
        total_data, db_session = self.get_twap_get_data(frequency, order_book_ids, start_date, end_date)

        if is_batch:  # 如果需要分批次处理数据
            for i in range(0, total_data.rows, batch_size):
                # 分批次从dolphindb获取数据，转换成dataframe（因为数据量过大时，将tables对象转换成dataframe比较耗时）
                data = total_data.limit([i, batch_size]).toDF()

                # 重命名字段
                data = self.rename_twap_columns(data)

                # 使用 yield from 将数据添加到列表中
                yield from [data[["order_book_id", "date", "vwap_value"]]]

            # 关闭数据库连接
            db_session.close()
        else:  # 如果不需要分批次处理数据
            # 分批将dolphindb获取的数据转换成dataframe
            data = self._get_vwap_data_todf(total_data)

            ''' 数据处理 '''
            # 重命名字段
            data = self.rename_twap_columns(data)

            yield data[["order_book_id", "date", "vwap_value"]]

            # 关闭数据库连接
            db_session.close()

    # 重命名字段名称
    @staticmethod
    def rename_twap_columns(data):
        """
        此方法用于重命名字段名称
        :param data: 数据
        :return: 重命名后的数据

        """

        twap_fields_dict = {
            "instrument_id": "order_book_id", "trade_time": "date", "value": "vwap_value"
        }

        rename_data = data.rename(columns=twap_fields_dict)

        return rename_data

    def get_twap_validate_required_params(self, order_book_ids, start_date, end_date, frequency):
        """
        校验必填参数
        :param order_book_ids: str OR str list--必填, 合约代码
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :param frequency: str--必填, 历史数据的频率
        :return: None
        """

        params_dict = {
            "order_book_ids": order_book_ids,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency
        }

        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)

    def get_twap_validate_order_book_ids(self, order_book_ids):
        """
        校验order_book_ids参数类型是否为str OR str list
        :param order_book_ids: str OR str list--必填, 合约代码
        :return: None
        """

        self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")

    def get_twap_validate_date_type(self, start_date, end_date):
        """
        校验start_date和end_date参数类型是否为datetime
        :param start_date: datetime--必填,  开始日期
        :param end_date: datetime--必填, 结束日期
        :return: None
        """

        self._get_twap_validate_date_type(start_date, "start_date")
        self._get_twap_validate_date_type(end_date, "end_date")

    def _get_twap_validate_date_type(self, date_str, date_str_name):
        """
        校验date_str参数类型是否为datetime格式的字符串
        :param date_str: str, 日期
        :return: None
        """

        if isinstance(date_str, str) and not self.general_validate_date_str_is_datetime_type(date_str):
            raise ValueError(f"{date_str_name} type error, datetime.datetime type or can be converted to the type")
        if not isinstance(date_str, str) and not isinstance(date_str, datetime.datetime):
            raise ValueError(f"{date_str_name} type error, datetime.datetime type or can be converted to the type")

    def get_twap_get_data(self, frequency, order_book_ids, start_date, end_date):
        """
        获取twap数据
        :param frequency: 频率
        :param order_book_ids: 合约代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: twap数据
        """

        twap_dict = {
            "1m": {
                "table_name": twap_min_db_table_name,
                "db_path": twap_min_db_path
            },
            "1d": {
                "table_name": twap_day_db_table_name,
                "db_path": twap_day_db_path
            }
        }

        table_result = twap_dict.get(frequency, (None, None))
        table_name = table_result["table_name"]
        db_path = table_result["db_path"]

        data, db_session = self._get_twap_get_data(order_book_ids, table_name, db_path, start_date, end_date)

        return data, db_session

    def _get_twap_get_data(self, order_book_ids, table_name, db_path, start_date, end_date):
        """
        用于接收数据表以及数据库，获取数据
        : params order_book_ids: 合约代码
        : params table_name: 数据表路径
        : params db_path: 数据库路径
        : params start_date: 开始时间
        : params end_date: 结束时间

        : return limit_data: 从数据库获取并根据合约代码筛选后的数据
        """

        get_vwap_data, db_session = self.connect_db(table_name, db_path)

        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            limit_data = get_vwap_data.where(f"instrument_id='{order_book_ids}'")
        else:
            limit_data = get_vwap_data.where(f"instrument_id in {order_book_ids}")

        # 将日期转换成 DolphinDB 识别的日期格式，用于筛选数据
        format_start_date = self.get_twap_format_date(start_date)
        format_end_date = self.get_twap_format_date(end_date)

        # 根据日期对数据再次进行筛选，最大程度减轻数据库压力
        limit_data = limit_data.where(f"trade_time >= {format_start_date} and trade_time <= {format_end_date}").where(
            "metric='twap'")

        return limit_data, db_session

    @staticmethod
    def get_twap_format_date(date_str):
        """将日期字符串格式化为 'YYYY.MM.DD HH:mm:ss' 格式。
        : params date_str: 日期字符串，例如 '2018-01-04 09:01:00'。
        : return ：
            格式化后的日期字符串，例如 '2018.01.04 09:01:00'。
        """
        if isinstance(date_str, str):
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y.%m.%d %H:%M:%S')
        return date_str.strftime('%Y.%m.%d %H:%M:%S')

    def get_twap_validate_frequency(self, frequency):
        """
        校验frequency参数类型是否为str格式的字符串
        :param frequency: str, 历史数据的频率
        :return: None
        """

        self.general_validate_param_is_str("frequency", frequency)

    """ 实时分钟k线订阅接口封装 """

    def subscribe(self, subscribe_ip=None, subscribe_port=None, subscribe_user_id=None, subscribe_password=None,
                  is_batch=True, batch_size=10, order_book_ids=None, frequency=None, fields=None):
        """
        实时分钟k线订阅接口封装
        :param subscribe_ip: 订阅ip
        :param subscribe_port: 订阅端口
        :param subscribe_user_id: 订阅用户id
        :param subscribe_password: 订阅用户密码
        :param is_batch: 是否批量订阅
        :param batch_size: 订阅数据批次大小
        :param order_book_ids: 订阅合约代码 str or str list(必填)
        :param frequency: 订阅频率 str (必填)
        :param fields: 订阅字段 str or str list
        """

        """ 校验必填参数 """
        # 校验参数是否必填
        self.general_validate_params_required(order_book_ids, "order_book_ids")  # 校验order_book_ids
        self.general_validate_params_required(frequency, "frequency")  # 校验frequency

        # 校验参数类型
        self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")  # 校验order_book_ids是否为str或str list
        self.general_validate_param_is_str("frequency", frequency)  # 校验frequency是否为str

        s = ddb.session()
        s.connect(subscribe_ip, subscribe_port, subscribe_user_id, subscribe_password)

        s.enableStreaming()

        subscribe_fields = ["trading_day", "instrument_id", "trade_time", "open_price", "highest_price", "lowest_price", "close_price",
                            "volume", "turnover", "open_inretest"]

        def handler(lsts):
            """
            回调函数，用于对返回的结果进行各种处理
            """
            # 根据order_book_ids过滤数据
            if isinstance(order_book_ids, str):
                filter_df = lsts[lsts['instrument_id'] == order_book_ids]
            else:
                filter_df = lsts[lsts['instrument_id'].isin(order_book_ids)]

            filter_df = filter_df[subscribe_fields]  # 根据subscribe_fields进行字段筛选
            # 根据fields进行字段筛选
            if fields:
                filter_df = filter_df[fields] if isinstance(fields, list) else filter_df[[fields]]

            if not filter_df.empty:
                # 输出筛选后的数据
                print("\n", filter_df)  # 处理接收到的数据

        async def subscribe_data(is_subscribe, batch_num):
            if is_subscribe:
                s.subscribe(subscribe_ip, subscribe_port, handler, "MinKlineTable", actionName="first_action1",
                            offset=-1, batchSize=batch_num, throttle=0.1, msgAsTable=True)
            else:
                s.subscribe(subscribe_ip, subscribe_port, handler, "MinKlineTable", actionName="first_action1",
                            offset=-1)
            while True:
                await asyncio.sleep(1)

        async def subscribe_minute_kline(is_subscribe, batch_num):
            """
            实时订阅分钟k线接口封装
            """

            await (subscribe_data(is_subscribe, batch_num))

        try:
            asyncio.run(subscribe_minute_kline(is_batch, batch_size))
        except KeyboardInterrupt:
            print("Subscription stopped by user.")
            #  在实际应用中，这里可以添加更优雅的关闭连接和资源释放逻辑
            s.unsubscribe(subscribe_ip, subscribe_port, "MinKlineTable")

