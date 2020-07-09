# celery的使用

## 1.简介

```Python
 一. 介绍

    # 1.是一个简单的，灵活且可靠的，处理大量消息的分布式系统

    # 2.专注于实时的处理异步任务队列

    # 3.支持任务的定时执行

    # 4.支持任务调度
    
二、组成部分

   # 1.消息中间件(message borker) --->celery 本身不提供消息服务(redis,RabbitMQ)
   
   # 2.任务执行单元：worker 运行在分布式系统的节点中，可以开多个
    
   # 3.任务结果存储:(Task result store) (AMQP,redis，MySQL等) --> backend

三、使用的场景
   
 # 异步任务：将耗时操作任务提交给Celery去异步执行，比如发送短信/邮件、消息推送、音视频处理             等等

 # 定时任务：定时执行某件事情，比如每天数据统计

```

## 2. celery异步执行任务

### 2.1 基本使用

```python
1. 创建项目：celerytest

2. 创建py文件:celery_task.py

    import celery  -->安装：pip3 install celery
    import time
    # 存储结果
    backend='redis://:123456@127.0.0.1:6379/1'
    # 消息中间件
    broker='redis://:123456@127.0.0.1:6379/2'
    # 第一个参数是起别名，
    cel=celery.Celery('test',backend=backend,broker=broker)
    @cel.task
    def add(x,y):
        return x+y

 3. 创建py文件：add_task.py(将任务添加到队列中)
     
    from celery_task import add
    # 使用delay()为任务函数传参数
    result = add.delay(4,5)
    print(result.id)
    
4. 执行任务(一般使用命令行)： 
    
     4.1 cd \d 文件夹的目录
        
     4.2 在Windows下：celery worker -A celery_task -l info -P eventlet
        
5. 创建py文件：result.py (查看任务的执行结果)

    from celery.result import AsyncResult
    from celery_task import app

async = AsyncResult(id="e919d97d-2938-4d0f-9265-fd8237dc2aa3", app=app)

if async.successful():
    result = async.get()
    print(result)
    # result.forget() # 将结果删除
elif async.failed():
    print('执行失败')
elif async.status == 'PENDING':
    print('任务等待中被执行')
elif async.status == 'RETRY':
    print('任务异常后正在重试')
elif async.status == 'STARTED':
    print('任务已经开始被执行')
   
```

### 2.2 多任务结构

```Python
# 目录结构
   pro_cel
    ├── celery_task # celery相关文件夹
    │   ├── celery.py   # celery连接和配置相关文件,必须叫这个名字
    │   └── tasks1.py    #  所有任务函数
    │	└── tasks2.py    #  所有任务函数
    ├── check_result.py # 检查结果
    └── send_task.py    # 触发任务
  
  
# 1. celery.py文件：

from celery import Celery

cel = Celery('celery_demo',
             broker='redis://127.0.0.1:6379/1',
             backend='redis://127.0.0.1:6379/2',
             # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
             include=['celery_task.tasks1',
                      'celery_task.tasks2'
                      ])

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False


# 2. task1.py文件：
    
import time
from celery_task.celery import cel

@cel.task
def test_celery(res):
    time.sleep(5)
    return "test_celery任务结果:%s"%res


# 3. task2.py 文件

import time
from celery_task.celery import cel
@cel.task
def test_celery2(res):
    time.sleep(5)
    return "test_celery2任务结果:%s"%res


# 4.check_result.py:

from celery.result import AsyncResult
from celery_task.celery import cel

async = AsyncResult(id="08eb2778-24e1-44e4-a54b-56990b3519ef", app=cel)

if async.successful():
    result = async.get()
    print(result)
    # result.forget() # 将结果删除,执行完成，结果不会自动删除
    # async.revoke(terminate=True)  # 无论现在是什么时候，都要终止
    # async.revoke(terminate=False) # 如果任务还没有开始执行呢，那么就可以终止。
elif async.failed():
    print('执行失败')
elif async.status == 'PENDING':
    print('任务等待中被执行')
elif async.status == 'RETRY':
    print('任务异常后正在重试')
elif async.status == 'STARTED':
    print('任务已经开始被执行')
    
    
# 5. send_task.py
    
from celery_task.tasks1 import test_celery
from celery_task.tasks2 import test_celery2

# 立即告知celery去执行test_celery任务，并传入一个参数
result = test_celery.delay('第一个的执行')
print(result.id)
result = test_celery2.delay('第二个的执行')
print(result.id)

  
# 6 添加任务（执行send_task.py），开启work：celery worker -A celery_task -l info  -P  eventlet，检查任务执行结果（执行check_result.py）注 事先要cd要项目的目录下  
```

