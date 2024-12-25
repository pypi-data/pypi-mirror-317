#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-10-29 10:44:07
# @Author: Alan
# @File: yian.py
# @Describe: work for test

import os
import time
import random
import json
import jsonpath
import heapq
import schedule
from decimal import Decimal
from utils import *
from test_redis import add_redis_data, get_redis_data
# from apscheduler.schedulers.blocking import BlockingScheduler
# from cacheout import Cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, wait_fixed


config = CONFIG['redis']


def make_limit_order_diy(price, size, account_id, symbol_id, order_side, token):
    """
    https://yianpro.codekit.work/api/v1/private/spot/order/createOrder
    """
    url = '{}/api/v1/private/spot/order/createOrder'.format(
        CONFIG['NEW_URL'])
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'authToken={}'.format(token)
    }
    client_order_id = make_client_order_id()
    print('clientOrderId: {}'.format(client_order_id))
    try:
        data = {
            'price': '{}'.format(str(price)),
            'size': '{}'.format(size),
            'type': 'LIMIT',
            'timeInForce': 'GOOD_TIL_CANCEL',
            'reduceOnly': False,
            'isPositionTpsl': False,
            'accountId': '{}'.format(account_id),
            'symbolId': '{}'.format(symbol_id),
            'side': '{}'.format(order_side),
            'triggerPrice': '',
            'extraType': '',
            'extraDataJson': '',
            'symbol': 'AWK/USDT',
            'triggerPriceType': 'LAST_PRICE',
            'triggerPriceWithType': '0',
            'clientOrderId': '{}'.format(client_order_id),
            'isSetOpenTp': False,
            'isSetOpenSl': False,
            'orderSide': '{}'.format(order_side),
            'orderSource': 'WEB'
        }
        res = common_requests(url=url, header=headers,
                              data=json.dumps(data), http_method='POST')
        return res
    except Exception as e:
        print('create spot order异常: {}'.format(e))


def make_market_order_diy(size, account_id, symbol_id, order_side, token):
    """
    size, account_id, symbol_id, 'BUY'
    https://yianpro.codekit.work/api/v1/private/spot/order/createOrder
    """
    url = '{}/api/v1/private/spot/order/createOrder'.format(
        CONFIG['NEW_URL'])
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'authToken={}'.format(token)
    }
    client_order_id = make_client_order_id()
    print('clientOrderId: {}'.format(client_order_id))
    last_price = get_last_price(symbol_id)
    print('last price: {}'.format(last_price))
    try:
        data = {
            'price': '0',
            'size': '{}'.format(size),
            'type': 'MARKET',
            'timeInForce': 'GOOD_TIL_CANCEL',
            'reduceOnly': False,
            'isPositionTpsl': False,
            'accountId': '{}'.format(account_id),
            'symbolId': '{}'.format(symbol_id),
            'side': '{}'.format(order_side),
            'triggerPrice': '',
            'extraType': '',
            'extraDataJson': '',
            'triggerPriceType': 'LAST_PRICE',
            'triggerPriceWithType': '{}'.format(last_price),
            'clientOrderId': '{}'.format(client_order_id),
            'isSetOpenTp': False,
            'isSetOpenSl': False,
            'orderSide': '{}'.format(order_side),
            'orderSource': 'WEB'
        }
        if order_side == 'BUY':
            """
            price is top price
            1、get last price
            2、generate top price 101%
            """
            top_price = get_price_top(last_price)
            data['price'] = str(top_price)

        res = common_requests(url=url, header=headers,
                              data=json.dumps(data), http_method='POST')
        return res
    except Exception as e:
        print('create market order异常: {}'.format(e))


def make_market_sell(size, account_id='545970865217471061', symbol_id='90000006', token=CONFIG['ACCESS_TOKEN_ONE']):
    # size, symbol_id, order_side
    res = make_market_order_diy(size, account_id, symbol_id, 'SELL', token)
    return res


