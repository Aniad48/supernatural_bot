# -*- coding: utf-8 -*-
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import urllib
from time import sleep

token = '549722574:AAG4vmMiocWoIFg9SR5Kxtmr0fdOMDEYd_E'
url = "https://api.telegram.org/bot549722574:AAG4vmMiocWoIFg9SR5Kxtmr0fdOMDEYd_E/"
offset = 546320619


def get_updates_json(request):
    response = urllib2.urlopen(request)
    print(response)
    string = response.read().decode('utf-8')
    return json.loads(string)


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_string_offset():
    ofst = offset
    offset_string = "?offset=" + str(ofst)
    return offset_string

def first_update(data):
    results = data['result']
    total_updates = 0
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    # data for sending
    data = urllib.urlencode(params)
    #  HTTP POST
    request = urllib2.Request(url + 'sendMessage', data)
    response = urllib2.urlopen(request)
    html = response.read()
    return response

def work_with_update():
    response_text = "command was executing successful"
    json_data = get_updates_json(url + 'getUpdates' + get_string_offset())
    text_of_message = first_update(json_data)['message']['text'].encode('utf-8')
    if text_of_message == 'top 10':
        print("здесь должен быть запрос к серверу на топ 10")
        response = urllib2.urlopen('http://localhost:8080/') # change url
        print(response)
        response_text = response.read().decode('utf-8')
    elif text_of_message == 'news':
        print("здесь должен быть запрос к серверу на новости")
        response = urllib2.urlopen('http://localhost:8080/')
        print(response)
        response_text = response.read().decode('utf-8')
    elif text_of_message == 'commands':
        response_text = "'top 10' for top 10 best players 'news' for news"
    else:
        response_text = text_of_message + " - it isn't command, type 'commands' for getting list of commands"

    send_mess(get_chat_id(first_update(json_data)), response_text)


def main():
    global offset
    update_id = first_update(get_updates_json(url + 'getUpdates' + get_string_offset()))['update_id']
    print(update_id)
    offset = update_id
    last_update_id = last_update(get_updates_json(url + 'getUpdates' + get_string_offset()))['update_id']
    print(last_update_id)
    while update_id < last_update_id:
        work_with_update()
        update_id += 1
        offset += 1
        print (update_id, " ", last_update_id)
    while True:
        if update_id == last_update(get_updates_json(url + 'getUpdates' + get_string_offset()))['update_id']:
            work_with_update()
            update_id += 1
            offset += 1
        sleep(1)


if __name__ == '__main__':
    main()
