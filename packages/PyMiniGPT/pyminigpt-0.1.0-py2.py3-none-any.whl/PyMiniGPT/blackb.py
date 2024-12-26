import requests
def blackbox(user_input):
	promt = '''برمجة سكربتات و تصليح سكربتات /Programming scripts and fixing scripts'''
	cookies = {
	    'render_session_affinity': '9cebaf83-1d14-40d4-9eb6-d232630f0f1c',
	    'sessionId': 'bd0e0753-cefc-4991-a051-ab8b2f6573eb',
	    'render_session_affinity': 'eb58e0e7-ca2d-4d4c-830b-d85a72043af6',
	    '__Host-authjs.csrf-token': 'f651506bd823ae2a7ed4bab61d97343a8c7d89869b205b05bf36fb5268bc6d72%7C505877e9793bb46e9f4d827a344ace0ecf0656c96a0be0d3b043775b120e8830',
	    '__Secure-authjs.callback-url': 'https%3A%2F%2Fwww.blackbox.ai',
	    'intercom-id-jlmqxicb': '49590a63-ff74-4ee4-862e-9bd10bc4de69',
	    'intercom-session-jlmqxicb': '',
	    'intercom-device-id-jlmqxicb': 'ac2be61f-7aad-464f-ac8d-108824020b89',
	}
	
	headers = {
	    'authority': 'www.blackbox.ai',
	    'accept': '*/*',
	    'accept-language': 'en-US,en;q=0.9',
	    'content-type': 'application/json',
	    'dnt': '1',
	    'origin': 'https://www.blackbox.ai',
	    'referer': 'https://www.blackbox.ai/',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	}
	
	json_data = {
	    'messages': [
	        {
	            'role': 'user',
	            'content': user_input,
	            'id': 'mHshAkm',
	        },
	    ],
	    'id': 'HWD7OWk',
	    'previewToken': None,
	    'userId': None,
	    'codeModelMode': True,
	    'agentMode': {},
	    'trendingAgentMode': {},
	    'isMicMode': False,
	    'userSystemPrompt': promt,
	    'maxTokens': 1024,
	    'playgroundTopP': None,
	    'playgroundTemperature': None,
	    'isChromeExt': False,
	    'githubToken': '',
	    'clickedAnswer2': False,
	    'clickedAnswer3': False,
	    'clickedForceWebSearch': False,
	    'visitFromDelta': False,
	    'mobileClient': False,
	    'userSelectedModel': None,
	    'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
	    'imageGenerationMode': False,
	    'webSearchModePrompt': False,
	    'deepSearchMode': False,
	    'domains': None,
	}
	
	response = requests.post('https://www.blackbox.ai/api/chat', cookies=cookies, headers=headers, json=json_data)
	result = response.text
	return result
	

