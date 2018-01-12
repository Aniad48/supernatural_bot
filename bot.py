try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import urllib
from time import sleep

token = '549722574:AAG4vmMiocWoIFg9SR5Kxtmr0fdOMDEYd_E'
url = "https://api.telegram.org/bot549722574:AAG4vmMiocWoIFg9SR5Kxtmr0fdOMDEYd_E/"


def get_updates_json(request):  
	response = urllib2.urlopen(request + 'getUpdates')
	print(response)
	string = response.read().decode('utf-8')
	return json.loads(string)


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
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

def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
           json_data = get_updates_json(url)
           send_mess(get_chat_id(last_update(json_data)), 'test')
           update_id += 1
        sleep(1)       

if __name__ == '__main__':  
    main()