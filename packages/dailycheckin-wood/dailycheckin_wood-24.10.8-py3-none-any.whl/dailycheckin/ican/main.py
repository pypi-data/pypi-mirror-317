import json
import os
import logging
import requests
import urllib3
import random
import time
from datetime import datetime

from dailycheckin import CheckIn

urllib3.disable_warnings()

logging.basicConfig(level=logging.DEBUG)
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.DEBUG)


class ICan(CheckIn):
    name = "ICAN"

    def __init__(self, check_item: dict):
        self.check_item = check_item
        self.base_url = 'https://ican.sinocare.com'

    def update_token(self, refresh_token):
        url = f'{self.base_url}/api/sino-archives/v1/user/info'
        headers = {'Sino-Auth': refresh_token}
        response = requests.get(url=url, headers=headers, verify=False)  # 禁用 SSL 证书验证
        print(response.status_code)
        status_code = response.status_code
        return status_code

    def sign(self, access_token):
        pass

    def record_uric_acid(self, access_token):
        pass
        msg = []
        url = f'{self.base_url}/api/sino-health/ua/save?familyUserId='
        headers = {'Sino-Auth': access_token, 'Content-Type': 'application/json'}
        for i in range(0, 3):
            data = {
                "mode": 1,
                "deviceSn": "",
                "detectionIndicatorsId": "2",
                "detectionChannel": "1",
                "detectionUnit": "μmol/L",
                "detectionTime": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                "detectionWay": 1,
                "remark": "",
                "sex": 1,
                "result": {
                    "ua": {
                        "val": random.randrange(260, 450),
                        "unit": "μmol/L",
                        "sex": 1
                    }
                }
            }
            response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False)

            if response.status_code != 200:
                return [{"name": "ICAN", "value": f"第{i}次记录尿酸失败"}]

            msg.append({"name": f"ICAN 第{i}次记录尿酸", "value": "成功"})
            time.sleep(2)
        return msg

    def record_diet(self, access_token):
        headers = {'Sino-Auth': access_token, 'Content-Type': 'application/json'}
        food_url = f'{self.base_url}/api/sino-knowledge/v1/food-items-info/page-app'
        diet_url = f'{self.base_url}/api/sino-health/v1/diet-record/save-or-update'
        data = {"current": 1, "size": 10, "isHot": 1}
        response = requests.post(url=food_url, headers=headers, data=json.dumps(data), verify=False)
        if response.status_code != 200:
            return [{"name": "ICAN", "value": "获取食物列表失败"}]

        msg = []
        response_data = json.loads(response.text)
        print(type(response_data))
        for i in range(0, 4):
            random_number = random.randrange(0, 9)
            foods = response_data["data"]["records"]
            data = {
                "uploadType": "0",
                "platformType": 1,
                "dietTypeName": "晚餐",
                "dietTime": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                "dietType": 5,
                "dataSource": 1,
                "remark": "",
                "isSocial": 0,
                "messageContent": "",
                "energyIntake": 16,
                "carbohydrate": 2,
                "fat": 0,
                "protein": 0,
                "detailReqList": [
                    {
                        "dietProjectId": foods[random_number]["id"],
                        "dietProjectName": foods[random_number]["dietName"],
                        "dietRecordEnergy": random.randrange(100, 800),
                        "dietEnergyIntake": 2,
                        "dietRecordNum": 16,
                        "carbohydrate": 2,
                        "fat": 0,
                        "protein": 0,
                        "dietUnit": "克",
                        "uploadType": "0",
                        "photoUrl": foods[random_number]["dietPictures"],
                        "type": 2
                    }
                ]
            }
            response = requests.post(url=diet_url, headers=headers, data=json.dumps(data), verify=False)

            if response.status_code != 200:
                return [{"name": "ICAN", "value": f"第{i}次记录饮食失败"}]

            msg.append({"name": f"ICAN 第{i}次记录饮食", "value": "成功"})
            time.sleep(2)
        return msg

    def main(self):
        refresh_token = self.check_item.get("Sino-Auth")
        status_code = self.update_token(refresh_token)
        if status_code != 200:
            return [{"name": "ICAN", "value": "token 过期"}]
        # msg = self.sign(refresh_token)
        # msg = self.record_diet(refresh_token)
        # msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        msg = self.record_uric_acid(refresh_token)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"),
            encoding="utf-8",
    ) as f:
        datas = json.loads(f.read())
    _check_item = datas.get("ICAN", [])[0]
    print(ICan(check_item=_check_item).main())
