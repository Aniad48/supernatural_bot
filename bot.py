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
    if total_updates < 0:
    	return None # ЗДЕСЬ ЕЩЁ НЕ ЯСНО
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
    response_text = ""
    json_data = get_updates_json(url + 'getUpdates' + get_string_offset())
    text_of_message = first_update(json_data)['message']['text'].encode('utf-8')
    print(text_of_message)
    if text_of_message == 'top 10':
        print("здесь должен быть запрос к серверу на топ 10")
        response = json.load(urllib2.urlopen('http://localhost:8080/news/')) # change url
        print(response)
        size = len(response)
        current = 0
        while current<size:
          nick_name = response[current]['name']
          level = response[current]['level']
          race = response[current]['race']
          response_text += nick_name + "  " + str(level) + "  " + race + "\n"
          current +=1
    elif text_of_message == 'news':
        print("здесь должен быть запрос к серверу на новости")
        response = json.load(urllib2.urlopen('http://localhost:8080/news/'))
        print(response)
        size = len(response)
        current = 0
        while current<size:
          timestamp = response[current]['timestamp']
          title = response[current]['title']
          text = response[current]['text']
          response_text += title + "\n" + text + "\n" + str(timestamp) + "\n"
          current +=1
    elif text_of_message == 'commands':
        response_text = "'top 10' for top 10 best players 'news' for news"
    else:
        response_text =" - it isn't command, type 'commands' for getting list of commands"

    send_mess(get_chat_id(first_update(json_data)), response_text)


def main():
    global offset
    try: 
      update_id = first_update(get_updates_json(url + 'getUpdates' + get_string_offset()))['update_id']
      print(update_id)
      offset = update_id
    except IndexError:
      print("empty")
      update_id = 1
    last_upd = last_update(get_updates_json(url + 'getUpdates' + get_string_offset()))
    last_update_id = 0
    if last_upd != None:
        last_update_id = last_upd['update_id'] 
    print(last_update_id)
    while update_id < last_update_id:
        work_with_update()
        update_id += 1
        offset += 1
        print (update_id, " ", last_update_id)
    while True:
    	print(offset)
    	last_upd = last_update(get_updates_json(url + 'getUpdates' + get_string_offset()))
    	last_update_id = 0
    	if last_upd != None:
          last_update_id = last_upd['update_id']
        if update_id == last_update_id:
            work_with_update()
            update_id += 1
            offset += 1
        sleep(1)


if __name__ == '__main__':
    main()
