# 20、Rest Formwork_RESTful学习

## 一 、RESTful 的认识

```
-- 1.  是一种规范

-- 2. 面向资源编程：把网络中的所有的东西，都看作为是资源 
```

## 二、 RESTful 的规范

```
1. API与用户的通信协议，总是使用HTTPs协议:https比http安全

2 域名 
	https://api.example.com  尽量将API部署在专用域名（会存在跨域问题）
	https://example.org/api/  API很简单
	例如写一个查询所有图书的api接口:https://api.example.com/books
							   https://127.0.0.1/api/books
											
											
3. 版本:每个接口都应该有版本
			URL，如：https://api.example.com/v1/   
            https://127.0.0.1/api/v2/books(推荐用这种)
			请求头 跨域时，引发发送多次请求
			
			
4. 路径，视网络上任何东西都是资源，均使用名词表示（可复数）
			https://api.example.com/v1/books
			https://api.example.com/v1/animals
			https://api.example.com/v1/employees
			
			不能这么写:
				-获取所有图书:https://127.0.0.1/api/get_all_books
				-新增一本书:https://127.0.0.1/api/add_book
			同一都用这个:
			https://api.example.com/v1/books
			
			
5. method
			GET     ：从服务器取出资源（一项或多项）
			POST    ：在服务器新建一个资源
			PUT     ：在服务器更新资源（客户端提供改变后的完整资源）
			PATCH   ：在服务器更新资源（客户端提供改变的属性）
			DELETE  ：从服务器删除资源
			
			
6. 过滤，通过在url上传参的形式传递搜索条件
			https://api.example.com/v1/zoos?limit=10：指定返回记录的数量
			
7. 状态码

200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
			
			
			请求回去,需要有状态码
			自定义状态码
			status: 100表示成功
					101表示用户名密码错误
					102我也不知道什么错误
					
					
8. 错误处理，应返回错误信息，error当做key。
			-{status:100,error:'错误信息写上'}
			
9. 返回结果，针对不同操作，服务器向用户返回的结果应该符合以下规范。
			GET /books：返回资源对象的列表（数组）
			GET /books/1：返回单个资源对象
			POST /books：返回新生成的资源对象    -新增,传数据,一旦新增完成,把新的资源对象返回
			PUT /books/1：返回完整的资源对象
			PATCH /books/1：返回完整的资源对象
			DELETE /books/1：返回一个空文档
			
			
10. Hypermedia API，RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。
				{
					status:100
					msg:成功
					url:127.0.0.1/books/1
				}
			   核心:返回结果中提供链接
```

## 三、基于Django写RESTful规范接口

### 1.postman软件

```
-- 是一种模拟发送请求的软件(在开发测试的时候会用到)
```

### 2.实现数据的增删改查

```python
from django.views import View
from django.http import  JsonResponse
from app01 import models
class Books(View):
    #得到数据
    def get(self,request):
        respose = {'static':100,'data':None}
        books=models.Book.objects.all()
        ll = [{'name':book.name,'price':book.price} for book in books]
        respose['data']=ll
        return  JsonResponse(respose)

    #  数据的修改
    def put(self, request, pk):
        // django不会帮我们解析body内的数据，需要自己处理，
       //  在使用postman软件的时候，需要注意传输数据的方式和请求的方式的切换
        import json
        data = json.loads(str(request.body, encoding='utf-8'))
        name = data.get('name')
        price = data.get('price')
        ret = models.Book.objects.filter(pk=pk).update(name=name, price=price)
        return JsonResponse({'status': 100, 'msg': '修改成功'})

    #删除数据
    def delete(self,request,pk):
        print(pk)
        models.Book.objects.filter(id = pk).delete()
        return JsonResponse({'status': 100, 'msg': '删除成功'})

    #增加数据
    def post(self,request):
        import json
        data = json.loads(str(request.body, encoding='utf-8'))
        name = data.get('name')
        price = data.get('price')
        models.Book.objects.create(name=name,price=price)
        return JsonResponse({'status': 100, 'msg': '新增成功'})
    
    
  
// url.py文件的路由的编写
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    // get方法
    url(r'^books/$', views.Books.as_view()),
    // put方法(修改)
    url(r'^books/(?P<pk>\d+)/$', views.Books.as_view()),
    // delete（删除）
    url(r'^books/delete/(?P<pk>\d+)$', views.Books.as_view()),
    // post(增加)
    url(r'^books/post/$', views.Books.as_view()),
]
```

## 四、幂等性

```python
1. 什么是幂等性:# 就是你操作无数波操作和你操作一波效果一毛一样的
	

2. 那如何做到幂等性处理呢？关键所在是他们有唯一的区别性id之类的，比如唯一的订单号，可以防止你多次支付

   解决方案：
    #1）当你提交之后，按钮给你变成不可按的

    #2）每当你访问一个页面时，生成一个token（唯一的），储存在redis，为了和你传过来的token对比真实性。如果你多次提交，在redis上如果存在这个token说明你已经提交一次了，再次提交就失效了。
    
3. 具体的案例：
   
    get 获取数据 #幂等

    post 在服务器新建数据 #非幂等

    put 修改服务器中数据  #发送的完整数据 幂等

    patch 修改服务器中的数据 #发送要修改的部分数据 幂等

    delete 删除服务器的数据  #幂等

    option 询问服务器支持的请求方式与返回数据格式

    head 与get 对应 仅返回 响应头

```

## 五、CBV 的源码分析

```python
   #1. Class Base View(基于类的视图) 
   #2. Function Base View(基于函数的视图)
    
	3.def as_view 类方法的返回的值是他内部view函数(闭包函数)的内存地址
    
	4. def view:类方法内部,闭包函数定义:内层函数包含对外部作用域的引用
            
	5. hasattr(self, 'get')--判断self类中是不是有该(get)方法  
	
    6. 反射 setattr(self,get,get_all):相当于把get函数,变成了get_all 
	
    7. getattr(self, 'get'):拿到get函数的内存地址
        
	8. def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
		#执行:dispatch:谁的dispatch方法?写的cbv的那个c,视图中的那个视图类
		#我这个类如果没有写dispatch,会执行View中的dispatch方法
		return self.dispatch(request, *args, **kwargs)
    
	9. def dispatch(self, request, *args, **kwargs):
            #request.method 前台请求的方法,转成了小写
            #http_method_names View中定义的一个列表:是一堆请求方式
            if request.method.lower() in self.http_method_names:
                #getattr的第三个参数是默认值:self.http_method_not_allowed
                #拿到get方法的内存地址
                handler = getattr(self, request.method.lower(),                                                    self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            #get(request,*args, **kwargs)
            return handler(request, *args, **kwargs)

	
    
    总结:*******请求来了--->as_view---->view---->dispatch--->分发到不同的函数,执行函数,拿到结果,然后返回
```

