
# from lib.conf.config import Settings
# from  src.plugins import PluginManager
# import sys,os
# BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASEDIR)
from src import script

if __name__ == '__main__':
    script.run()

    # res = PluginManager().exec_plugins()
    #
    # print(res)
    #
    # for k, v in res.items():
    #
    #     print(k, v)