import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import ffquant.plot.dash_ports as dash_ports
import getpass
import pandas as pd
import numpy as np
import psutil
import socket
import os
from ffquant.utils.Logger import stdout_log
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import webbrowser
from ffquant.utils.dump_bt_data_utils import prepare_data_for_pickle, serialize_backtest_data
import time
import signal
import threading
import ffquant.utils.observer_data as observer_data
import sqlite3
from pathlib import Path

dash_last_access_time = 0
def get_self_ip():
    addrs = psutil.net_if_addrs()
    for _, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET and address.address.startswith('192.168.25.'):
                return address.address

def init_dash_app(strategy_name, port, username, use_local_dash_url=False):
    app = dash.Dash(
        name=strategy_name,
        requests_pathname_prefix=f"/user/{username}/proxy/{port}/" if not use_local_dash_url else None
    )
    app.title = strategy_name
    return app

def get_order_origin_stats(order_info_list: list, debug=False):
    order_origin_dict = dict()
    for order_item in order_info_list:
        if order_item['order_status'] != "Completed":
            continue

        order_origin = order_item['origin'] if order_item['origin'] is not None else "unknown"
        if order_origin not in order_origin_dict.keys():
            order_origin_dict[order_origin] = 1
        else:
            order_origin_dict[order_origin] += 1
    return order_origin_dict

