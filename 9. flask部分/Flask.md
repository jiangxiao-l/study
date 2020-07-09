# Flask

## 0.Flask简介

Flask是一个基于Python开发并且依赖jinja2模板和Werkzeug  WSGI服务的一个微型框架，对于Werkzeug本质是Socket服务端，其用于接收http请求并对请求进行预处理，然后触发Flask框架，开发人员基于Flask框架提供的功能对请求进行相应的处理，并返回给用户，如果要返回给用户复杂的内容时，需要借助jinja2模板来实现对模板的处理，即：将模板和数据进行渲染，将渲染后的字符串返回给用户浏览器。

“微”(micro) 并不表示你需要把整个 Web 应用塞进单个 Python 文件（虽然确实可以 ），也不意味着 Flask  在功能上有所欠缺。微框架中的“微”意味着 Flask 旨在保持核心简单而易于扩展。Flask 不会替你做出太多决策——比如使用何种数据库。而那些  Flask 所选择的——比如使用何种模板引擎——则很容易替换。除此之外的一切都由可由你掌握。如此，Flask 可以与您珠联璧合。

默认情况下，Flask 不包含数据库抽象层、表单验证，或是其它任何已有多种库可以胜任的功能。然而，Flask  支持用扩展来给应用添加这些功能，如同是 Flask  本身实现的一样。众多的扩展提供了数据库集成、表单验证、上传处理、各种各样的开放认证技术等功能。Flask  也许是“微小”的，但它已准备好在需求繁杂的生产环境中投入使用

## 1.安装

pip3 install flask

## 2.werkzeug简介

Werkzeug是一个WSGI工具包，他可以作为一个Web框架的底层库。这里稍微说一下， werkzeug 不是一个web服务器，也不是一个web框架，而是一个工具包，官方的介绍说是一个 WSGI 工具包，它可以作为一个 Web 框架的底层库，因为它封装好了很多 Web 框架的东西，例如 Request，Response 等等 

代码示例：

```python
from werkzeug.wrappers import Request, Response

@Request.application
def hello(request):
    return Response('Hello World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, hello)
```

## 3.flask快速使用

```python
from flask import Flask
# 实例化产生一个Flask对象
app = Flask(__name__)
# 将 '/'和视图函数hello_workd的对应关系添加到路由中
@app.route('/') # 1. v=app.route('/') 2. v(hello_world)
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run() # 最终调用了run_simple()
```

### 案例：登录，显示用户信息

main.py

```python
from flask import Flask,render_template,request,redirect,session,url_for
app = Flask(__name__)
app.debug = True
app.secret_key = 'sdfsdfsdfsdf'

USERS = {
    1:{'name':'张三','age':18,'gender':'男','text':"道路千万条"},
    2:{'name':'李四','age':28,'gender':'男','text':"安全第一条"},
    3:{'name':'王五','age':18,'gender':'女','text':"行车不规范"},
}

@app.route('/detail/<int:nid>',methods=['GET'])
def detail(nid):
    user = session.get('user_info')
    if not user:
        return redirect('/login')

    info = USERS.get(nid)
    return render_template('detail.html',info=info)


@app.route('/index',methods=['GET'])
def index():
    user = session.get('user_info')
    if not user:
        # return redirect('/login')
        # 反向解析
        url = url_for('l1')
        return redirect(url)
    return render_template('index.html',user_dict=USERS)


@app.route('/login',methods=['GET','POST'],endpoint='l1')
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        # request.query_string
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if user == 'lqz' and pwd == '123':
            session['user_info'] = user
            return redirect('http://www.baidu.com')
        return render_template('login.html',error='用户名或密码错误')

if __name__ == '__main__':
    app.run()
```

detail.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>详细信息 {{info.name}}</h1>
    <div>
        {{info.text}}
    </div>
</body>
</html>
```

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>用户列表</h1>
    <table>
        {% for k,v in user_dict.items() %}
        <tr>
            <td>{{k}}</td>
            <td>{{v.name}}</td>
            <td>{{v['name']}}</td>
            <td>{{v.get('name')}}</td>
            <td><a href="/detail/{{k}}">查看详细</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>用户登录</h1>
    <form method="post">
        <input type="text" name="user">
        <input type="text" name="pwd">
        <input type="submit" value="登录">{{error}}
    </form>
</body>
</html>
```

