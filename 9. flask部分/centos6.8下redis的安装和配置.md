# centos6.8下redis的安装和配置

## 下载、安装

在[redis官网](https://redis.io/)可以获取到最新版本的redis

进入/usr/local/目录，执行如下命令

```
wget http://download.redis.io/releases/redis-4.0.2.tar.gz
tar xzf redis-4.0.2.tar.gz
cd redis-4.0.2
make
```

执行make构建redis时报如下错误，这是因为没有安装gcc,执行如下命令即可解决

错误： make[3]: gcc：命令未找到
解决： yum install -y wget gcc make tcl //安装gcc

    错误： make[3]: gcc：命令未找到
    解决： yum install -y wget gcc make tcl //安装gcc

继续执行make又报错，这是因为构建redis的默认内存分配器是jemalloc，如果系统中没有jemalloc，就会报错，可以在构建时将内存分配器设置成libc

```
错误： zmalloc.h:50:31: 错误：jemalloc/jemalloc.h：没有那个文件或目录
解决： make MALLOC=libc  //构建时指定内存分配器
```

## 启动redis服务

### 使用默认配置文件启动redis服务

执行完make命令后，redis就安装完毕了，在安装目录/usr/local/redis-4.0.2目录下执行下面的命令，如果成功启动redis服务，说明redis安装成功 

```
redis-server
```

### 指定配置文件启动redis服务

创建如下目录，存放配置文件、日志文件、进程文件、工作文件（如数据备份） 

```
mkdir /etc/redis
mkdir /var/redis
mkdir /var/redis/log
mkdir /var/redis/run
mkdir /var/redis/6379
```

复制一份配置文件到/etc/redis目录 

```
cp redis.conf /etc/redis/6379.conf
```

修改配置文件6379.conf 

```
daemonize yes //将redis服务设成守护进程 
requirepass 123456 //设置认证密码 
bind 0.0.0.0 //设置监听所有ip，默认为bind 127.0.0.1，只监听本机ip，其他主机无法访问此redis，因为我要远程操作redis，所以暂时改成0.0.0.0 
protected-mode no //关闭保护模式，默认启用保护模式，同样要想远程访问redis，必须设成no pidfile /var/redis/run/redis_6379.pid 
logfile /var/redis/log/redis_6379.log 
dir /var/redis/6379

```

使用6379.conf启动redis服务 

```
redis-server /etc/redis/6379.conf
```

## 关闭redis服务

### 直接杀死redis服务进程

```
#查看运行的redis服务，得到redis服务的进程号，假设是1000
ps -ef|grep redis
#杀死redis进程
kill -9 1000
```

### 使用redis客户端关闭

```
redis-cli –h localhost –p 6379 –a 123456 shutdown
```

## 注意

远程访问redis服务，redis主机需要对外开放6379端口号或者直接关闭防火墙，否则会连接失败

开放6379端口号

```
/sbin/iptables -I INPUT -p tcp --dport 6379 -j ACCEPT #开启6379端口
/etc/rc.d/init.d/iptables save #保存配置
/etc/rc.d/init.d/iptables restart #重启服务
```

```
service iptables stop   #关闭防火墙
service iptables status #查看防火墙状态
service iptables start  #启动防火墙
```