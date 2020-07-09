
from . import global_settings
from config import settings

class Settings():

    def __init__(self):
        # 需要引入默认的配置文件
        self.__set_attr(global_settings)

        # 需要引入自定义的配置文件
        try:
            self.__set_attr(settings)
        except Exception:
            pass

    def __set_attr(self, obj):
        for key in dir(obj):
            if key.isupper():
                value = getattr(obj, key)
                setattr(self, key, value)


settings = Settings()