### 作业：登录认证装饰器

-多个装饰器执行顺序

-反向查找的名称（endpoint），不允许重复

## 4.配置文件

`flask中的配置文件是一个flask.config.Config对象（继承字典）,默认配置为：` 

```python
 {
        'DEBUG':                                get_debug_flag(default=False),  是否开启Debug模式
        'TESTING':                              False,                          是否开启测试模式
        'PROPAGATE_EXCEPTIONS':                 None,                         
        'PRESERVE_CONTEXT_ON_EXCEPTION':        None,
        'SECRET_KEY':                           None,
        'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),
        'USE_X_SENDFILE':                       False,
        'LOGGER_NAME':                          None,
        'LOGGER_HANDLER_POLICY':               'always',
        'SERVER_NAME':                          None,
        'APPLICATION_ROOT':                     None,
        'SESSION_COOKIE_NAME':                  'session',
        'SESSION_COOKIE_DOMAIN':                None,
        'SESSION_COOKIE_PATH':                  None,
        'SESSION_COOKIE_HTTPONLY':              True,
        'SESSION_COOKIE_SECURE':                False,
        'SESSION_REFRESH_EACH_REQUEST':         True,
        'MAX_CONTENT_LENGTH':                   None,
        'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours=12),
        'TRAP_BAD_REQUEST_ERRORS':              False,
        'TRAP_HTTP_EXCEPTIONS':                 False,
        'EXPLAIN_TEMPLATE_LOADING':             False,
        'PREFERRED_URL_SCHEME':                 'http',
        'JSON_AS_ASCII':                        True,
        'JSON_SORT_KEYS':                       True,
        'JSONIFY_PRETTYPRINT_REGULAR':          True,
        'JSONIFY_MIMETYPE':                     'application/json',
        'TEMPLATES_AUTO_RELOAD':                None,
    }
```

### 方式一

```python
   app.config['DEBUG'] = True
   PS： 由于Config对象本质上是字典，所以还可以使用app.config.update(...)
```

### 方式二

```python
#通过py文件配置
app.config.from_pyfile("python文件名称")
如：
settings.py
DEBUG = True

app.config.from_pyfile("settings.py")
#通过环境变量配置
app.config.from_envvar("环境变量名称")
#app.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])
环境变量的值为python文件名称，内部调用from_pyfile方法

app.config.from_json("json文件名称")
JSON文件名称，必须是json格式，因为内部会执行json.loads

app.config.from_mapping({'DEBUG': True})
字典格式

app.config.from_object("python类或类的路径")

app.config.from_object('pro_flask.settings.TestingConfig')

settings.py


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


PS: 从sys.path中已经存在路径开始写

PS: settings.py文件默认路径要放在程序root_path目录，如果instance_relative_config为True，则就是instance_path目录（Flask对象init方法的参数）
```

## 5.路由系统

### 典型写法

```python
@app.route('/detail/<int:nid>',methods=['GET'],endpoint='detail')
```

### 默认转换器

```python
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
```

### 路由系统本质

```python
"""
1. decorator = app.route('/',methods=['GET','POST'],endpoint='n1')
    def route(self, rule, **options):
        # app对象
        # rule= /
        # options = {methods=['GET','POST'],endpoint='n1'}
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
2. @decorator
    decorator(index)
"""
#同理
def login():
    return '登录'
app.add_url_rule('/login', 'n2', login, methods=['GET',"POST"])
#与django路由类似
#django与flask路由：flask路由基于装饰器，本质是基于：add_url_rule
#add_url_rule 源码中，endpoint如果为空，endpoint = _endpoint_from_view_func(view_func)，最终取view_func.__name__（函数名）
```

### CBV(源码分析)

```python
def auth(func):
    def inner(*args, **kwargs):
        print('before')
        result = func(*args, **kwargs)
        print('after')
        return result

    return inner

class IndexView(views.View):
    methods = ['GET']
    decorators = [auth, ]

    def dispatch_request(self):
        print('Index')
        return 'Index!'

app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint
#或者，通常用此方式
  class IndexView(views.MethodView):
            methods = ['GET']
            decorators = [auth, ]

            def get(self):
                return 'Index.GET'

            def post(self):
                return 'Index.POST'
        app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint

```

