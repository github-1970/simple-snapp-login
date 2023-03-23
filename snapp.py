import requests
import re

# get js url
print('[+] send request for get js url...')
res = requests.get('https://app.snapp.taxi/?utm_source=website&utm_medium=webapp-button&utm_campaign=body')
# <script defer="defer" src="/static/js/main.everything.js"></script>
src = re.search('<script defer="defer" src="(/static/js/main\..+?\.js)">', res.text).group(1)
jsUrl = 'https://app.snapp.taxi%s' % (src)
print('[+] js url: %s' % jsUrl)

# get client_id and client_secret
print('[+] send request for get client_id and client_secret from js file...')
res = requests.get(jsUrl)
# PWA_CLIENT_ID:"everything",PWA_CLIENT_SECRET:"everything"
clientId = re.search('PWA_CLIENT_ID:"(.+?)"', res.text).group(1)
clientSecret = re.search('PWA_CLIENT_SECRET:"(.+?)"', res.text).group(1)
print('[+] client_id: %s' % (clientId))
print('[+] client_secret: %s' % (clientSecret))

# get phone number
cellphone = input('[+] give me phone number (without first 0): ')
cellphone = '+98%s' % (cellphone)

# get otp code
print('[+] send request for get otp code...')
data = {'cellphone':cellphone}
res = requests.post('https://app.snapp.taxi/api/api-passenger-oauth/v2/otp', json=data)
print('[+] status: %s' % (res.json()['status']))
otpCode = input('[+] give me snapp otp code: ')

# get authorization token
print('[+] send request for get authorization token...')
data = {"grant_type":"sms_v2","client_id":clientId,"client_secret":clientSecret,"cellphone":cellphone,"token":otpCode}
res = requests.post('https://app.snapp.taxi/api/api-passenger-oauth/v2/auth', json=data)
authorizationToken = res.json()['access_token']
fullname = res.json()['fullname']
print('[+] authorization token received: %s' % (authorizationToken))

# get balance
print('[+] send request for get balance...')
res = requests.post('https://app.snapp.taxi/api/api-base/v2/passenger/balance', headers={'Authorization':'Bearer %s' % (authorizationToken)})
print('[+] %s balance: %s ' % (fullname, res.json()['data']['ap_balance']))
