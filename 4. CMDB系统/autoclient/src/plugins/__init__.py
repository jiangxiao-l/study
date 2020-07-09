import importlib
import traceback
from lib.conf.config import settings

class PluginManager(object):

    def __init__(self, hostname = None):
        self.hostname = hostname
        self.settings = settings.PLUGINS_DICT

        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == 'SSH':
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD

    # 执行所有的插件，并返回执行的结果
    def exec_plugins(self):
        response = {}
        ret = []
        for k, v in self.settings.items():
            #'base' : 'src.plugins.base.Base'
            ret = {'status':True, 'data':None}
            try:
                module_name, class_name = v.rsplit('.', 1)
                m = importlib.import_module(module_name)

                cls = getattr(m, class_name)

                if hasattr(cls, 'initial'):
                    obj = cls().initial()
                else:
                    obj = cls()

                res = obj.process(self.command, self.debug)
                ret['data'] = res
            except Exception as e:
                ret['status'] = False
                ret['data'] = "[%s][%s] 采集出错的信息：%s" % (self.hostname if self.hostname else "AGENT", k, traceback.format_exc())

            response[k] = ret

        # ret.append(response)
        return response

    def command(self, cmd):
        if self.mode == 'AGENT':
            return self.__agent_cmd(cmd)
        elif self.mode == 'SSH':
            return self.__ssh_cmd(cmd)
        elif self.mode == 'SALT':
            return self.__salt_cmd(cmd)
        else:
            raise Exception('采集资产的模式不正确，只支持: agent/ssh/salt')


    def __agent_cmd(self, cmd):

        import subprocess
        stdout = subprocess.getoutput(cmd)
        return stdout

    def __salt_cmd(self, cmd):
        # import salt.client
        # local = salt.client.LocalClient()
        # result = local.cmd(self.hostname, 'cmd.run', [cmd])
        # return result[self.hostname]

        salt_cmd = "salt '%s' cmd.run '%s'" % (self.hostname, cmd,)
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh_cmd(self, cmd):

        import paramiko

        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result