### app.add_url_rule参数

```python
@app.route和app.add_url_rule参数:
rule, URL规则
view_func, 视图函数名称
defaults = None, 默认值, 当URL中无参数，函数需要参数时，使用defaults = {'k': 'v'}
为函数提供参数
endpoint = None, 名称，用于反向生成URL，即： url_for('名称')
methods = None, 允许的请求方式，如：["GET", "POST"]
#对URL最后的 / 符号是否严格要求
strict_slashes = None
    '''
        @app.route('/index', strict_slashes=False)
        #访问http://www.xx.com/index/ 或http://www.xx.com/index均可
        @app.route('/index', strict_slashes=True)
        #仅访问http://www.xx.com/index
    '''
#重定向到指定地址
redirect_to = None, 
    '''
        @app.route('/index/<int:nid>', redirect_to='/home/<nid>')
    '''

#子域名访问
subdomain = None, 
    '''
    #C:\Windows\System32\drivers\etc\hosts
    127.0.0.1       www.liuqingzheng.com
	127.0.0.1       admin.liuqingzheng.com
	127.0.0.1       buy.liuqingzheng.com
    
    from flask import Flask, views, url_for
    app = Flask(import_name=__name__)
    app.config['SERVER_NAME'] = 'liuqingzheng.com:5000'
    @app.route("/", subdomain="admin")
    def static_index():
        """Flask supports static subdomains
        This is available at static.your-domain.tld"""
        return "static.your-domain.tld"
    #可以传入任意的字符串，如传入的字符串为aa，显示为 aa.liuqingzheng.com
    @app.route("/dynamic", subdomain="<username>")
    def username_index(username):
        """Dynamic subdomains are also supported
        Try going to user1.your-domain.tld/dynamic"""
        return username + ".your-domain.tld"
    if __name__ == '__main__':
        app.run()
        
    访问：
    http://www.liuqingzheng.com:5000/dynamic
    http://admin.liuqingzheng.com:5000/dynamic
    http://buy.liuqingzheng.com:5000/dynamic
    '''
```

### 支持正则

```python
#1 写类，继承BaseConverter
#2 注册：app.url_map.converters['regex'] = RegexConverter
# 3 使用：@app.route('/index/<regex("\d+"):nid>')  正则表达式会当作第二个参数传递到类中
from flask import Flask, views, url_for
from werkzeug.routing import BaseConverter

app = Flask(import_name=__name__)

class RegexConverter(BaseConverter):
    """
    自定义URL匹配正则表达式
    """
    def __init__(self, map, regex):
        super(RegexConverter, self).__init__(map)
        self.regex = regex

    def to_python(self, value):
        """
        路由匹配时，匹配成功后传递给视图函数中参数的值
        """
        return int(value)

    def to_url(self, value):
        """
        使用url_for反向生成URL时，传递的参数经过该方法处理，返回的值用于生成URL中的参数
        """
        val = super(RegexConverter, self).to_url(value)
        return val
# 添加到flask中
app.url_map.converters['regex'] = RegexConverter
@app.route('/index/<regex("\d+"):nid>')
def index(nid):
    print(url_for('index', nid='888'))
    return 'Index'

if __name__ == '__main__':
    app.run()
```

## 6.模版

比django中多可以加括号，执行函数，传参数

```python
from flask import Flask,render_template,Markup,jsonify,make_response
app = Flask(__name__)

def func1(arg):
    return Markup("<input type='text' value='%s' />" %(arg,))
@app.route('/')
def index():
    return render_template('index.html',ff = func1)

if __name__ == '__main__':
    app.run()
```

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

    {{ff('六五')}}
	{{ff('六五')|safe}}

