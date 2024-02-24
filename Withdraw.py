import time
import random

# 替换为您的API密钥
api_key = '17774cda-e093-4ba4-9468-f59536bab499'
secret_key = '7F655AB4C1C4CB6BB93E8112312352BF'
passphrase = 'Cooper.0412'

# 替换为您的提币信息
currency = 'CELO'
withdrawal_address = '0x21aDD8ec8020C81FACD5783479C8597522dE6a4D'
withdrawal_amount_min = 1  # 最小提币金额
withdrawal_amount_max = 1.5  # 最大提币金额

# 替换为您的延迟时间范围（以秒为单位）
delay_min = 1
delay_max = 20

# Okx API请求的基本URL
#base_url = 'https://www.okex.com'

# 生成签名
def generate_signature(timestamp, method, request_path, body=''):
    message = str(timestamp) + method + request_path + body
    signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

# 发送提币请求
def withdraw(api_key, secret_key, passphrase, currency, withdrawal_address, amount):
    timestamp = str(int(time.time() * 1000))
    method = 'POST'
    request_path = '/api/account/v3/withdrawal'
    body = {
        'currency': currency,
        'destination': '4',  # 4表示提币到外部地址
        'address': withdrawal_address,
        'amount': str(amount),
        'fee': '0',  # 可根据需要设置提币手续费
        'tradePwd': '',  # 可根据需要设置交易密码
    }
    body = json.dumps(body)
    signature = generate_signature(timestamp, method, request_path, body)
    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json',
    }
    url = base_url + request_path
    response = requests.post(url, headers=headers, data=body)
    return response.json()

# 生成随机金额
def generate_random_amount():
    return round(random.uniform(withdrawal_amount_min, withdrawal_amount_max), 8)

# 生成随机延迟时间
def generate_random_delay():
    return random.randint(delay_min, delay_max)

# 批量提币
def batch_withdraw(api_key, secret_key, passphrase, currency, withdrawal_address, num_of_withdrawals):
    for i in range(num_of_withdrawals):
        amount = generate_random_amount()
        delay = generate_random_delay()
        response = withdraw(api_key, secret_key, passphrase, currency, withdrawal_address, amount)
        print('Withdrawal', i+1, ':', response)
        time.sleep(delay)

# 替换为您想要的提币次数
num_of_withdrawals = 10

# 开始批量提币
batch_withdraw(api_key, secret_key, passphrase, currency, withdrawal_address, num_of_withdrawals)