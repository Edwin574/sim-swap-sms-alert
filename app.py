from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN")
SMS_API_ENDPOINT = os.getenv("SMS_API_ENDPOINT")



@app.route('/')
def index():
    return "Welcome to SMS sender!!"

@app.route("/listen_url", methods=['POST'])
def listen_url():
    '''The request should receive a listening URL and a phone number from the client POST request. The phone number should be used to send an SMS to the user.'''
    data = request.get_json()
    print(data,type(data))
    if not all(key in data for key in ["phone", "listen_url"]): 
        return jsonify({'error': 'Missing phone number or listen URL'}), 400
    
    url = str(data['listen_url'] )
    phone = str(data['phone'])
    
    # print(f"Phone: {phone}, URL: {url}")
    
    try:
        response = requests.get(url)
        response_data = response.json()
        #chack the swap status gotten from the Insights API
        if response_data.get('status') == 'Swapped':
            message = "Dear Customer, our system has detected suspicious activity on your account due to a recent SIM swap.Please Visit our nearest branch to verify your account.Thank you."
        elif response_data.get('status') == 'NoSwapDate':
            message = "Dear Customer, the account is safe. Thank you for choosing us."
        elif response_data.get('status') == 'InsufficientBalance':
            message="Dear Customer, your account has insufficient balance. Please top up your account to continue using our services. Thank you."
        else:
            return jsonify({'error': 'Invalid status code'}), 400
        
        return send_sms(token=API_TOKEN, message=message, phone=[phone])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_sms', methods=['POST'])
def send_sms(token, message, phone):
    '''Send SMS using the provided token, message, and phone number(s).'''
    payload = {
        "token": token,
        "message": message,
        "phone": phone
    }
    
    response = requests.post(SMS_API_ENDPOINT, json=payload)
    
    if response.status_code == 200:
        return jsonify({'success': True, "response": response.json()}), 200
    else:
        return jsonify({'success': False, "response": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
