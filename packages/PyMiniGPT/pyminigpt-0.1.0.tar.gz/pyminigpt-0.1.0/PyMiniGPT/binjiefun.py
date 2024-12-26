import requests
def binjfun(user_input):
	headers = {
	    'authority': 'api.binjie.fun',
	    'accept': 'application/json, text/plain, */*',
	    'accept-language': 'en-US,en;q=0.9',
	    'content-type': 'application/json',
	    'dnt': '1',
	    'origin': 'https://chat18.aichatos96.com',
	    'referer': 'https://chat18.aichatos96.com/',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'cross-site',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	}
	
	params = {
	    'refer__1360': 'n4UxuD9AeeqiqD5DsD7mjqAKKiKqg00hBbD',
	}
	
	json_data = {
	    'prompt': user_input,
	    'userId': '#/chat/1735123753254',
	    'network': True,
	    'system': '',
	    'withoutContext': False,
	    'stream': False,
	}
	
	response = requests.post('https://api.binjie.fun/api/generateStream', params=params, headers=headers, json=json_data)
	result = response.content.decode('utf-8')
	return result
