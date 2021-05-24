import requests
import time
import json
from datetime import datetime, timedelta
from sys import argv


def delta_cnt(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def vk_request(params_upd, date, keyword):
    params = {'q': keyword, 'extended': 1, 'count': 200, 'start_time': date,
                     'end_time': dates_list[dates_list.index(date) + 1]}
    params.update(params_upd)
    response = requests.get('https://api.vk.com/method/newsfeed.search?', params=params)
    data = response.json()['response']['items']
    if len(data) > 0:
        data_to_write = json.dumps(data, indent=4, ensure_ascii=False)
        data_to_write = data_to_write[1:-2] + ','
        file.write(data_to_write)

        print(date)
        if len(data) == 200:
            new_from = response.json()['response']['next_from']
            return False, new_from
        else:
            return True, None
    else:
        time.sleep(0.5)
        return True, None


def news_search(keyword, list_of_dates):
    error_list = []
    for date in list_of_dates:
        try:
            bool_val, new_from = vk_request({'access_token': token, 'v': 5.95}, date, keyword)
            while bool_val is False:
                next_params = {'start_from': new_from, 'access_token': token, 'v': 5.95}
                bool_val, new_from = vk_request(next_params, date, keyword)
            continue
        except KeyError:
            time.sleep(1)
            continue
        except requests.Timeout or requests.exceptions.ConnectionError:
            error_list.append(date)
            time.sleep(1)
            continue
    return error_list


script, token = argv
dates_list = []
for result in delta_cnt(datetime(2011, 1, 1), datetime(2021, 1, 1), timedelta(days=1)):
    dates_list.append(result.timestamp())

key = "ТюмГУ"

file_name = 'vk_data_' + key + '.json'
with open(file_name, 'w', encoding='utf-8') as file:
    file.write('[\n')
    not_parsed_dates = news_search(key, dates_list[:-1])
    if len(not_parsed_dates) > 0:
        news_search(key, not_parsed_dates)
    file.write('\n]')
    file.close()
print(key, 'finished')
