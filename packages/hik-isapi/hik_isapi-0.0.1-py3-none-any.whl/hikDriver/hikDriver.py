import requests
import json
import xmltodict
from requests import ConnectTimeout, ConnectionError
from requests.auth import HTTPDigestAuth


class hikDriver:

    def __init__(self, ip='', username='admin', password='', isSSL=False) -> None:
        self.username = username
        self.password = password
        self.auth = HTTPDigestAuth(username, password)
        if isSSL:
            self.base_url = f'https://{ip}'
        else:
            self.base_url = f'http://{ip}'

    def auto_xml_json_to_dict(self, data) -> dict:

        if data is dict:
            return data
        try:
            return json.loads(data)  # 尝试解析 JSON 数据
        except ValueError:
            try:
                return xmltodict.parse(data, process_namespaces=False)
            except ValueError:
                return {}

    def get_device_info(self) -> dict:
        url = self.base_url + '/ISAPI/System/deviceInfo'
        try:
            r = requests.get(url, auth=self.auth, timeout=(3, 7))
            temp_dict = self.auto_xml_json_to_dict(r.text)
            return temp_dict

        except ConnectTimeout as e:
            # 连接超时
            return {'error': f'{e}'}

        except ConnectionError as e:
            # 由于目标计算机积极拒绝，无法连接
            return {'error': f'{e}'}

        except Exception as e:
            # 捕获未知错误
            return {'error': f'{e.__name__}'}

    def device_reboot(self) -> bool:
        url = self.base_url + '/ISAPI/System/reboot'

        try:
            r = requests.put(url, auth=self.auth, timeout=(3, 7))

            temp_xml_dict = self.auto_xml_json_to_dict(r.text)

            if temp_xml_dict['ResponseStatus']['statusString'] == 'OK' and temp_xml_dict['ResponseStatus'][
                'statusCode'] == '1':
                return True

            else:
                return False
        except TimeoutError:
            # 超时
            # 连接失败
            return False

        except Exception as e:
            # 捕获未知错误

            return False