def get_order_pnl_stats(order_info_list: list, position_list: list = [], debug=False):
    closed_trades = []

    for order_item in order_info_list:
        if order_item['order_status'] != "Completed":
            continue

        order_dt_str = order_item['datetime']
        order_price = order_item['execute_price']
        order_size = order_item['execute_size']
        order_side = order_item['order_type']
        order_origin = order_item['origin'] if order_item['origin'] is not None else "unknown"
        is_close_order = order_item['is_close_pos']
        if debug:
            stdout_log(f"order_dt_str: {order_dt_str}, order_price: {order_price}, order_size: {order_size}, order_side: {order_side}, order_origin: {order_origin}")
        
        if is_close_order:
            pos_dt_str = (datetime.strptime(order_dt_str, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')

            pos_price = None
            for pos_item in position_list:
                if pos_item['datetime'] == pos_dt_str:
                    pos_price = pos_item['price']
                    break

            if pos_price is not None:
                pnl = None
                pnl_return = None
                if order_side == "Buy":
                    pnl = (pos_price - order_price) * order_size
                    pnl_return = pnl / (abs(order_item['execute_size']) * pos_price)
                else:
                    pnl = (order_price - pos_price) * order_size
                    pnl_return = pnl / (abs(order_item['execute_size']) * pos_price)

                if pnl is not None:
                    closed_trades.append({
                        'datetime': order_dt_str,
                        'pnl': pnl,
                        'pnl_return': pnl_return,
                        'is_win': pnl > 0
                    })

    win_pnls = [trade['pnl'] for trade in closed_trades if trade['is_win']]
    loss_pnls = [trade['pnl'] for trade in closed_trades if not trade['is_win']]

    avg_win_pnl = sum(win_pnls) / len(win_pnls) if len(win_pnls) > 0 else 0
    avg_loss_pnl = abs(sum(loss_pnls) / len(loss_pnls)) if len(loss_pnls) > 0 else 0

    reward_risk_ratio = avg_win_pnl / avg_loss_pnl if avg_loss_pnl > 0 else float('inf')
    win_rate = len(win_pnls) / len(closed_trades) if len(closed_trades) > 0 else 0
    avg_return = sum([trade['pnl_return'] for trade in closed_trades]) / len(closed_trades) if len(closed_trades) > 0 else 0

    return reward_risk_ratio, win_rate, avg_return

def show_perf_graph(backtest_data, is_live=False, backtest_data_dir=None, task_id=None, debug=False):
    strategy_name = backtest_data["strategy_name"]
    use_local_dash_url = backtest_data["use_local_dash_url"]

    if backtest_data_dir is not None and not is_live and len(observer_data.kline) > 0:
        pkl_file_path = serialize_backtest_data(strategy_name,
                                riskfree_rate=backtest_data["riskfree_rate"],
                                use_local_dash_url=use_local_dash_url,
                                backtest_data_dir=backtest_data_dir,
                                debug=debug)
        if task_id is not None:
            update_task_field(task_id, "pkl_data_path", pkl_file_path)

    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(strategy_name, port, username, use_local_dash_url)

    init_table_callback(app, debug)
    init_graph_callback(app, debug)

    header = f"{strategy_name}(live), created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not is_live:
        dt_range = f"{backtest_data['portfolio'][0]['datetime']} - {backtest_data['portfolio'][-1]['datetime']}"
        header = f"{strategy_name}[{dt_range}], created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    interval = dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0,
        max_intervals=0
    )
    if is_live:
        interval = dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        )

    html_elements = []
    html_elements.append(html.H1(header, style={'textAlign': 'center'}))
    if is_live or len(observer_data.kline) > 0:
        html_elements.append(html.Button("Download Backtest Data", id="download-button", style={'position': 'absolute', 'top': '10px', 'right': '10px'}))
        html_elements.append(dcc.Download(id="download-backtest-data"))
        @app.callback(
            dash.dependencies.Output("download-backtest-data", "data"),
            [dash.dependencies.Input("download-button", "n_clicks")],
            prevent_initial_call=True
        )
        def download_backtest_data(n_clicks):
            if n_clicks:
                pkl_file_path = serialize_backtest_data(strategy_name, riskfree_rate=backtest_data["riskfree_rate"], use_local_dash_url=use_local_dash_url)
                return dcc.send_file(pkl_file_path)

    html_elements.append(dash_table.DataTable(
        id='metrics-table',
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Metrics'}, 'width': '50%'},
            {'if': {'column_id': 'Result'}, 'width': '50%'}
        ],
        style_table={
            'width': '50%',
            'maxWidth': '800px',
            'margin': '0 auto'
        },
    ))
    html_elements.append(dcc.Graph(id='buysell-graph'))
    html_elements.append(interval)
    html_elements.append(dcc.Store(id='backtest-data-store', data=backtest_data))

    app.layout = html.Div(html_elements)

    if not is_live:
        TIMEOUT_SECONDS = 15

        @app.server.before_request
        def update_last_access_time():
            global dash_last_access_time
            dash_last_access_time = time.time()

        def monitor_timeout():
            global dash_last_access_time
            dash_last_access_time = time.time()
            while True:
                time.sleep(5)
                if time.time() - dash_last_access_time > TIMEOUT_SECONDS:
                    stdout_log("No activity detected. Shutting down server...")
                    os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=monitor_timeout, daemon=True).start()

    server_url = f"https://{os.environ.get('FINTECHFF_JUPYTERHUB_SERVER_URL', 'strategy.sdqtrade.com')}"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}"

    if task_id is not None and not is_live:
        update_task_field(task_id, "dash_pid", str(os.getpid()))
        update_task_field(task_id, "dash_port", str(port))
        update_task_field(task_id, "last_dash_started_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        update_task_field(task_id, "exec_pid", 0)

        if len(backtest_data["portfolio"]) > 0:
            return_rate = backtest_data["portfolio"][-1]["portfolio"] / backtest_data["portfolio"][0]["portfolio"] - 1
            update_task_field(task_id, "return_rate", str(return_rate))

    if get_self_ip() != "192.168.25.144":
        webbrowser.open(f"http://{get_self_ip()}:{int(port)}")

    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True)