</body>
</html>
```

注意：

1.Markup等价django的mark_safe ,

2.extends,include一模一样

## 7.请求响应

````python
   from flask import Flask
    from flask import request
    from flask import render_template
    from flask import redirect
    from flask import make_response

    app = Flask(__name__)


    @app.route('/login.html', methods=['GET', "POST"])
    def login():

        # 请求相关信息
        # request.method
        # request.args
        # request.form
        # request.values
        # request.cookies
        # request.headers
        # request.path
        # request.full_path
        # request.script_root
        # request.url
        # request.base_url
        # request.url_root
        # request.host_url
        # request.host
        # request.files
        # obj = request.files['the_file_name']
        # obj.save('/var/www/uploads/' + secure_filename(f.filename))

        # 响应相关信息
        # return "字符串"
        # return render_template('html模板路径',**{})
        # return redirect('/index.html')
        #return jsonify({'k1':'v1'})

        # response = make_response(render_template('index.html'))
        # response是flask.wrappers.Response类型
        # response.delete_cookie('key')
        # response.set_cookie('key', 'value')
        # response.headers['X-Something'] = 'A value'
        # return response
        return "内容"

    if __name__ == '__main__':
        app.run()
````

## 8.session

除请求对象之外，还有一个 session 对象。它允许你在不同请求间存储特定用户的信息。它是在 Cookies 的基础上实现的，并且对 Cookies 进行密钥签名要使用会话，你需要设置一个密钥。 (app.session_interface对象)

```python
设置：session['username'] ＝ 'xxx'
删除：session.pop('username', None)
```

## 9.闪现（message）

```python
-设置:flash('aaa')
-取值：get_flashed_message()
-假设在a页面操作出错，跳转到b页面，在b页面显示a页面的错误信息
```
示例：

```python
from flask import Flask,flash,get_flashed_messages,request,redirect

app = Flask(__name__)
app.secret_key = 'asdfasdf'


@app.route('/index')
def index():
    # 从某个地方获取设置过的所有值，并清除。
    val = request.args.get('v')
    if val == 'oldboy':
        return 'Hello World!'
    flash('超时错误',category="x1")
    return "ssdsdsdfsd"
    # return redirect('/error')


@app.route('/error')
def error():
    """
    展示错误信息
    :return:
    """
    data = get_flashed_messages(category_filter=['x1'])
    if data:
        msg = data[0]
    else:
        msg = "..."
    return "错误信息：%s" %(msg,)

if __name__ == '__main__':
    app.run()
```

## 10.请求扩展

### 1 before_request

类比django中间件中的process_request，在请求收到之前绑定一个函数做一些事情 

```python
#基于它做用户登录认证
@app.before_request
def process_request(*args,**kwargs):
    if request.path == '/login':
        return None
    user = session.get('user_info')
    if user:
        return None
    return redirect('/login')
```

### 2 after_request

类比django中间件中的process_response，每一个请求之后绑定一个函数，如果请求没有异常 

```python
@app.after_request
def process_response1(response):
    print('process_response1 走了')
    return response
```

### 3 before_first_request

第一次请求时,跟浏览器无关

```python
@app.before_first_request
def first():
    pass
```

### 4 teardown_request 

每一个请求之后绑定一个函数，即使遇到了异常 

```python
@app.teardown_request 
def ter(e):
    pass
```
### 5 errorhandler

路径不存在时404，服务器内部错误500

```python
@app.errorhandler(404)
def error_404(arg):
    return "404错误了"
```

### 6 template_global

标签

```python
@app.template_global()
def sb(a1, a2):
    return a1 + a2
#{{sb(1,2)}}
```

### 7 template_filter

过滤器

```python
@app.template_filter()
def db(a1, a2, a3):
    return a1 + a2 + a3
#{{ 1|db(2,3)}}
```

总结：

1 重点掌握before_request和after_request，

2 注意有多个的情况，执行顺序

3 before_request请求拦截后（也就是有return值），response所有都执行

## 11 中间件（了解）

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
# 模拟中间件
class Md(object):
    def __init__(self,old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def __call__(self,  environ, start_response):
        print('开始之前')
        ret = self.old_wsgi_app(environ, start_response)
        print('结束之后')
        return ret

if __name__ == '__main__':
    #把原来的wsgi_app替换为自定义的
    app.wsgi_app = Md(app.wsgi_app)
    app.run()
```

## 12.蓝图

对程序进行目录结构划分

### 不使用蓝图，自己分文件

目录结构：

```python
-templates
-views
	-__init__.py
    -user.py
    -order.py
-app.py
```

app.py