def make_market_buy(size, account_id='545970865217471061', symbol_id='90000006', token=CONFIG['ACCESS_TOKEN_ONE']):
    # size, symbol_id, order_side
    res = make_market_order_diy(size, account_id, symbol_id, 'BUY', token)
    return res


def make_sell(price, size, account_id='544972745536963037', symbol_id='90000006', token=CONFIG['ACCESS_TOKEN']):
    # price, size, account_id, symbol_id, order_side
    res = make_limit_order_diy(
        price, size, account_id, symbol_id, 'SELL', token)
    return res


def make_buy(price, size, account_id='544972745536963037', symbol_id='90000006', token=CONFIG['ACCESS_TOKEN']):
    # price, size, account_id, symbol_id, order_side
    res = make_limit_order_diy(
        price, size, account_id, symbol_id, 'BUY', token)
    return res


def sell_function(*args):
    # print('args: {}'.format(args))  # like ((5.586581, '0.94'),)
    return make_sell(args[0][0], args[0][1])


def buy_function(*args):
    return make_buy(args[0][0], args[0][1])


def make_limit_sell_order(symbol_id, num):
    data_list = []
    result_list = []
    # get last price
    last_price = get_last_price(symbol_id)
    print('last_price: {}'.format(last_price))
    if last_price > 0:
        # make sell price and size
        g_price_list = [greater(last_price, 0.01, 0.02) for _ in range(num)]
        size_list = [str(round(random.uniform(0, 2), 2)) for _ in range(num)]
        data_list = list(zip(g_price_list, size_list))
        # thread create sell order
        with ThreadPoolExecutor() as executor:
            res = executor.map(sell_function, data_list)
            for i in res:
                print(i)
                if i['code'] == 'SUCCESS' and i['data']:
                    # make order_id list
                    result_list.append(i['data']['orderId'])
                else:
                    print('make sell order error...')
        # make order_id with price list, write to cache like [(price, order_id),...]
        final_list = list(zip(g_price_list, result_list))
        for i in final_list:
            add_redis_data(config, get_str_full_price(i[0]), i[1])
        # for key, value in cache.items():
        #     print(str(key) + ':' + value)
        # if key == '1.3322':
        # print(value)
        # final_dict = dict(zip(result_list, g_price_list))
        # sorted_dict = dict(sorted(final_dict.items(), key=lambda x: x[1]))
        # print(sorted_dict)
        # num_min_order = find_nums_min_values_keys(
        #     sorted_dict)  # 是个orderid的list
        # print(num_min_order)
        # 撤单
        # res = cancel_order(num_min_order[0])
        # print(res)


def make_limit_buy_order(symbol_id, num):
    data_list = []
    result_list = []
    last_price = get_last_price(symbol_id)
    print('last_price: {}'.format(last_price))
    if last_price > 0:
        # make sell and buy price
        l_price_list = [lesser(last_price, 0.03, 0.01) for _ in range(num)]
        size_list = [str(round(random.uniform(0, 2), 2)) for _ in range(num)]
        data_list = list(zip(l_price_list, size_list))
        with ThreadPoolExecutor() as executor:
            res = executor.map(buy_function, data_list)
            for i in res:
                print(i)
                if i['code'] == 'SUCCESS' and i['data']:
                    result_list.append(i['data']['orderId'])
                else:
                    print('make buy order error...')
        final_list = list(zip(l_price_list, result_list))
        for i in final_list:
            add_redis_data(config, get_str_full_price(i[0]), i[1])
        # final_dict = dict(zip(result_list, l_price_list))
        # sorted_dict = dict(
        #     sorted(final_dict.items(), key=lambda x: x[1], reverse=True))
        # print(sorted_dict)
        # num_max_order = find_nums_max_values_keys(
        #     sorted_dict)  # 是个orderid的list
        # print(num_max_order)


def make_deal():
    """
    90000005
    """
    pass


