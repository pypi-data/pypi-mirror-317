import requests
from loguru import logger

api_url = "http://139.196.154.85:54674"


def api_post(endpoint, json_data):
    try:
        # 发送POST请求
        response = requests.post(
            url=f"{api_url}{endpoint}",
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )

        # 检查响应状态
        if response.status_code == 200:
            response_json = response.json()
            if response_json['statusCode'] == 200:
                return response_json['data']
            logger.error(f"POST请求失败，响应数据: {response_json}")

        else:
            raise Exception(f"请求失败，状态码: {response.status_code},错误信息: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"发送请求时出错: {e}")


def api_get(endpoint, params=None):
    try:
        # 发送GET请求
        response = requests.get(
            url=f"{api_url}{endpoint}",
            params=params,
            headers={'Content-Type': 'application/json'}
        )
        # 检查响应状态
        if response.status_code == 200:
            response_json = response.json()
            if response_json['statusCode'] == 200:
                return response_json['data']
            logger.error(f"GET请求失败，响应数据: {response_json}")

        else:
            raise Exception(f"请求失败，状态码: {response.status_code},错误信息: {response.text}")


    except requests.exceptions.RequestException as e:
        print(f"发送请求时出错: {e}")
