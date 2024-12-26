import requests, re
def duckduck(user_input):
	history =[]
	cookies = {'dcm': '3'}
	headers = {
	    'authority': 'duckduckgo.com',
	    'accept': '*/*',
	    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
	    'cache-control': 'no-store',
	    'referer': 'https://duckduckgo.com/',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	    'x-vqd-accept': '1',
	}
	response = requests.get('https://duckduckgo.com/duckchat/v1/status', cookies=cookies, headers=headers)
	data = response.headers
	xq = data.get('x-vqd-4')
	if len(history) < 1:
	    pass
	elif len(history) >= 2:
	    user_input = f"Here’s the translation:\n\nBased on the history that occurred between you and me: {history}\n\nPlease answer or execute the following question: {user_input}\n\nif i asked you to say what i sayed little wille tel me only the answer but if ther are a thing need explain pleas explain it.\n\ndont explain too much just answer"
	cookies = {'dcm': '3'}
	headers = {
	    'authority': 'duckduckgo.com',
	    'accept': 'text/event-stream',
	    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
	    'content-type': 'application/json',
	    'origin': 'https://duckduckgo.com',
	    'referer': 'https://duckduckgo.com/',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	    'x-vqd-4': xq,
	}
	json_data = {
	    'model': 'gpt-4o-mini',
	    'messages': [{'role': 'user', 'content': user_input}],
	}
	response = requests.post('https://duckduckgo.com/duckchat/v1/chat', cookies=cookies, headers=headers, json=json_data)
	data = response.content.decode('utf-8')
	matches = re.findall(r'{"message":"(.*?)"', data)
	result = ''.join(matches)
	return result
