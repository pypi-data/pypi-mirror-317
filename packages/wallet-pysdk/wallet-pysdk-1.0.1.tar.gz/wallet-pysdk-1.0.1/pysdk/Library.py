import time
import json
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
import base64

class Library:
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.config = {
            "app_id": "",                 # 商户号（后台获取）
            "host": "https://xxx.com/",   # API接口域名，/结尾
            "version": "1.0",             # 版本号
            "time": "",                   # 时间戳（秒）
            "key_version": "",            # 默认为空，risk - 风控、query - 查询
            "lang": "cn",                 # 默认为cn，仅支持，cn - 中文、en - 英文
            # 自己的私钥，对应公钥需要绑定至商户后台
            "private_key": "",
            # 商户的公钥，用于响应数据验签
            "platform_public_key": ""
        }

        self.config.update(config)

        self.host = self.config.get("host", "")
        self.private_key = self.config.get("private_key", "")
        self.platform_public_key = self.config.get("platform_public_key", "")

        # 默认时间戳
        if not self.config["time"]:
            self.config["time"] = str(int(time.time()))

        # 从config中去除无关字段
        del self.config["host"]
        del self.config["private_key"]
        del self.config["platform_public_key"]

    def get_sign_string(self, data):
        """
        获取签名字符串
        """
        if 'sign' in data:
            del data['sign']
        sorted_data = sorted(data.items())
        pairs = []
        for k, v in sorted_data:
            if isinstance(v, dict):
                v = self.array_to_string(v)
            pairs.append(f"{k}={v}")
        return "&".join(pairs)

    def array_to_string(self, data):
        """
        将数组或字典转换为字符串
        """
        if isinstance(data, dict):
            return "".join(self.array_to_string(v) for v in data.values())
        elif isinstance(data, list):
            return "".join(self.array_to_string(v) for v in data)
        else:
            return str(data)

    def encryption(self, data):
        """
        使用私钥对数据进行签名
        """
        try:
            # 获取待签名字符串
            sign_string = self.get_sign_string(data)
            private_key = RSA.import_key(self.private_key)
            hash_obj = MD5.new(sign_string.encode('utf-8'))
            signature = base64.b64encode(pkcs1_15.new(private_key).sign(hash_obj)).decode('utf-8')
            return signature
        except Exception as e:
            print(f"Error during encryption: {e}")
            return None

    def check_signature(self, data):
        """
        使用公钥验证签名
        """
        try:
            # 获取签名
            sign = data.get('sign', '')
            if not sign:
                return False

            # 获取待签名字符串
            to_sign = self.get_sign_string(data)
            # 加载公钥
            public_key = RSA.import_key(self.platform_public_key)
            # 创建 SHA256 哈希对象
            hash_obj = MD5.new(to_sign.encode('utf-8'))
            # 验证签名
            pkcs1_15.new(public_key).verify(hash_obj, base64.b64decode(sign))
            return True
        except Exception as e:
            print(f"Error during signature verification: {e}")
            return False

    def _curl(self, url, data=None, method="POST", headers=None):
        """
        发送 HTTP 请求
        """
        method = method.upper()
        if headers is None:
            headers = {"Content-Type": "application/json;charset=utf-8"}

        try:
            if method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "GET":
                response = requests.get(url, params=data, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # 如果返回状态码不是 200，抛出异常
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"HTTP Request failed: {e}")

    def request(self, data, url):
        """发送接口请求并返回结果"""
        try:
            url = self.host + url
            data = {**self.config, **data}
            data['sign'] = self.encryption(data)  # 获取签名
            result = self._curl(url, data)
            return json.dumps(result)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise Exception('Request exception')

