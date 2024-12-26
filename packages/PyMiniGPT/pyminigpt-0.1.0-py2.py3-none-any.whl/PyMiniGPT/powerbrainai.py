import requests
def powerai(user_input):
	headers = {
	    'authority': 'powerbrainai.com',
	    'accept': '*/*',
	    'accept-language': 'en-US,en;q=0.9',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://powerbrainai.com',
	    'referer': 'https://powerbrainai.com/chat.html',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	}
	
	data = {
	    'message': user_input,
	    'messageCount': '1',
	}
	
	response = requests.post('https://powerbrainai.com/chat.php', headers=headers, data=data)
	data = response.json()
	result = data['response']
	return result
