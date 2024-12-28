import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta, timezone
import time
from ffquant.utils.Logger import stdout_log

__ALL__ = ['BaseIndicator']

class BaseIndicator(bt.Indicator):

    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.127:8288')}/signal/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('max_retries', 15),
        ('prefetch_size', 60),
        ('version', None),
        ('test', None),
        ('debug', None),
    )

    # cache the http response, because all indicators share the same response
    http_resp_cache = {}

    VERSION = 'V2024112911'
    TEST = False
    DEBUG = False

    def __init__(self):
        super(BaseIndicator, self).__init__()
        if self.p.test is None:
            self.p.test = self.TEST

        if self.p.debug is None:
            self.p.debug = self.DEBUG

        if self.p.test:
            self.p.url = self.p.url + "/test"

        if self.p.version is None:
            self.p.version = self.VERSION

        self.cache = {}

    def handle_api_resp(self, result):
        pass

    def determine_final_result(self):
        pass

    def get_internal_key(self):
        pass

    def next(self):
        # skip the starting empty bars
        if len(self.data.close.array) == 0:
            return
        cur_bar_local_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        cur_bar_local_time_str = cur_bar_local_time.strftime('%Y-%m-%d %H:%M:%S')

        is_live = self.data.islive()
        if is_live:
            if cur_bar_local_time_str not in self.cache:
                start_time = cur_bar_local_time
                start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                end_time = cur_bar_local_time + timedelta(minutes=1)
                # make sure to fetch data up to latest minute
                now = datetime.now().replace(second=0, microsecond=0).astimezone()
                if end_time < now:
                    end_time = now
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

                params = self.prepare_params(start_time_str, end_time_str)

                # fill with -inf
                minutes_delta = int((end_time.timestamp() - start_time.timestamp()) / 60)
                for i in range(minutes_delta):
                    self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = {'value': float('-inf'), 'create_time': 0}

                key = f"{self.p.symbol}_{start_time_str}_{end_time_str}"
                response = BaseIndicator.http_resp_cache.get(key, None)
                if response is None:
                    retry_count = 0
                    max_retry_count = self.p.max_retries
                    while retry_count < max_retry_count:
                        retry_count += 1
                        if self.p.debug:
                            stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

                        response = requests.get(self.p.url, params=params).json()
                        if self.p.debug:
                            stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

                        if response.get('code') != '200':
                            raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                        BaseIndicator.http_resp_cache[key] = response
                        if response.get('results') is not None and len(response['results']) > 0:
                            results = response['results']
                            results.sort(key=lambda x: x['openTime'])
                            for result in results:
                                self.handle_api_resp(result)
                            break
                        time.sleep(1)
                else:
                    if response.get('results') is not None and len(response['results']) > 0:
                        results = response['results']
                        results.sort(key=lambda x: x['openTime'])
                        if results[len(results) - 1].get(self.get_internal_key(), None) is None:
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, cached response's last result has no {self.get_internal_key()}, refresh data params: {params}, url: {self.p.url}")

                            time.sleep(1)
                            response = requests.get(self.p.url, params=params).json()
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, refresh data response: {response}")

                            if response.get('code') != '200':
                                raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                            BaseIndicator.http_resp_cache[key] = response
                            results = response['results']
                            results.sort(key=lambda x: x['openTime'])
                        else:
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, use cached response: {response}")

                        for result in results:
                            self.handle_api_resp(result)
            else:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {cur_bar_local_time_str}, hit cache: {self.cache[cur_bar_local_time_str]['value']}")
        else:
            if cur_bar_local_time_str not in self.cache:
                start_time = cur_bar_local_time
                start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                end_time = cur_bar_local_time + timedelta(minutes=self.p.prefetch_size)
                now = datetime.now().replace(second=0, microsecond=0).astimezone()
                if end_time > now:
                    end_time = now
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                params = self.prepare_params(start_time_str, end_time_str)

                # fill with -inf value in this range
                for i in range(0, int((end_time.timestamp() - start_time.timestamp()) / 60)):
                    self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = {'value': float('-inf'), 'create_time': 0}

                retry_count = 0
                max_retry_count = 1
                while retry_count < max_retry_count:
                    retry_count += 1
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

                    response = requests.get(self.p.url, params=params).json()
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

                    if response.get('code') != '200':
                        raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                    if response.get('results') is not None and len(response['results']) > 0:
                        results = response['results']
                        results.sort(key=lambda x: x['openTime'])
                        for result in results:
                            self.handle_api_resp(result)
                        break
                    time.sleep(1)
            else:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {cur_bar_local_time_str}, hit cache: {self.cache[cur_bar_local_time_str]['value']}")

        create_time = self.determine_final_result()

        # Replace -info with previous value. Starting value is zero. heartbeat info print
        for line_name in self.lines.getlinealiases():
            line = getattr(self.lines, line_name)
            if line[0] == float('-inf'):
                if len(self) > 1:
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, {cur_bar_local_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, line[0] inherited from line[-1]: {line[-1]}")
                    line[0] = line[-1]
                else:
                    line[0] = 0
            kline_local_time_str = cur_bar_local_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            create_local_time_str = datetime.fromtimestamp(create_time / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
            stdout_log(f"[INFO], {self.__class__.__name__}, kline time: {kline_local_time_str}, create_time: {create_local_time_str}, {line_name}: {line[0]}")

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'startTime' : start_time_str,
            'endTime' : end_time_str,
            'symbol' : self.p.symbol
        }

        return params