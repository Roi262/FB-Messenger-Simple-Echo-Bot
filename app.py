from flask import Flask, request
from pymessenger import Bot
import sys, os

app = Flask("My echo bot")

FB_ACCESS_TOKEN = "EAANSLNttakoBACts0kqZBgqxv04nk3JZBZCOL88HV4F4q2PbmF3ZBTQFtxk0r9Hh2bWZCDZCfGxMvmd0lPep3qUx8NZCQFPQZCXRWMDrCatGKN5ZCPJj1XHyLxwPIKGsMpvYr188tPByYJ5tDFHM8hF2UWXz5MAyZAnkPhbLI7u3Ok9vg3vLLzFv0pTFHF49dd11UZD"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET']) # '/' means homepage of our website
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:  # a messaging_event is essentially a webhook event

                # extract IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # Echo
                    response = messaging_text
                    bot.send_text_message(sender_id, response)

    return 'ok', 200

def log(message):
    print(message)
    sys.stdout.flush()




# @app.route('/', methods=['POST'])
# def webhook():
# 	print(request.data)
# 	data = request.get_json()

# 	if data['object'] == "page":
# 		entries = data['entry']

# 		for entry in entries:
# 			messaging = entry['messaging']

# 			for messaging_event in messaging:

# 				sender_id = messaging_event['sender']['id']
# 				recipient_id = messaging_event['recipient']['id']

# 				if messaging_event.get('message'):
# 					# HANDLE NORMAL MESSAGES HERE
# 					if messaging_event['message'].get('text'):
# 						# HANDLE TEXT MESSAGES
# 						query = messaging_event['message']['text']
# 						# ECHO THE RECEIVED MESSAGE
# 						bot.send_text_message(sender_id, query)
# 	return "ok", 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)
	# app.run(port=80, use_reloader = True)