## 3. celery定时执行任务

### 3.1 普通的执行任务

```python 
send.task.py:
from celery_app_task import add
from datetime import datetime
from datetime import timedelta

# 方式一
# v1 = datetime(2019, 2, 13, 18, 19, 56)
# print(v1)
# 提交任务
# v2 = datetime.utcfromtimestamp(v1.timestamp())
# print(v2)
# result = add.apply_async(args=[1, 3], eta=v2)
# print(result.id)

# 方式二
ctime = datetime.now()
# 默认用utc时间
utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())

time_delay = timedelta(seconds=10)
task_time = utc_ctime + time_delay

# 使用apply_async并设定时间,args为任务传参数，eta设定执行的时间
result = add.apply_async(args=[4, 3], eta=task_time)
print(result.id)   
```

### 3.2 类似于contab的定时任务

```python
# 1. celery.py：

from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

cel = Celery('tasks', broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2', include=[
    'celery_task.tasks1',
    'celery_task.tasks2',
])
cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False

cel.conf.beat_schedule = {
    # 名字随意命名
    'add-every-10-seconds': {
        # 执行tasks1下的test_celery函数
        'task': 'celery_task.tasks1.test_celery',
        # 每隔2秒执行一次
        # 'schedule': 2.0,
        # 'schedule': crontab(minute="*/1"),
        'schedule': timedelta(seconds=2),
        # 传递参数
        'args': ('test',)
    },
    # 'add-every-12-seconds': {
    #     'task': 'celery_task.tasks1.test_celery',
    #     每年4月11号，8点42分执行
    #     'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
    #     'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
    #     'args': (16, 16)
    # },
}




# 2. 执行(在命令行中执行，事先要cd到项目的目录下面)

   启动一个beat：celery beat -A celery_task -l info
    
   启动work执行：celery worker -A celery_task -l info -P  eventlet
 
```

## 4. Django中的使用

```python 
# 安装：Django-celery


# 1. 在项目目录下创建celeryconfig.py：

    import djcelery
    djcelery.setup_loader()
    CELERY_IMPORTS=(
        'app01.tasks',
    )
    #有些情况可以防止死锁
    CELERYD_FORCE_EXECV=True
    # 设置并发worker数量
    CELERYD_CONCURRENCY=4
    #允许重试
    CELERY_ACKS_LATE=True
    # 每个worker最多执行100个任务被销毁，可以防止内存泄漏
    CELERYD_MAX_TASKS_PER_CHILD=100
    # 超时时间
    CELERYD_TASK_TIME_LIMIT=12*30
    
    
# 2. 在app01目录下创建task.py文件 

from celery import task
@task
def add(a,b):
    with open('a.text', 'a', encoding='utf-8') as f:
        f.write('a')
    print(a+b)
    

# 3. 视图函数views.py

from django.shortcuts import render,HttpResponse
from app01.tasks import add
from datetime import datetime
def test(request):
    # result=add.delay(2,3)
    ctime = datetime.now()
    # 默认用utc时间
    utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())
    from datetime import timedelta
    time_delay = timedelta(seconds=5)
    task_time = utc_ctime + time_delay
    result = add.apply_async(args=[4, 3], eta=task_time)
    print(result.id)
    return HttpResponse('ok')


# 4. setting.py 文件中的修改：

  INSTALLED_APPS = [
    ...
    'djcelery',
    'app01'
]

...
#在setting文件中进行配置
from djagocele import celeryconfig
BROKER_BACKEND='redis'
BOOKER_URL='redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2'
   
```



