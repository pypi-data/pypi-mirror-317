# -*- coding: utf-8 -*-
import io
import json
import os
import ssl
import sys
import time
import ast
from collections.abc import Callable

import xmltodict
import yaml
import threading
import socket
import hmac
import base64
import hashlib
from numbers import Number
from typing import List, Optional, Dict, Union
from urllib import parse
import urllib.request
from urllib.error import HTTPError, URLError

from loguru import logger

CONFIGURATIONS = "configurations"
NOTIFICATION_ID = "notificationId"
NAMESPACE_NAME = "namespaceName"
RELEASE_KEY = "releaseKey"
CONTENT = "content"

ConfigFormats = ['.json', '.yaml', '.yml', '.xml', '.txt']
ValueType = Union[str, bool, Number, Dict, List]
NamespaceConfigValueType = Union[Dict, List, str]

class ApolloClientReadRemoteError(Exception):
    pass

class ApolloClient(object):

    def __init__(self,
                 app_id: str='',
                 config_service_url: str='http://localhost:8080',
                 cluster: str='default',
                 secret: str='',
                 env: str='DEV',
                 namespaces: Optional[List[str]]=None,
                 change_listener: Optional[Callable]=None,
                 client_ip: Optional[str]=None,
                 log_level: str='INFO',
                 pull_timeout:int = 75,
                 cycle_time: int = 5,
                 ignore_ssl_verify: bool = False):
        """
        Apollo client
        :param app_id: application id of apollo project
        :param config_service_url: apollo config service url
        :param cluster: cluster name of apollo project
        :param secret: secret key from apollo project
        :param env: environment
        :param namespaces: namespaces need to be fetched
        :param change_listener: configuration change listener callback function, e.g. change_listener(action=[add|update|delete], namespace: str, key: str, value: Any)
        :param client_ip: client ip
        :param log_level: log level
        :param pull_timeout: pull timeout
        :param cycle_time: cycle time
        :param ignore_ssl_verify: bool
        """

        logger.remove()
        logger.add(sys.stdout, level=log_level)

        self.app_id = app_id
        self.cluster = cluster

        self.secret = secret or ''  # for None case
        self.env = env
        self.client_ip = client_ip or self.init_ip()
        self.config_service_url = config_service_url

        self.change_listener: Optional[Callable] = change_listener
        self.namespaces = namespaces or ['application']
        self.pull_timeout = pull_timeout
        self.cycle_time = cycle_time
        self.ignore_ssl_verify = ignore_ssl_verify
        self.stopping = False
        self._cache: Dict[str, NamespaceConfigValueType]  = {}
        self._notification_map: Dict[str, int]  = {}  # namespace -> notification id
        self._ns: Dict[str, str] = {}
        self.ns = {self._get_ns(namespace): namespace for namespace in self.namespaces}  # ns（no format） -> namespace (with namespace format)

        # Load all namespaces
        self._fetch_all()

        # 定时心跳拉取全量配置
        heartbeat = threading.Thread(target=self._heart_beat, daemon=True)
        heartbeat.start()

        # 热更新长轮询
        long_poll = threading.Thread(target=self._listener, daemon=True)
        long_poll.start()


    @staticmethod
    def init_ip():
        """
        Get local IP address
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 53))
                ip = s.getsockname()[0]
            finally:
                s.close()
        except socket.error as err:
            logger.error(f"Unable to get local IP: {err}")
            ip = "127.0.0.1"
        return ip

    def _get_ns(self, namespace: str):
        """
        Get namespace data from cache
        :param namespace: namespace without format suffix
        """
        if not self._ns.get(namespace):
            for fmt in ConfigFormats:
                if namespace.endswith(fmt):
                    self._ns[namespace] = namespace
                    break
            else:
                self._ns[namespace] = namespace
        return self._ns.get(namespace)

    def _http_request(self, url, timeout: int, headers: Optional[Dict]=None) -> (int, Optional[str]):
        """
        HTTP request
        :param url: request url
        :param timeout: request timeout
        :param headers: request headers
        """
        headers = headers or {}
        request = urllib.request.Request(url, headers=headers)

        context = ssl._create_unverified_context() if self.ignore_ssl_verify else ssl.create_default_context()
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                body = response.read().decode("utf-8")
                return response.code, body
        except HTTPError as e:
            if e.code != 304:
                logger.warning(str(f"HTTPError: {e}"))
            return e.code, None
        except Exception as e:
                logger.error(f"Failed to make a request to {url}: {e}")
                return 0, None



    def _handle_resp_body(self, data: Dict, namespace: str) -> Optional[NamespaceConfigValueType]:
        """
        Handle response body
        """
        data = data.get(CONFIGURATIONS)
        if data is None:
            logger.error(f"'{CONFIGURATIONS}' key not found in data.")
            return data

        content = data.get(CONTENT)
        if content is not None:
            data_bytes = content.encode('utf-8')
            if namespace.endswith('.json'):
                try:
                    return json.loads(data_bytes)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to load JSON content: {e}")
                    return None

            if namespace.endswith('.yaml') or namespace.endswith('.yml'):
                try:
                    return yaml.load(io.BytesIO(data_bytes), Loader=yaml.SafeLoader)
                except yaml.YAMLError as e:
                    logger.error(f"Failed to load YAML content: {e}")
                    return None

            if namespace.endswith('.xml'):
                return xmltodict.parse(content)

            if namespace.endswith('.txt'):
                return str(content)

        for key, s in data.items():
            data[key] = self._parse_properties(s)
        return data

    @staticmethod
    def _parse_properties(s: ValueType) -> ValueType:
        """
        Handle properties file
        """
        # 尝试判断是否是布尔类型
        if s.lower() == "true":
            return True
        elif s.lower() == "false":
            return False

        # 尝试判断是否是数字
        try:
            if '.' in s:
                return float(s)  # 尝试转换为浮点数
            else:
                return int(s)  # 尝试转换为整数
        except ValueError:
            pass

        # 尝试判断是否是列表
        try:
            parsed_list = ast.literal_eval(s)
            if isinstance(parsed_list, list):
                return parsed_list
        except (ValueError, SyntaxError):
            pass

        # 尝试判断是否是字典
        try:
            parsed_dict = ast.literal_eval(s)
            if isinstance(parsed_dict, dict):
                return parsed_dict
        except (ValueError, SyntaxError):
            pass

        # 如果都不是，返回原始字符串
        return s


    @staticmethod
    def _url_encode_wrapper(params: Optional[Dict] = None) -> str:
        """
        URL encode wrapper
        """
        return parse.urlencode(params) if params else ''


    def get_value_from_dict(self, ns_cache: Optional[Dict], key: str) -> Optional[ValueType]:
        """
        Get value from dict
        :param ns_cache: namespace cache dict
        :param key: config key
        """
        if not ns_cache:
            return None
        return ns_cache.get(key)


    def get_from_remote(self, namespace: str='application', n_id: int = -1) -> Dict:
        """
        Get JSON from net
        """
        url = f'{self.config_service_url}/configs/{self.app_id}/{self.cluster}/{namespace}?ip={self.client_ip}'
        code, body = self._http_request(url, timeout=5, headers=self._sign_headers(url))
        if code != 200:
            raise ApolloClientReadRemoteError(f'Failed to fetch configuration {url}, code: {code}, body: {body}')

        data = json.loads(body)
        data = self._handle_resp_body(data=data, namespace=namespace)

        ns_key = self._get_ns(namespace)
        if n_id > -1:
            self._notification_map[namespace] = n_id
            self._call_listener(namespace, self._cache.get(ns_key), data)
        self._cache[ns_key] = data
        return data

    def all(self):
        """
        Get all configurations
        """
        return self._cache

    def get_value(self, key, default_val=None, namespace='application'):
        """
        Get value from cache
        """
        namespace_data = self._cache.get(self._get_ns(namespace))
        val = self.get_value_from_dict(namespace_data, key)
        if val is not None:
            return val
        return default_val

    def _call_listener(self, namespace: str, old_kv: Optional[Dict], new_kv: Optional[Dict]):
        """
        Call listener when configuration changes
        :param namespace: namespace
        :param old_kv: old key-value
        :param new_kv: new key-value
        """
        if not self.change_listener:
            return

        old_kv = old_kv or {}
        new_kv = new_kv or {}

        all_keys = set(old_kv) | set(new_kv)

        try:
            for key in all_keys:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if new_value != old_value:
                    if new_value is None:
                        self.change_listener("delete", namespace, key, old_value)
                    elif old_value is None:
                        self.change_listener("add", namespace, key, new_value)
                    else:
                        self.change_listener("update", namespace, key, new_value)
        except Exception as e:
            logger.exception(f"Error calling change listener for namespace '{namespace}': {e}")


    def stop(self):
        """
        Stop listener
        """
        self.stopping = True
        logger.info("Stopping listener...")

    def _fetch_all(self):
        """
        Update all namespaces
        """
        for namespace in self.namespaces:
            try:
                self.get_from_remote(namespace=namespace)
            except Exception as e:
                logger.exception(f"Failed to fetch namespace '{namespace}' configurations: {e}")

    def _long_poll(self):
        """
        Long poll for changes
        """
        notifications = [
            {
                NAMESPACE_NAME: namespace,
                NOTIFICATION_ID: self._notification_map.get(namespace, -1),
            }
            for namespace in self._ns.values()
        ]

        if not notifications:
            logger.info("_long_poll: No notifications to poll.")
            return

        try:
            url = f'{self.config_service_url}/notifications/v2'
            params = {
                'appId': self.app_id,
                'cluster': self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }
            param_str = self._url_encode_wrapper(params)
            url = url + '?' + param_str
            http_code, body = self._http_request(url, self.pull_timeout,
                                                 headers=self._sign_headers(url))
            if http_code == 304:
                logger.debug('No change detected by long poll.')
                return

            if http_code == 200:
                logger.debug(f"Received update notification: {body}")
                data = json.loads(body)
                for entry in data:
                    namespace = entry[NAMESPACE_NAME]
                    n_id = entry[NOTIFICATION_ID]
                    logger.info(f"{namespace} has changes: notificationId={n_id}")
                    self.get_from_remote(namespace, n_id)
                    break

            else:
                logger.warning(f"Long poll received unexpected HTTP status code: {http_code}")

        except Exception as e:
            logger.warning(f"Long polling failed with an exception: {e}")
            # raise e

    def _listener(self):
        """
        Long poll for changes
        """
        logger.info('start long_poll')
        while not self.stopping:
            self._long_poll()
            time.sleep(self.cycle_time)
        logger.info("stopped, long_poll")

    def _heart_beat(self):
        """
        Heartbeat to apollo server：update all namespaces every 10 minutes
        """
        while not self.stopping:
            self._fetch_all()
            time.sleep(60 * 10)  # 10 minutes update all namespaces

    def _sign_headers(self, url):
        """
        Sign headers for apollo server
        """
        headers = {}
        if self.secret == '':
            return headers
        uri = url[len(self.config_service_url):len(url)]
        time_unix_now = int(time.time() * 1000)
        headers['Authorization'] = 'Apollo ' + self.app_id + ':' + self._signature(time_unix_now, uri, self.secret)
        headers['Timestamp'] = time_unix_now
        return headers

    @staticmethod
    def _signature(timestamp: int, uri: str, secret: str):
        """
        Signature for Apollo server
        :param timestamp: current timestamp
        :param uri: request uri
        :param secret: secret key
        """
        string_to_sign = f'{str(timestamp)}\n{uri}'
        hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
        return base64.b64encode(hmac_code).decode()

if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    def change_listener(action: str, namespace: str, key: str, value: NamespaceConfigValueType):
        print(f"action: {action}, namespace: {namespace}, key: {key}, value", value)

    client = ApolloClient(
        app_id=os.environ.get('APOLLO_APP_ID'),
        config_service_url=os.environ.get('APOLLO_CONFIG_URL'),
        cluster=os.environ.get('APOLLO_CLUSTER'),
        secret=os.environ.get('APOLLO_SECRET'),
        env=os.environ.get('APOLLO_ENV'),
        namespaces=['application', 'test', 'testjson.json', 'testyaml.yaml'],
        ignore_ssl_verify=True,
        change_listener=change_listener
    )
    print(client.all())
    time.sleep(100000)

