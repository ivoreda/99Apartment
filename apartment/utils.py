import requests
import json

baseUrl = "https://user-service-production-7c6d.up.railway.app"

# baseUrl = "http://127.0.0.1:8001"

# paystack_callback_url = "https://99apartment-production.up.railway.app/apartments/verify-booking/verified=true/"
paystack_callback_url = "https://99apt-web.vercel.app/checkout/status"

class UserService:

    def get_user(self, **kwargs):
        url = f'{baseUrl}/user/get-user/'

        payload = {}
        token = kwargs.get('token')

        headers = {
        'Authorization': 'Bearer {token}'.format(token=token),
        'Accept': 'application/json'
        }


        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.content.decode('utf-8'))

class PaystackAPI:
    def __init__(self) -> None:
        self.secret_key = "sk_test_de60132ea93ebb81b5a505f3d2c23531525fc60e"
        self.paystackUrl = 'https://api.paystack.co'


    def initialise_transaction(self, **kwargs):
        url = f'{self.paystackUrl}/transaction/initialize'
        print("paystack url",url)

        customer_email = kwargs.get('email')
        amount = kwargs.get('amount') * 100
        str_amount = str(amount)
        payload = json.dumps({
            "email": customer_email,
            "amount": str_amount,
            "callback_url": paystack_callback_url
        })
        print("payload", payload)

        headers = {
        'Authorization': 'Bearer {secret_key}'.format(secret_key=self.secret_key),
        'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.content.decode('utf-8'))

    def verify_transaction(self, **kwargs):
        reference = kwargs.get('reference')
        url = f'{self.paystackUrl}/transaction/verify/{reference}'

        payload = {}

        headers = {
        'Authorization': 'Bearer {secret_key}'.format(secret_key=self.secret_key),
        'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.content.decode('utf-8'))

