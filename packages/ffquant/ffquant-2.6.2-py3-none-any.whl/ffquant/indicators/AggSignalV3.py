from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz
from ffquant.utils.Logger import stdout_log

__ALL__ = ['AggSignalV3']

class AggSignalV3(BaseIndicator):
    (BEARISH_WITH_LARGE_PULL_BACK,
     BEARISH_WITH_SMALL_PULL_BACK,
     INVERSE_TO_BEARISH,
     CONT_BEARISH,
     FLUCT_BEARISH,
     NA,
     FLUCT_BULLISH,
     CONT_BULLISH,
     INVERSE_TO_BULLISH,
     BULLISH_WITH_SMALL_PULL_BACK,
     BULLISH_WITH_LARGE_PULL_BACK) = (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5)

    lines = ('agg_sig',)

    def __init__(self):
        super(AggSignalV3, self).__init__()
        self.addminperiod(1)

    def handle_api_resp(self, item):
        internal_key = self.get_internal_key()
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        if item.get(internal_key, None) is not None and item[internal_key] == 'BEARISH_WITH_LARGE_PULL_BACK':
            self.cache[result_time_str]['value'] = self.BEARISH_WITH_LARGE_PULL_BACK
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'BEARISH_WITH_SMALL_PULL_BACK':
            self.cache[result_time_str]['value'] = self.BEARISH_WITH_SMALL_PULL_BACK
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'INVERSE_TO_BEARISH':
            self.cache[result_time_str]['value'] = self.INVERSE_TO_BEARISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'CONT_BEARISH':
            self.cache[result_time_str]['value'] = self.CONT_BEARISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'FLUCT_BEARISH':
            self.cache[result_time_str]['value'] = self.FLUCT_BEARISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'FLUCT_BULLISH':
            self.cache[result_time_str]['value'] = self.FLUCT_BULLISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'CONT_BULLISH':
            self.cache[result_time_str]['value'] = self.CONT_BULLISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'INVERSE_TO_BULLISH':
            self.cache[result_time_str]['value'] = self.INVERSE_TO_BULLISH
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'BULLISH_WITH_SMALL_PULL_BACK':
            self.cache[result_time_str]['value'] = self.BULLISH_WITH_SMALL_PULL_BACK
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'BULLISH_WITH_LARGE_PULL_BACK':
            self.cache[result_time_str]['value'] = self.BULLISH_WITH_LARGE_PULL_BACK
            self.cache[result_time_str]['create_time'] = item['createTime']
        elif item.get(internal_key, None) is not None and item[internal_key] == 'NA':
            self.cache[result_time_str]['value'] = self.NA
            self.cache[result_time_str]['create_time'] = item['createTime']

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, result_time_str: {result_time_str}, {internal_key}: {item.get(internal_key, None)}")

    def determine_final_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        self.lines.agg_sig[0] = self.cache[current_bar_time_str]['value']

        return self.cache[current_bar_time_str]['create_time']

    def get_internal_key(self):
        return 'TYPE_AGG_SIGNAL_V3' if self.p.version is None else f'TYPE_AGG_SIGNAL_V3_{str(self.p.version).upper()}'