def init_table_callback(app, debug=False):
    @app.callback(
        Output('metrics-table', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_metrics_table(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(backtest_data["strategy_name"], backtest_data["riskfree_rate"], backtest_data["use_local_dash_url"])

        riskfree_rate = backtest_data["riskfree_rate"]
        portfolio = backtest_data["portfolio"]
        treturn = backtest_data["treturn"]
        order_info = backtest_data["order_info"]

        length = portfolio.__len__()
        if length > 0:
            days_in_year = 252
            minutes_in_day = 6.5 * 60
            total_return = portfolio[-1]['portfolio'] / portfolio[0]['portfolio'] - 1
            annual_return = "NaN"
            annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
            std_per_minute = np.std([item['timereturn'] for item in treturn])
            std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
            sharpe = "NaN"
            completed_order_num = len([item for item in order_info if item['order_status'] == "Completed"])
            limit_order_num = len([item for item in order_info if item['exec_type'] == "Limit"])
            completed_limit_order_num = len([item for item in order_info if item['exec_type'] == "Limit" and item['order_status'] == "Completed"])
            if std_annual != 0:
                sharpe = (annual_return - riskfree_rate) / std_annual

            long_positions = [item['position'] for item in backtest_data["position"] if item['position'] > 0]
            max_long_position = max(long_positions) if len(long_positions) > 0 else 0
            short_positions = [item['position'] for item in backtest_data["position"] if item['position'] < 0]
            max_short_position = abs(min(short_positions)) if len(short_positions) > 0 else 0

            reward_risk_ratio, win_rate, avg_return = get_order_pnl_stats(order_info, backtest_data["position"], debug=debug)
            if debug:
                stdout_log(f"reward_risk_ratio: {reward_risk_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

            order_origin_dict = get_order_origin_stats(order_info, debug=debug)

            metrics_data = {
                "Metrics": [
                    "总成交订单数量(买+卖)",
                    "限价单成交率",
                    "成交订单来源统计",
                    "区间总收益率",
                    "年化收益率",
                    "年化收益波动率",
                    "夏普比率",
                    "平均盈亏比",
                    "交易胜率",
                    "平仓单平均收益率",
                    "多头最大持仓量",
                    "空头最大持仓量"
                ],
                "Result": [
                    f"{completed_order_num}",
                    f"{(completed_limit_order_num/limit_order_num):.8%} ({completed_limit_order_num}/{limit_order_num})" if limit_order_num != 0 else "NaN",
                    f"{str(order_origin_dict)}",
                    f"{total_return:.8%}",
                    f"{annual_return:.8%}" if annual_return != "NaN" else annual_return,
                    f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                    f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                    f"{reward_risk_ratio:.8f}" if reward_risk_ratio != float('inf') else 'NaN',
                    f"{win_rate:.8%}",
                    f"{avg_return:.8%}",
                    f"{max_long_position}",
                    f"{max_short_position}"
                ]
            }
            return pd.DataFrame(metrics_data).to_dict('records')

def init_graph_callback(app, debug=False):
    @app.callback(
        Output('buysell-graph', 'figure'),
        Output('backtest-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_graph(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(backtest_data["strategy_name"], backtest_data["riskfree_rate"], backtest_data["use_local_dash_url"])

        # Fill K-line data
        kline_data = {
            "datetimes": [],
            "prices": []
        }
        for item in backtest_data["kline"]:
            kline_data['datetimes'].append(item["datetime"])
            kline_data['prices'].append(item["close"])

        figure = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,  # Share X-axis between the plots
            vertical_spacing=0.05,
            row_heights=[2, 1, 1, 1], # kline graph, indicator graph, position graph, drawdown graph
            specs=[
                [{"secondary_y": True}],  # The first row enables secondary y
                [{}],  # The second row
                [{}],  # The third row
                [{}],  # The fourth row
            ]
        )

        # Add price line to the first row
        figure.add_trace(
            go.Scatter(
                x=kline_data['datetimes'],
                y=kline_data['prices'],
                mode='lines',
                name='Price'
            ),
            row=1, col=1  # First row, first column
        )

        # purple: market order, orange: limit order, red: lost close pos order, green: won close pos order
        # black: limit order created, gray: limit order cancelled

        arrow_offset = 2

        # Handle buy points
        annotations = []
        for item in backtest_data["order_info"]:
            if item['order_status'] == "Completed" and item['order_type'] == "Buy":
                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "purple" or annotation['arrowcolor'] == "orange" or annotation['arrowcolor'] == "red" or annotation['arrowcolor'] == "green"):
                        current_count += 1
                close_price = None
                for kline in backtest_data["kline"]:
                    if kline['datetime'] == item['datetime']:
                        close_price = kline['close']
                        break

                last_pos = None
                for i in range(0, len(backtest_data["position"])):
                    if backtest_data["position"][i]['datetime'] == item['datetime']:
                        if i > 0:
                            last_pos = backtest_data["position"][i - 1]
                        else:
                            last_pos = backtest_data["position"][i]
                        break

                hovertext = f"{item['origin']}"
                realized_pnl = 0
                if item['is_close_pos']:
                    realized_pnl = (last_pos['price'] - item['execute_price']) * item['execute_size']
                    hovertext = f"{hovertext}, 平空, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 后仓位: {item['position_after']}, 盈利: {round(realized_pnl, 2)}, 原因: {item['message']}"
                else:
                    hovertext = f"{hovertext}, 开多, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 后仓位: {item['position_after']}, 原因: {item['message']}"

                arrowcolor = ""
                if item['is_close_pos']:
                    if realized_pnl >= 0:
                        arrowcolor = "green"
                    else:
                        arrowcolor = "red"
                elif item['exec_type'] == "Market":
                    arrowcolor = "purple"
                else:
                    arrowcolor = "orange"
                annotations.append(
                    dict(
                        x=item['datetime'],
                        y=close_price - 10 * current_count - arrow_offset,
                        xref="x",
                        yref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowcolor=arrowcolor,
                        hovertext=hovertext,
                        ax=0,
                        ay=40
                    )
                )

        # Handle sell points
        for item in backtest_data["order_info"]:
            if item['order_status'] == "Completed" and item['order_type'] == "Sell":
                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "purple" or annotation['arrowcolor'] == "orange" or annotation['arrowcolor'] == "red" or annotation['arrowcolor'] == "green"):
                        current_count += 1
                close_price = None
                for kline in backtest_data["kline"]:
                    if kline['datetime'] == item['datetime']:
                        close_price = kline['close']
                        break

                last_pos = None
                for i in range(0, len(backtest_data["position"])):
                    if backtest_data["position"][i]['datetime'] == item['datetime']:
                        if i > 0:
                            last_pos = backtest_data["position"][i - 1]
                        else:
                            last_pos = backtest_data["position"][i]
                        break

                hovertext = f"{item['origin']}"
                if item['is_close_pos']:
                    realized_pnl = (item['execute_price'] - last_pos['price']) * item['execute_size']
                    hovertext = f"{hovertext}, 平多, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 后仓位: {item['position_after']}, 盈利: {round(realized_pnl, 2)}, 原因: {item['message']}"
                else:
                    hovertext = f"{hovertext}, 开空, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 后仓位: {item['position_after']}, 原因: {item['message']}"

                arrowcolor = ""
                if item['is_close_pos']:
                    if realized_pnl >= 0:
                        arrowcolor = "green"
                    else:
                        arrowcolor = "red"
                elif item['exec_type'] == "Market":
                    arrowcolor = "purple"
                else:
                    arrowcolor = "orange"
                annotations.append(
                    dict(
                        x=item['datetime'],
                        y=close_price + 10 * current_count + arrow_offset,
                        xref="x",
                        yref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowcolor=arrowcolor,
                        hovertext=hovertext,
                        ax=0,       # X-axis shift for the arrow
                        ay=-40      # Y-axis shift for the arrow
                    )
                )

        # Handle Limit Order Creation
        for item in backtest_data["order_info"]:
            if item['order_status'] == "Submitted":
                close_price = None
                for kline in backtest_data["kline"]:
                    if kline['datetime'] == item['datetime']:
                        close_price = kline['close']
                        break

                hovertext = f"{item['origin']}"
                if item['is_close_pos']:
                    hovertext = f"{hovertext}, 平{'空' if item['order_type'] == 'Buy' else '多'}限创"
                else:
                    hovertext = f"{hovertext}, 开{'多' if item['order_type'] == 'Buy' else '空'}限创"
                hovertext = f"{hovertext}, 订单ID: {item['order_id']}, 价格: {item['create_price']}, 数量: {item['create_size']}, 原因: {item['message']}"

                annotations.append(
                    dict(
                        x=item['datetime'],
                        y=item['create_price'],
                        xref="x",
                        yref="y",
                        text="●",
                        showarrow=False,
                        font=dict(size=15, color="black"),
                        align="center",
                        hovertext=hovertext,
                    )
                )

        # Handle Limit Order Cancellation
        for item in backtest_data["order_info"]:
            if item['order_status'] == "Cancelled":
                close_price = None
                for kline in backtest_data["kline"]:
                    if kline['datetime'] == item['datetime']:
                        close_price = kline['close']
                        break

                hovertext = f"{item['origin']}"
                if item['is_close_pos']:
                    hovertext = f"{hovertext}, 平{'空' if item['order_type'] == 'Buy' else '多'}限消"
                else:
                    hovertext = f"{hovertext}, 开{'多' if item['order_type'] == 'Buy' else '空'}限消"
                hovertext = f"{hovertext}, 订单ID: {item['order_id']}, 价格: {item['create_price']}, 数量: {item['create_size']}, 原因: {item['message']}"

                annotations.append(
                    dict(
                        x=item['datetime'],
                        y=item['create_price'],
                        xref="x",
                        yref="y",
                        text="●",
                        showarrow=False,
                        font=dict(size=15, color="gray"),
                        align="center",
                        hovertext=hovertext,
                    )
                )

        # Add portfolio line to the last row
        portfolio_data = {
            "datetimes": [],
            "values": []
        }
        for item in backtest_data["portfolio"]:
            portfolio_data['datetimes'].append(item["datetime"])
            portfolio_data['values'].append(item["portfolio"])
        figure.add_trace(
            go.Scatter(
                x=portfolio_data['datetimes'],
                y=portfolio_data['values'],
                mode='lines',
                name='Portfolio'
            ),
            row=1, col=1,
            secondary_y=True
        )
        figure.update_yaxes(
            title_text='Portfolio',
            row=1, col=1,
            secondary_y=True
        )

        # Add indicator data to the second row
        ind_data = {
            "datetimes": kline_data["datetimes"]
        }
        keys = list(backtest_data["ind_data"].keys())
        for key in keys:
            if ind_data.get(key, None) is None:
                ind_data[key] = []

            for item in backtest_data["ind_data"][key]:
                ind_data[key].append(item)

            # Add indicator line to the second row
            figure.add_trace(
                go.Scatter(
                    x=ind_data['datetimes'],
                    y=ind_data[key],
                    mode='lines',
                    name=key
                ),
                row=2, col=1  # Second row, first column
            )

        # Update Y-axis title for each indicator subplot
        figure.update_yaxes(
            title_text="Indicators",
            row=2, col=1
        )

        # Add position line
        position_data = {
            "datetimes": kline_data["datetimes"],
            "values": []
        }
        for item in backtest_data["position"]:
            position_data['datetimes'].append(item["datetime"])
            position_data['values'].append(item["position"])
        figure.add_trace(
            go.Scatter(
                x=position_data['datetimes'],
                y=position_data['values'],
                mode='lines',
                name='Position'
            ),
            row=3, col=1  # Last row, first column
        )
        figure.update_yaxes(
            title_text='Position',
            row=3, col=1
        )

        # Add drawdown line to the last row
        drawdown_data = {
            "datetimes": [],
            "drawdowns": []
        }
        for item in backtest_data["drawdown"]:
            drawdown_data['datetimes'].append(item["datetime"])
            drawdown_data['drawdowns'].append(item["drawdown"])
        figure.add_trace(
            go.Scatter(
                x=drawdown_data['datetimes'],
                y=drawdown_data['drawdowns'],
                mode='lines',
                name='Drawdown'
            ),
            row=4, col=1  # Last row, first column
        )

        figure.update_yaxes(
            title_text='Drawdown',
            row=4, col=1
        )

        # Add annotations to the layout
        figure.update_layout(
            title='买卖点和账户价值(紫色箭头: 市价单成交, 橘黄色箭头: 限价单成交, 红色箭头: 亏损平仓单, 绿色箭头: 盈利平仓单, 黑色点: 限价单创建, 灰色点: 限价单取消)',
            xaxis=dict(title='Time', type='category'),
            yaxis=dict(title='Price'),
            height=400 * 6,
            annotations=annotations
        )

        return figure, backtest_data

def update_task_field(task_id, field_name, new_value):
    db_path = f"{Path.home()}/backtest_manage/apps/db.sqlite3"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_query = f"UPDATE tasks SET {field_name} = ? WHERE id = ?"

        cursor.execute(sql_query, (new_value, task_id))

        conn.commit()

        if cursor.rowcount > 0:
            stdout_log(f"Task with ID {task_id} updated successfully. {field_name}: {new_value}")
        else:
            stdout_log(f"No task found with ID {task_id}.")

    except sqlite3.Error as e:
        stdout_log(f"SQLite error: {e}")
    finally:
        conn.close()