import json
import requests

def lambda_handler(event, context):
    print(event)
    try:
        body = json.loads(event['body'])
        print(body)

        # Extract the URL from the message
        message_part = body['message'].get('text')
        print("Message part : {}".format(message_part))

        # Shorten the URL using CleanURI API
        data = {'url': message_part}
        response = requests.post('https://cleanuri.com/api/v1/shorten', data=data) 
        short_url = response.json()['result_url']
        print("The short URL is: {}".format(short_url))

        # Send the short URL to the Telegram chat
        chat_id = body['message']['chat']['id']
        bot_token = "6426299192:AAEZSKI4UBLPhoIaHpSpVxRh2A7yflvCBnc"  
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': short_url
        }
        telegram_response = requests.post(url, json=payload) 

        # Check if the message was sent successfully
        if telegram_response.status_code == 200:
            return {"statusCode": 200}
        else:
            return {"statusCode": telegram_response.status_code}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"statusCode": 500}
