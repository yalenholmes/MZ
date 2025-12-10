def listen():
	# microphone -> speech to text
	return text

def think(text):
	# text -> llm
	return response

def speak(response):
	# tts -> play audio
	pass

while True: 
	user_input = listen()
	answer = think(user_input)
	speak(answer)