```python
from views import app
if __name__ == '__main__':
    app.run()
```

init.py

```python
from flask import Flask,request
app = Flask(__name__)
#不导入这个不行
from . import account
from . import order
from . import user
```

user.py

```python
from . import app
@app.route('/user')
def user():
    return 'user'
```

order.py

```python
from . import app
@app.route('/order')
def order():
    return 'order'
```

### 使用蓝图之中小型系统

详见代码：pro_flask_简单应用程序目录示例.zip

目录结构：

```python
-flask_pro
	-flask_test
    	-__init__.py
    	-static
        -templates
        -views
        	-order.py
            -user.py
     -manage.py 
        
```

__init_.py

```python
from flask import  Flask
app=Flask(__name__)
from flask_test.views import user
from flask_test.views import order
app.register_blueprint(user.us)
app.register_blueprint(order.ord)
```

manage.py

```python
from flask_test import  app
if __name__ == '__main__':
    app.run(port=8008)
```

user.py

```python
from flask import Blueprint
us=Blueprint('user',__name__)

@us.route('/login')
def login():
    return 'login'
```

order.py

```python
from flask import Blueprint
ord=Blueprint('order',__name__)

@ord.route('/test')
def test():
    return 'order test'
```

### 使用蓝图之大型系统

详见代码：pro_flask_大型应用目录示例.zip

总结：

1 xxx = Blueprint('account', __name__,url_prefix='/xxx') ：蓝图URL前缀，表示url的前缀，在该蓝图下所有url都加前缀

2 xxx = Blueprint('account', name,url_prefix='/xxx',template_folder='tpls')：给当前蓝图单独使用templates，向上查找，当前找不到，会找总templates

3 蓝图的befort_request，对当前蓝图有效

4 大型项目，可以模拟出类似于django中app的概念

## 13.请求上下文源码分析

```python
第一阶段：将ctx(request,session)放到Local对象上
				   
第二阶段：视图函数导入：request/session 
request.method
	-LocalProxy对象.method,执行getattr方法，getattr(self._get_current_object(), name)
		-self._get_current_object()返回return self.__local()，self.__local()，在LocakProxy实例化的时候,object.__setattr__(self, '_LocalProxy__local', local),此处local就是：partial(_lookup_req_object, 'request')

	-def _lookup_req_object(name):
			top = _request_ctx_stack.top #_request_ctx_stack 就是LocalStack()对象，top方法把ctx取出来
			if top is None:
				raise RuntimeError(_request_ctx_err_msg)
			return getattr(top, name)#获取ctx中的request或session对象

第三阶段：请求处理完毕
		- 获取session并保存到cookie
		- 将ctx删除
```

程序运行，两个LocalStack()对象，一个里面放request和session，另一个放g和`current_app` 

## 14.g对象

专门用来存储用户信息的g对象，g的全称的为global 

g对象在一次请求中的所有的代码的地方，都是可以使用的 

当次请求的全局变量。可以做权限的保存

### g对象和session的区别

```python
session对象是可以跨request的，只要session还未失效，不同的request的请求会获取到同一个session，但是g对象不是，g对象不需要管过期时间，请求一次就g对象就改变了一次，或者重新赋值了一次
```

## 15.flask-session

作用：将默认保存的签名cookie中的值 保存到 redis/memcached/file/Mongodb/SQLAlchemy

安装：pip3 install flask-session

使用1：

```python
from flask import Flask,session
from flask_session import RedisSessionInterface
import redis
app = Flask(__name__)
conn=redis.Redis(host='127.0.0.1',port=6379)
#use_signer是否对key签名
app.session_interface=RedisSessionInterface(conn,key_prefix='lqz')
@app.route('/')
def hello_world():
    session['name']='lqz'
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

使用2：

```python
from redis import Redis
from flask.ext.session import Session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='192.168.0.94',port='6379')
Session(app)
```

问题：设置cookie时，如何设定关闭浏览器则cookie失效。

```python
response.set_cookie('k','v',exipre=None)#这样设置即可
#在session中设置
app.session_interface=RedisSessionInterface(conn,key_prefix='lqz',permanent=False)
#一般不用，我们一般都设置超时时间，多长时间后失效
```

问题：cookie默认超时时间是多少？如何设置超时时间

```python
#源码expires = self.get_expiration_time(app, session)
'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),#这个配置文件控制
```





## 16.数据库连接池

### pymsql链接数据库

```python
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='s8day127db')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# cursor.execute("select id,name from users where name=%s and pwd=%s",['lqz','123',])
cursor.execute("select id,name from users where name=%(user)s and pwd=%(pwd)s",{'user':'lqz','pwd':'123'})
obj = cursor.fetchone()
conn.commit()
cursor.close()
conn.close()