def make_depth_intelligent(symbol_id):
    # 全部撤单
    # res = batch_cancel_order(symbol_id)
    # print(res)

    # depth
    num = 10
    my_depth = get_depth(symbol_id)
    print(my_depth)  # {'asks': 0, 'bids': 2}
    my_asks, my_bids = my_depth[0], my_depth[1]

    if len(my_asks) < num:
        # sell
        make_limit_sell_order(symbol_id, num-len(my_asks))
    elif len(my_asks) == num:
        # len equal 10
        # cancel last two order my_list[:4]
        asks_cancel_list = my_asks[:4]
        # print(asks_cancel_list)
        price_list = [i['price'] for i in asks_cancel_list]
        # print(price_list)
        order_id_list = [get_redis_data(config, i) for i in price_list]
        print('cancel order id: {}'.format(order_id_list))
        # cancel order
        for i in order_id_list:
            cancel_order(i)
        time.sleep(random.randrange(0, 10))
        # add the order
        make_limit_sell_order(symbol_id, 4)
    else:
        # len more then 10
        n = len(my_asks) - num
        asks_cancel_list = my_asks[-n:]
        price_list = [i['price'] for i in asks_cancel_list]
        order_id_list = [get_redis_data(config, i) for i in price_list]
        for i in order_id_list:
            cancel_order(i)
        time.sleep(random.randrange(1, 2))

    if len(my_bids) < num:
        # sell
        make_limit_buy_order(symbol_id, num-len(my_bids))
    elif len(my_bids) == num:
        # cancel last two order
        bids_cancel_list = my_bids[-4:]
        # print(bids_cancel_list)
        price_list = [i['price'] for i in bids_cancel_list]
        # print(price_list)
        order_id_list = [get_redis_data(config, i) for i in price_list]
        print('cancel order id: {}'.format(order_id_list))
        # cancel order
        for i in order_id_list:
            cancel_order(i)
        time.sleep(random.randrange(0, 10))
        # add the order
        make_limit_buy_order(symbol_id, 4)
    else:
        # len more then 10
        n = len(my_bids) - num
        bids_cancel_list = my_bids[-n:]
        price_list = [i['price'] for i in bids_cancel_list]
        order_id_list = [get_redis_data(config, i) for i in price_list]
        for i in order_id_list:
            cancel_order(i)
        time.sleep(random.randrange(1, 2))


def buy_by_market_job():
    """
    market buy in order to last price go up
    size, account_id='545970865217471061', symbol_id='90000006', token=CONFIG['ACCESS_TOKEN']
    """
    size = str(round(random.uniform(0, 2), 2))
    res = make_market_buy(size, account_id='545970865217471061',
                          symbol_id='90000006', token=CONFIG['ACCESS_TOKEN_ONE'])
    return res


def sell_by_market_job():
    """
    market sell in order to last price go down
    """
    size = str(round(random.uniform(0, 2), 2))
    res = make_market_sell(size, account_id='545970865217471061',
                           symbol_id='90000006', token=CONFIG['ACCESS_TOKEN_ONE'])
    return res


def get_account_asset(token=CONFIG['ACCESS_TOKEN']):
    """
    调用接口获取账户的USDT和JPS, 并存入redis
    返回用户account_id 方便查redis
    """
    res = get_account_spot_asset(token)
    final = [i for i in res[1] if i['coinId'] == 2 or i['coinId'] == 11]
    # print(final)
    # print('account_id: {}'.format(res[0]))
    add_redis_data(config, res[0], json.dumps(final))
    return res[0]


def get_order_list(token=CONFIG['ACCESS_TOKEN']):
    """
    https://yianpro.codekit.work/api/v1/private/spot/account/getAccountAsset
    return account_id, asset info
    """
    url = '{}/api/v1/private/spot/account/getAccountAsset'.format(
        CONFIG['NEW_URL'])
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'authToken={}'.format(token)
    }
    try:
        res = common_requests(url=url, header=headers)
        if res['code'] == 'SUCCESS' and res['data']['assetList']:
            return res['data']['account']['id'], res['data']['assetList']
    except Exception as e:
        print('get account spot asset异常: {}'.format(e))


