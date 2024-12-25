from .quote_lib import QuoteLib
from .util import *
from .model import Reply
from .constants import *
import re
import datetime

ZipVersion = "2"


class ThsQuote:
    def __init__(self, quotelib):
        # 默认值是None，这样你可以传入一个 QuoteLib 实例
        if quotelib is None:
            self.quotelib = None
        elif isinstance(quotelib, QuoteLib):
            self.quotelib = quotelib
        else:
            raise TypeError("quotelib must be an instance of QuoteLib")

    def history_minute_time_data(self, code: str, date: str, fields: list = None):
        # 检查code的长度和前四位         # if len(code) != 10 or not (code.startswith('USHA') or code.startswith('USZA')):
        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        # 检查date的格式
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date must be in the format YYYYMMDD, e.g. 20241220.")

        instance = rand_instance(8)
        zipVersion = ZipVersion
        data_type = "1,10,13,19,40"
        market = code[:4]
        short_code = code[4:]
        req = f"id=207&instance={instance}&zipversion={zipVersion}&code={short_code}&market={market}&datatype={data_type}&date={date}"
        response = self.quotelib.query_data(req)
        if response == "":
            raise ValueError("No history data found.")

        reply = Reply(response)
        reply.convert_data()

        for entry in reply.data:
            if "time" in entry:  # 检查是否存在 "time" 键
                entry["time"] = ths_int2time(entry["time"])

        if fields:
            reply.data = [entry for entry in reply.data if all(field in entry for field in fields)]

        return reply

    def security_bars(self, code: str, start: int, end: int, fuquan: str, period: int):
        """
        获取证券条数据。

        :param code: 证券代码，必须是10个字符长，并以'USHA'或'USZA'开头。
        :param start: 开始时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param end: 结束时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param fuquan: 复权类型，必须是有效的复权值之一。
        :param period: 周期类型，必须是有效的周期值之一。
        """

        valid_fuquan = {Fuquanqian, Fuquanhou, FuquanNo}
        valid_periods = {Kline1m, Kline5m, Kline15m, Kline30m, Kline60m, Kline120m, KlineDay, KlineWeek, KlineMoon,
                         KlineQuarterly, KlineYear}

        if fuquan not in valid_fuquan:
            raise ValueError("Invalid fuquan.")

        if period not in valid_periods:
            raise ValueError("Invalid period.")

        mPeriod = {Kline1m, Kline5m, Kline15m, Kline30m, Kline60m, Kline120m}

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        instance = rand_instance(8)
        zipVersion = ZipVersion
        data_type = "1,7,8,9,11,13,19"
        market = code[:4]
        short_code = code[4:]
        req = f"id=210&instance={instance}&zipversion={zipVersion}&code={short_code}&market={market}&start={start}&end={end}&fuquan={fuquan}&datatype={data_type}&period={period}"
        response = self.quotelib.query_data(req)
        if response == "":
            raise ValueError("No history data found.")

        reply = Reply(response)
        reply.convert_data()

        if period in mPeriod:
            for entry in reply.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = ths_int2time(entry["time"])
        else:
            for entry in reply.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = datetime.datetime.strptime(str(entry["time"]), "%Y%m%d")

        return reply

    def get_block_data(self, block_id: int):
        """
        :param block_id: 板块代码，必须是有效的板块代码。
            0xC6A6 # 全部A股
            0xE # 沪深A股
            0xE # 沪深A股
            0x15 # 沪市A股
            0x1B # 深市A股
            0xC5E3 # 北京A股
            0xCFE4 # 创业板
            0xCBE5 # 科创板
            0xDBC6 # 风险警示
            0xDBC7 # 退市整理
            0xF026 # 行业和概念
            0xCE5E # 概念
            0xCE5F # 行业
            0xc4b5 # 行业二级 0xc4b5/0xcd1a/ 0xf04c
            0xc4b7 # 行业一二级 0xc4b7
            0xdffb # 地域
            0xD385 # 国内外重要指数
            0xDB5E # 股指期货
            0xCBBE # 科创板
            0xCBBD #blockDataFromBlockServer(
            0xD2 # 全部指数
            0xCE3F # 上证系列指数
            0xCE3E # 深证系列指数
            0xCE3D # 中证系列指数
            0xC2B0 # 北证系列指数
            0xCFF3 # ETF基金
            0x6 # 沪深封闭式基金
            0x4 # 沪封闭式基金
            0x5 # 深封闭式基金
            0xEF8C # LOF基金
            0xD811 # 分级基金
            0xD90C # T+0 基金
            0xC7B1 # 沪REITs
            0xC7A0 # 深REITs
            0xC89C # 沪深REITs
            0xCE14 # 可转债
            0xCE17 # 国债
            0xCE0B # 上证债券
            0xCE0A # 深证债券
            0xCE12 # 回购
            0xCE11 # 贴债
            0xCE16 # 地方债
            0xCE15 # 企业债
            0xD8D4 # 小公募
        :return: 包含成分股信息的 Reply 对象。
        """
        if not block_id:
            raise ValueError("Block Id must be provided.")

        instance = rand_instance(8)
        zipVersion = ZipVersion
        req = f"id=7&instance={instance}&zipversion={zipVersion}&sortbegin=0&sortcount=0&sortorder=D&sortid=55&blockid={block_id}&reqflag=blockserver"
        response = self.quotelib.query_data(req)
        if response == "":
            raise ValueError("No sector components data found.")

        reply = Reply(response)
        reply.convert_data()

        return reply