print(obj)
```

### 数据库连接池版

setting.py

```python
from datetime import timedelta
from redis import Redis
import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection

class Config(object):
    DEBUG = True
    SECRET_KEY = "umsuldfsdflskjdf"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    SESSION_REFRESH_EACH_REQUEST= True
    SESSION_TYPE = "redis"
    PYMYSQL_POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        database='s8day127db',
        charset='utf8'
    )

class ProductionConfig(Config):
    SESSION_REDIS = Redis(host='192.168.0.94', port='6379')



class DevelopmentConfig(Config):
    SESSION_REDIS = Redis(host='127.0.0.1', port='6379')


class TestingConfig(Config):
    pass
```

utils/sql.py

```python
import pymysql
from settings import Config
class SQLHelper(object):

    @staticmethod
    def open(cursor):
        POOL = Config.PYMYSQL_POOL
        conn = POOL.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn,cursor

    @staticmethod
    def close(conn,cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls,sql,args,cursor =pymysql.cursors.DictCursor):
        conn,cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchone()
        cls.close(conn,cursor)
        return obj

    @classmethod
    def fetch_all(cls,sql, args,cursor =pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj
```

使用：

```python
obj = SQLHelper.fetch_one("select id,name from users where name=%(user)s and pwd=%(pwd)s", form.data)
```



## 17.wtforms

安装:pip3 install wtforms

###使用1：

```python
from flask import Flask, render_template, request, redirect
from wtforms import Form
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

app = Flask(__name__, template_folder='templates')

app.debug = True


class LoginForm(Form):
    # 字段（内部包含正则表达式）
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空.'),
            validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(), # 页面上显示的插件
        render_kw={'class': 'form-control'}

    )
    # 字段（内部包含正则表达式）
    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')

        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
```

login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>登录</h1>
<form method="post">
    <p>{{form.name.label}} {{form.name}} {{form.name.errors[0] }}</p>

    <p>{{form.pwd.label}} {{form.pwd}} {{form.pwd.errors[0] }}</p>
    <input type="submit" value="提交">
</form>
</body>
</html>
```

### 使用2：

```python
from flask import Flask, render_template, request, redirect
from wtforms import Form
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

app = Flask(__name__, template_folder='templates')
app.debug = True



class RegisterForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='alex'
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            # 代替了全局钩子
            validators.EqualTo('pwd', message="两次密码输入不一致")
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空.'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )

    gender = core.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),
        coerce=int # “1” “2”
     )
    city = core.SelectField(
        label='城市',
        choices=(
            ('bj', '北京'),
            ('sh', '上海'),
        )
    )

    hobby = core.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )

    favor = core.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=int,
        default=[1, 2]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.favor.choices = ((1, '篮球'), (2, '足球'), (3, '羽毛球'))
    
    # 局部钩子
    def validate_pwd_confirm(self, field):
        """
        自定义pwd_confirm字段规则，例：与pwd字段是否一致
        :param field:
        :return:
        """
        # 最开始初始化时，self.data中已经有所有的值

        if field.data != self.data['pwd']:
            # raise validators.ValidationError("密码不一致") # 继续后续验证
            raise validators.StopValidation("密码不一致")  # 不再继续后续验证


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(data={'gender': 2,'hobby':[1,]}) # initial
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run()
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>用户注册</h1>
<form method="post" novalidate style="padding:0  50px">
    {% for field in form %}
    <p>{{field.label}}: {{field}} {{field.errors[0] }}</p>
    {% endfor %}
    <input type="submit" value="提交">
</form>
</body>
</html>
```



## 18.信号

Flask框架中的信号基于blinker，其主要就是让开发者在flask请求过程中定制一些用户行为 