@retry(wait=wait_fixed(5))  # 等待5秒重试,无限次重试
def scheduled_tasks():
    """
    # 定义定时任务
    # schedule.every(15).seconds.do(buy_by_market_job)
    # schedule.every(30).seconds.do(sell_by_market_job)
    """
    # random run function
    functions = {
        'buy': buy_by_market_job,
        'sell': sell_by_market_job
    }
    # random run a func
    random_function_name = random.choice(list(functions.keys()))
    print('this time use {}'.format(random_function_name))
    if random_function_name == 'buy':
        schedule.every(15).seconds.do(functions[random_function_name])
        schedule.every(30).seconds.do(sell_by_market_job)
    else:
        schedule.every(15).seconds.do(functions[random_function_name])
        schedule.every(30).seconds.do(buy_by_market_job)
    schedule.every(60).seconds.do(make_depth_intelligent, symbol_id='90000006')
    # 无限循环，并执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(random.randrange(1, 3))


def main():
    # make_depth_intelligent
    # sched = BlockingScheduler()  # 创建调度器
    # sched.add_job(work, 'interval', seconds=30, id='my_job_id')  # 间隔1秒调用job()
    # sched.start()
    # res = buy_by_market()
    # print(res)

    # 全部撤单
    # res = batch_cancel_order('90000006', token=CONFIG['ACCESS_TOKEN_ONE'])
    # print(res)

    # 单个撤单
    # res = get_depth('90000006')
    # print(res)

    # 获取account asset 写入redis
    # account_id = get_account_asset()
    # res = get_redis_data(config, account_id)
    # print(res)
    # print(type(json.loads(res)))

    # 定时任务
    # make_depth_intelligent('90000006')
    scheduled_tasks()

    # spot
    # res = get_spot_account_id(token=CONFIG['ACCESS_TOKEN_ONE'])
    # print('spot account id: {}'.format(res))
    # contract
    # res = get_contract_account_id()
    # print('contract account id: {}'.format(res))
    # wallet
    # res = get_wallet_account_id()
    # print('wallet account id: {}'.format(res))
    # client_order_id
    # my_client_order_id = make_client_order_id()
    # print(my_client_order_id)

    # make spot order
    # res = make_limit_order('545970865217471061')
    # print(res)

    # price, size, account_id, symbol_id, order_side
    # 545970865217471061 126
    # 544972745536963037 163
    # 买
    # res = make_limit_order_diy(
    #     '5.555686', '2', '544972745536963037', '90000006', 'SELL')
    # print(res)
    # make_buy('5.58232', '0.3455')

    # 卖
    # res = make_limit_order_diy(
    #     '5.555685', '2', '544972745536963037', '90000006', 'SELL')
    # print(res)
    # make_sell('5.555686', '2')

    # get last price
    # res = get_last_price('90000006')
    # print(res)  # str

    # make a just order
    # make_buy_order()
    # make_sell_order()

    # get depth
    # if jsonpath.jsonpath(json.loads(i), '$..adList'):
    # res = get_depth('90000006')
    # print(res)
    # my_asks = jsonpath.jsonpath(res, '$..asks')[0]
    # print(my_asks)
    # my_bids = jsonpath.jsonpath(res, '$..bids')[0]
    # print(my_bids)
    # print('####################################################')
    # my_asks.sort(key=lambda order: (order['price'], order['size']))
    # my_asks.sort(key=lambda order: (-float(order['price']), order['size']))
    # students.sort(key=lambda student: (-student['score'], student['age']))
    # print(my_asks)

    # make sell order
    # make_sell_order()

    # make buy order
    # make_buy_order()

    # batch_cancel
    # res = batch_cancel_order('90000006')
    # print(res)

    # market sell
    # res = make_market_sell('1')
    # print(res)

    # market buy
    # res = make_market_buy('1')
    # print(res)
    # work()


if __name__ == '__main__':
    main()
