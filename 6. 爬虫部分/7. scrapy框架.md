# 简介

​    Scrapy一个开源和协作的框架，其最初是为了页面抓取所设计的，使用它可以以快速、简单、可扩展的方式从网站中提取所需的数据。但目前Scrapy的用途十分广泛，可用于如数据挖掘、监测和自动化测试等领域，也可以应用在获取API所返回的数据(例如 Amazon Associates Web Services ) 或者通用的网络爬虫。

​    Scrapy 是基于twisted框架开发而来，twisted是一个流行的事件驱动的python网络框架。因此Scrapy使用了一种非阻塞（又名异步）的代码来实现并发。整体架构大致如下

![1036857-20171109221422778-1731419400](https://ws3.sinaimg.cn/large/006tNc79gy1fzhbu5vysxj312w0q4wge.jpg)

执行流程：

1.引擎从spider获取初始爬行请求。
2.引擎在调度程序中调度请求，并请求下一个要爬行的请求。
3.调度程序将下一个请求返回到引擎。
4.引擎将请求发送到下载器，并通过下载器中间件（请参见process_request（））。
5.一旦页面完成下载，下载器将生成响应（使用该页面），并将其发送到引擎，并通过下载器中间软件（请参见process_response（））。
6.引擎接收下载器的响应并将其发送给spider进行处理，并通过spider中间件进行处理（请参见process_spider_input（））。
7.spider处理响应，并通过spider中间件（请参见process_spider_output（））向引擎返回刮掉的项目和新请求（后续）。
8.引擎将已处理的项目发送到项目管道，然后将已处理的请求发送到计划程序，并请求可能的下一个请求进行爬网。
9.该过程重复（从步骤1开始），直到调度程序不再发出请求。

# 各组件以及作用

1. **引擎(EGINE)**

   引擎负责控制系统所有组件之间的数据流，并在某些动作发生时触发事件。有关详细信息，请参见上面的数据流部分。

2. **调度器(SCHEDULER)**
   用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL的优先级队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址

3. **下载器(DOWLOADER)**
   用于下载网页内容, 并将网页内容返回给EGINE，下载器是建立在twisted这个高效的异步模型上的

4. **爬虫(SPIDERS)**
   SPIDERS是开发人员自定义的类，用来解析responses，并且提取items，或者发送新的请求

5. **项目管道(ITEM PIPLINES)**
   在items被提取后负责处理它们，主要包括清理、验证、持久化（比如存到数据库）等操作

6. **下载器中间件(Downloader Middlewares)**

   位于Scrapy引擎和下载器之间，主要用来处理从EGINE传到DOWLOADER的请求request，已经从DOWNLOADER传到EGINE的响应response

7. **爬虫中间件(Spider Middlewares)**
   位于EGINE和SPIDERS之间，主要工作是处理SPIDERS的输入（即responses）和输出（即requests

# 安装

```python
#Windows平台
    1、pip3 install wheel #安装后，便支持通过wheel文件安装软件，wheel文件官网：https://www.lfd.uci.edu/~gohlke/pythonlibs
    3、pip3 install lxml
    4、pip3 install pyopenssl
    5、下载并安装pywin32：https://sourceforge.net/projects/pywin32/files/pywin32/
    6、下载twisted的wheel文件：http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
    7、执行pip3 install 下载目录\Twisted-17.9.0-cp36-cp36m-win_amd64.whl
    8、pip3 install scrapy
  
#Linux平台
    1、pip3 install scrapy
```

# 常用命令 

```python
#1 查看帮助
    scrapy -h
    scrapy <command> -h

#2 有两种命令：其中Project-only必须切到项目文件夹下才能执行，而Global的命令则不需要
    Global commands:
        startproject #创建项目
        	scrapy startproject amazon
        genspider    #创建爬虫程序  指定名称 限制爬取的网址
        	scrapy genspider amzon www.amzon.cn
        settings     #如果是在项目目录下，则得到的是该项目的配置
        	scrapy settings --get BOT_NAME
        runspider    #运行一个独立的python文件，不必创建项目
        	scrapy runspider amzon.py
        shell        #scrapy shell url地址  在交互式调试，如选择器规则正确与否
        	scrapy shell www.taobao.com
        fetch        #单纯地爬取一个页面，不打开浏览器，可以拿到请求头
        	 scrapy fetch --nolog http://www.baidu.com 不输出日志
             scrapy fetch --nolog --header http://www.baidu.com 不输出日志  只查看头信息
        view         #下载完毕后直接弹出浏览器，以此可以分辨出哪些数据是ajax请求
        	scrapy view http://www.baidu.com
        version      #scrapy version 查看scrapy的版本，scrapy version -v查看scrapy依赖库的版本
        	scrapy version -v
            
            
    Project-only commands:
		#必须先切换到对应的目录才能执行
        crawl        #运行爬虫，必须创建项目才行，确保配置文件中ROBOTSTXT_OBEY = False
        	scrapy crawl amzon
        check        #检测项目中有无语法错误
        	scrapy check
        list         #列出项目中所包含的爬虫名
        	scrapy list
        edit         #编辑器，一般不用
        parse        #scrapy parse url地址 --callback 回调函数  #以此可以验证我们的回调函数是否正确
        bench        #scrapy bentch压力测试
		
#3 官网链接
    https://docs.scrapy.org/en/latest/topics/commands.html
```

# 目录结构

```python
project_name/
   scrapy.cfg
   project_name/
       __init__.py
       items.py
       pipelines.py
       settings.py
       spiders/
           __init__.py
           爬虫1.py
           爬虫2.py
           爬虫3.py
文件说明：
scrapy.cfg  项目的主配置信息，用来部署scrapy时使用，爬虫相关的配置信息在settings.py文件中。
items.py    设置数据存储模板，用于结构化数据，如：Django的Model
pipelines    数据处理行为，如：一般结构化的数据持久化
settings.py 配置文件，如：递归的层数、并发数，延迟下载等。强调:配置文件的选项必须大写否则视为无效，正确写法USER_AGENT='xxxx'
spiders      爬虫目录，如：创建文件，编写爬虫规则
注意：一般创建爬虫文件时，以网站域名命名

import sys,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
```

## 在pycharm中运行爬虫程序

在项目目录下新建：entrypoint.py

```python
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'amzon'])
```

###  Spiders

#### 简介

1、Spiders是由一系列类（定义了一个网址或一组网址将被爬取）组成，具体包括如何执行爬取任务并且如何从页面中提取结构化的数据。

2、换句话说，Spiders是你为了一个特定的网址或一组网址自定义爬取和解析页面行为的地方

#### spiders的运作过程

```python
#1、生成初始的Requests来爬取第一个URLS，并且标识一个回调函数
第一个请求定义在start_requests()方法内默认从start_urls列表中获得url地址来生成Request请求，默认的回调函数是parse方法。回调函数在下载完成返回response时自动触发

#2、在回调函数中，解析response并且返回值
返回值可以4种：
        包含解析数据的字典
        Item对象
        新的Request对象（新的Requests也需要指定一个回调函数）
        或者是可迭代对象（包含Items或Request）

#3、在回调函数中解析页面内容
通常使用Scrapy自带的Selectors，但很明显你也可以使用Beutifulsoup，lxml或其他你爱用啥用啥。

#4、最后，针对返回的Items对象将会被持久化到数据库
通过Item Pipeline组件存到数据库：https://docs.scrapy.org/en/latest/topics/item-pipeline.html#topics-item-pipeline）
或者导出到不同的文件（通过Feed exports：https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-exports）
```

#### spiders模板类

```python
Spider 基础的爬虫 也是我们呢最常用的爬虫  不会对response 进行任何解析 直接传给回调函数

SitemapSpider 站点信息爬虫 对于需要seo优化的网站通常会在网站根目录下创建 站点地图文件
 其中列出网站所有链接地址，然后将该文件提交给搜索引擎，搜索引擎收录后，会查看其中的信息，例如最后跟新时间等，以便于搜索引擎的爬虫更有效的爬取你的网页

CrawlSpider
CrawlSpider类定义了一些规则(rule)来提供跟进link的机制，从爬取的网页中获取link并继续爬取。

固定格式爬虫
CSVFeedSpider  回调函数parse_row包含一个row用于直接提取一行内容
XMLFeedSpider，回调函数parse_node包含一个node表示一个节点

```

#### Spider的详细使用

这是最简单的spider类，任何其他的spider类都需要继承它（包含你自己定义的）。

该类不提供任何特殊的功能，它仅提供了一个默认的start_requests方法默认从start_urls中读取url地址发送requests请求，并且默认parse作为回调函数

```python
class AmazonSpider(scrapy.Spider):
    name = 'amazon' 
    allowed_domains = ['www.amazon.cn'] 
    start_urls = ['http://www.amazon.cn/']
    
    custom_settings = {
        'BOT_NAME' : 'Egon_Spider_Amazon',
        'REQUEST_HEADERS' : {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en',
        }
    }
    def parse(self, response):
        pass
```

```python
#1、name = 'amazon' 
定义爬虫名，scrapy会根据该值定位爬虫程序
所以它必须要有且必须唯一（In Python 2 this must be ASCII only.）

#2、allowed_domains = ['www.amazon.cn'] 
定义允许爬取的域名，如果OffsiteMiddleware启动（默认就启动），
那么不属于该列表的域名及其子域名都不允许爬取
如果爬取的网址为：https://www.example.com/1.html，那就添加'example.com'到列表.

#3、start_urls = ['http://www.amazon.cn/']
如果没有指定start_requests，就从该列表中读取url来生成第一个请求

#4、custom_settings
值为一个字典，定义一些配置信息，在运行爬虫程序时，这些配置会覆盖项目级别的配置
所以custom_settings必须被定义成一个类属性
 
#5、settings
通过self.settings['配置项的名字']可以访问settings.py中的配置，如果自己定义了custom_settings还是以自己的为准

#6、logger
日志名默认为spider的名字
self.logger.debug('=============>%s' %self.settings['BOT_NAME'])


#7、start_requests()
该方法用来发起第一个Requests请求，且必须返回一个可迭代的对象。它在爬虫程序打开时就被Scrapy调用，Scrapy只调用它一次。
默认从start_urls里取出每个url来生成Request(url, dont_filter=True)
        
#8、parse(response)
这是默认的回调函数，所有的回调函数必须返回an iterable of Request and/or dicts or Item objects.

#9、closed(reason)
爬虫程序结束时自动触发
```

## 自定义去重规则

在爬取网页的过程中可能会爬到一些重复的网页，这就需要制定去重规则了，默认情况下scrapy就会自动帮我们去除

```python
去重规则应该多个爬虫共享的，但凡一个爬虫爬取了，其他都不要爬了，实现方式如下

#方法一：
1、新增类属性
visited=set() #类属性

2、回调函数parse方法内：
def parse(self, response):
    if response.url in self.visited:
        return None
    .......

    self.visited.add(response.url) 

#方法一改进：针对url可能过长，所以我们存放url的hash值
def parse(self, response):
        url=md5(response.request.url)
    if url in self.visited:
        return None
    .......

    self.visited.add(url) 

#方法二：Scrapy自带去重功能
配置文件：
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter' #默认的去重规则帮我们去重，去重规则在内存中
DUPEFILTER_DEBUG = False # 是否记录所有重复请求 默认为第一个重复请求
JOBDIR = "保存范文记录的日志路径，如：/root/"  # 最终路径为 /root/requests.seen，去重规则放文件中

scrapy自带去重规则默认为RFPDupeFilter，只需要我们指定
Request(...,dont_filter=False) ，如果dont_filter=True则告诉Scrapy这个URL不参与去重。

#方法三：
我们也可以仿照RFPDupeFilter自定义去重规则，

from scrapy.dupefilter import RFPDupeFilter，看源码，仿照BaseDupeFilter

#步骤一：在项目目录下自定义去重文件dup.py
class UrlFilter(object):
    def __init__(self):
        self.visited = set() #或者放到数据库

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        if request.url in self.visited:
            return True
        self.visited.add(request.url)

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass

#步骤二：配置文件settings.py：
DUPEFILTER_CLASS = '项目名.dup.UrlFilter'


# 源码分析：
from scrapy.core.scheduler import Scheduler
见Scheduler下的enqueue_request方法：self.df.request_seen(request)
```

## 数据解析

```python
response常用属性与方法
text 获取文本
body 获取二进制
css() css选择器
xpath() xptah解析

css与xpath返回值都是selector类型

selector常用方法
extract   提取字符串形式数据
extract_first 提取第一个
css() 在当前文档上继续查找其他元素  返回selector类型
xpath()在当前文档上继续查找其他元素 返回selector类型
```

## 数据持久化

scrapy中使用item来作为数据模型，pipeline作为数据持久化组件

##### items.py

找到items文件 为itme类添加所需的属性

```python
class PicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
```

##### pipelines.py

一个pipeline应该具备以下几个方法

```python
class MyPipeline():
	def process_item(self, item, spider):
        """
        负责将一个Item进行持久化
        返回值将继续传递给下一个pipeline（如果有），即便是None
        """
        return item
	
    def open_spider(self, spider):
        """
        爬虫程序启动时执行该函数
        用于初始化操作例如连接数据库
        """
        pass

    def close_spider(self, spider):
        """
        爬虫程序关闭时执行该函数
        用于初清理操作例如关闭数据库
        """
        pass
   
	# 创建pipeline 会自动查看是否存在该方法如果存在则直接调用 用于获取一个pipline
    # crawler中的settings属性可以获取配置文件信息
    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中读取数据来创建pipline
        def get(key):
            return crawler.settings.get(key)
        return cls(get("HOST"),get("USER"),get("PWD"),get("DB"))
```

##### 代码写完后需要到配置文件中添加对应的配置项

```python
#数字表示优先级，数值越小优先级越高
ITEM_PIPELINES = {
    "name.pipelines.MysqlPipeline":10,
    "name.pipelines.JsonPipeline":20
}
```

##### 一个基于文件的实例

```python
class JsonPipeline():
    def __init__(self):
        self.json_data = []
    # 在这里处理item的持久化
    def process_item(self, item, spider):
        self.json_data.append(dict(item))
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        with open("pics.json","wt") as f:
            json.dump(self.json_data,f)
```

##### 中断pipeline的继续调用

process_item函数一旦有返回值就会继续执行后续的pipeline，即时返回None，可以是使用以下方法中断

```python
#导入 DropItem类
from scrapy.exceptions import  DropItem
# 在process_item中抛出异常
def process_item(self, item, spider):
    raise DropItem
```

## 下载器中间件

下载器主要负责从网络上下载数据，下载器中间件用于对请求与响应进行处理

例如：设置cookie，header，添加代理等等

```python
class DownMiddleware1(object):
    def process_request(self, request, spider):
        """
        该方法在下载器发起请求前执行
        :param request: 
        :param spider: 
        :return:  
            None,继续后续中间件去下载；
            Response对象，停止process_request的执行，开始执行process_response
            Request对象，停止中间件的执行，将Request重新调度器
            raise IgnoreRequest异常，停止process_request的执行，开始执行process_exception
        """
        pass

    def process_response(self, request, response, spider):
        """
        数据下载完成，返回spider前执行
        :param response:
        :param result:
        :param spider:
        :return: 
            Response 对象：转交给其他中间件process_response
            Request 对象：停止中间件，request会被重新调度下载
            raise IgnoreRequest 异常：调用Request.errback
        """
        print('response1')
        return response

    def process_exception(self, request, exception, spider):
        """
        当下载处理器(download handler)或 process_request() (下载中间件)抛出异常时执行
        :param response:
        :param exception:
        :param spider:
        :return: 
            None：继续交给后续中间件处理异常；
            Response对象：停止后续process_exception方法
            Request对象：停止中间件，request将会被重新调用下载
        """
        return None
```

##### 代码写完后需要到配置文件中添加对应的配置项

```python
DOWNLOADER_MIDDLEWARES = {
   'name.middlewares.TDownloaderMiddleware': 100,
}
需要注意的是优先级一定要比系统的高，因为scrapy自己有个proxy中间件
```

#### ip代理池

首先需要明确代理池的原理，从网页上爬取免费的代理地址数据，在请求时，如果对方服务器，限制访问IP，就从代理池中获取代理地址重新访问

网络上有很多线程的开源代理池，这里以IPProxyPool 为例

下载地址：https://github.com/qiyeboy/IPProxyPool

1.下载代理池

2.安装依赖

​	在代代理池目录中找到requirements.txt 复制其路径 执行以下命令	

​	pip3 install -r 文件路径

3.下载webpy https://codeload.github.com/webpy/webpy/zip/py3

​	安装webpy

​	切换目录到webpy文件夹中执行以下命令

​	python setup.py install

4.运行IPProxy.py文件开始爬取ip

​	执行过程可能报错，根据错误信息安装对应的模块即可

5.在项目中请求代理池的接口获取代理ip

```python
import requests,random
ips = None
def get_proxy():
    global ips
    if not ips:
        ips = requests.get("http://127.0.0.1:8001/").json()
    a = random.choice(ips)
    return "http://"+a[0]+":"+str(a[1])

def delete_ip(ip):
    ip = ip.strip("http://").split(":")[0]
    res = requests.get("http://127.0.0.1:8001/delete?ip="+ip).json()
    print(res)

if __name__ == '__main__':
    # print(get_proxy())
    #delete_ip("http://60.184.34.232:9999")
```
