安装：`pip3 install blinker` 

内置信号：

```python
request_started = _signals.signal('request-started')                # 请求到来前执行
request_finished = _signals.signal('request-finished')              # 请求结束后执行
 
before_render_template = _signals.signal('before-render-template')  # 模板渲染前执行
template_rendered = _signals.signal('template-rendered')            # 模板渲染后执行
 
got_request_exception = _signals.signal('got-request-exception')    # 请求执行出现异常时执行
 
request_tearing_down = _signals.signal('request-tearing-down')      # 请求执行完毕后自动执行（无论成功与否）
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')# 应用上下文执行完毕后自动执行（无论成功与否）
 
appcontext_pushed = _signals.signal('appcontext-pushed')            # 应用上下文push时执行
appcontext_popped = _signals.signal('appcontext-popped')            # 应用上下文pop时执行
message_flashed = _signals.signal('message-flashed')                # 调用flask在其中添加数据时，自动触发
```

使用信号：

```python
from flask import Flask,signals,render_template

app = Flask(__name__)

# 往信号中注册函数
def func(*args,**kwargs):
    print('触发型号',args,kwargs)
signals.request_started.connect(func)

# 触发信号： signals.request_started.send()
@app.before_first_request
def before_first1(*args,**kwargs):
    pass
@app.before_first_request
def before_first2(*args,**kwargs):
    pass

@app.before_request
def before_first3(*args,**kwargs):
    pass

@app.route('/',methods=['GET',"POST"])
def index():
    print('视图')
    return render_template('index.html')


if __name__ == '__main__':
    app.wsgi_app
    app.run()
```

一个流程中的信号触发点（了解）

```python
a. before_first_request
b. 触发 request_started 信号
c. before_request
d. 模板渲染
	渲染前的信号 before_render_template.send(app, template=template, context=context)
		rv = template.render(context) # 模板渲染
	渲染后的信号 template_rendered.send(app, template=template, context=context)
e. after_request
f. session.save_session()
g. 触发 request_finished信号		
	如果上述过程出错：
		触发错误处理信号 got_request_exception.send(self, exception=e)
			
h. 触发信号 request_tearing_down
```

自定义信号(了解)：

```python
from flask import Flask, current_app, flash, render_template
from flask.signals import _signals
app = Flask(import_name=__name__)

# 自定义信号
xxxxx = _signals.signal('xxxxx')
 
def func(sender, *args, **kwargs):
    print(sender)
# 自定义信号中注册函数
xxxxx.connect(func)
@app.route("/x")
def index():
    # 触发信号
    xxxxx.send('123123', k1='v1')
    return 'Index' 
 
if __name__ == '__main__':
    app.run()
```



## 19.多app应用

```python
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, current_app
app1 = Flask('app01')
app2 = Flask('app02')

@app1.route('/index')
def index():
    return "app01"

@app2.route('/index2')
def index2():
    return "app2"

# http://www.oldboyedu.com/index
# http://www.oldboyedu.com/sec/index2
dm = DispatcherMiddleware(app1, {
    '/sec': app2,
})

if __name__ == "__main__":
    run_simple('localhost', 5000, dm)

```

## 20.flask-script

用于实现类似于django中 python3 manage.py runserver  ...类似的命令

安装：pip3 install flask-script

###使用

```python
from flask_script import Manager
app = Flask(__name__)
manager=Manager(app)
...
if __name__ == '__main__':
    manager.run()
#以后在执行，直接：python3 manage.py runserver
#python3 manage.py runserver --help
```

### 自定制命令

```python
@manager.command
def custom(arg):
    """
    自定义命令
    python manage.py custom 123
    :param arg:
    :return:
    """
    print(arg)


@manager.option('-n', '--name', dest='name')
#@manager.option('-u', '--url', dest='url')
def cmd(name, url):
    """
    自定义命令（-n也可以写成--name）
    执行： python manage.py  cmd -n lqz -u http://www.oldboyedu.com
    执行： python manage.py  cmd --name lqz --url http://www.oldboyedu.com
    :param name:
    :param url:
    :return:
    """
    print(name, url)
#有什么用？
#把excel的数据导入数据库，定制个命令，去执行
```

## 
























