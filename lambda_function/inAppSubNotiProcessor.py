import json
import urllib3
import base64
import jwt

http = urllib3.PoolManager()
api_key = '3eaa561a-2adf-4040-9f0d-db31bfa86d96'
dev_url = 'http://1.232.94.157:9080/services/inapp/api/subscription/verify/noti'
stg_url = 'https://api.stage.dayup.co.kr/services/inapp/api/subscription/verify/noti'
prod_url = 'https://api.dayup.co.kr/services/inapp/api/subscription/verify/noti'

def lambda_handler(event, context):
    print('event',event)
    message = event.get('message')
    signedPayload = event.get('signedPayload')
    data = None
    url = None

    # noti
    if message is not None and message.get('data') is not None:
        print('noti message data:',message.get('data'))
        decoded_data = base64.b64decode(message.get('data')).decode('utf-8')
        decoded_json = json.loads(decoded_data)
        print('decoded_json:',decoded_json)
        subscription_notification = decoded_json.get('subscriptionNotification')
        subscriptionId = subscription_notification.get('subscriptionId')
        print('subscription_notification:',subscription_notification)
        print('subscriptionId:',subscriptionId)

        if subscriptionId is not None:
            if subscriptionId == 'subs_test_1' or subscriptionId == 'subs_test_2':
                url = dev_url
            elif subscriptionId == 'subs_test_3' or subscriptionId == 'subs_test_4':
                url = stg_url
            elif subscriptionId == 'kr.co.dayup.monthly' or subscriptionId == 'kr.co.dayup.yearly':
                url = prod_url
            print('call url',url)

            data = {
                "message": message['data'],
                "platform": 'aos'
            }

            # apple noti
    if signedPayload is not None:
        print('apple message', signedPayload)
        payload = jwt.decode(signedPayload, options={"verify_signature": False})
        if payload['data']['bundleId'] == 'kr.co.dayupcorp.dayup':
            print('prod')
            url = prod_url
        elif payload['data']['bundleId'] == 'kr.co.dayupcorp.dayupstage':
            print('stage')
            url = stg_url
        elif payload['data']['bundleId'] == 'kr.co.dayupcorp.dayupdev':
            print('dev')
            url = dev_url

        data = {
            "message": signedPayload,
            "platform": 'ios'
        }


    if data is not None:
        # 인앱 영수증 검증 호출
        try:
            response = http.request(
                'POST',
                url,
                body=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': api_key
                }
            )

            if response.status == 200:
                print('요청 성공')
                if response.data.decode('utf-8') == None:
                    print('응답 실패',response.data.decode('utf-8'))
                    return {
                        'statusCode': 500
                    }

                print('응답 성공',response.data.decode('utf-8'))
                print('응답 성공',response)
                return {
                    'statusCode': 200
                }
            else:
                print('요청 실패')
                print('응답 코드:', response.status)
                return {
                    'statusCode': response.status
                }
        except urllib3.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")

        except urllib3.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")

        except urllib3.exceptions.TimeoutError as e:
            print(f"Timeout error occurred: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")



