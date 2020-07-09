import json

import requests

from lib.conf.config import settings

from src.plugins import PluginManager
from lib.utils import encrypt

class Base(object):

    def post_data(self, server_info):


        data_str = encrypt(json.dumps(server_info))

        # res = requests.post(url='http://127.0.0.1:8200/api/asset.html/', data=data_str)

        requests.post(settings.API, data=data_str)
        # body: json.dumps(server_info)
        # headers= {'content-type':'application/json'}
        # request.body
        # json.loads(request.body)


class Agent(Base):

    def execute(self):
        res = PluginManager().exec_plugins()
        hostname = res['basic']['data']['hostname']
        certname = open(settings.CERT_PATH, 'r', encoding='utf-8').read()

        if not certname.strip():
            with open(settings.CERT_PATH, 'w', encoding='utf-8') as fp:
                fp.write(hostname)
        else:
            res['basic']['data']['hostname'] = certname

        self.post_data(res)


class SSHSALT(Base):

    def get_host(self):

        response = requests.get(settings.API)
        result = json.loads(response.text)  # "{status:'True',data: ['c1.com','c2.com']}"
        if not result['status']:
            return
        return result['data']


    def run(self,host):
        res = PluginManager(host).exec_plugins()

        self.post_data(res)

    def execute(self):

        host_list = self.get_host()
        from concurrent.futures import ThreadPoolExecutor
        p = ThreadPoolExecutor(10)

        for host in host_list:
            p.submit(self.run, host)



