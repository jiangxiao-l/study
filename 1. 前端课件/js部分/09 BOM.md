# BOM

#### 1、窗口操作 open

```js
// 新tag打开目标地址
open("http://www.yahoo.com");
// 自身tag转跳目标地址
open("http://www.yahoo.com", '_self');
// 自定义窗口打开目标地址
open("http://www.yahoo.com", '_blank', 'width=300, height=300');
```

#### 2、历史记录 history

```js
// 历史后退
history.back();
// 历史前进
history.forward()
```

#### 3、导航器 navigator

```js
// 拥有浏览器信息的字符串
navigator.userAgent;
```

#### 4、地址信息 location

```js
// 协议
location.protocol
// 服务器
location.hostname
// 端口号
location.port
// 参数拼接
location.search
```

