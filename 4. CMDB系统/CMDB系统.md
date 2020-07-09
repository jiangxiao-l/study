# CMDB系统

## 1.前言

```python
传统的运维：
   1. 项目的上线:
         a.产品经理前期的调研 --> 需求分析
         b. 和开发进行评审
         c. 开发人员进行开发
         d. 测试人员进行测试
         f. 上线
           
  
自动化运维的系统：
   1. 自定分布代码系统
   2. 报警自动化系统
   3. 装机自定化系统
    
注：以上的系统都要知道每台服务器上的详细信息 --> CMDB系统


如何保存服务器上的元信息：
    1. Excel --> 人为干预太严重，统计的时候也会有问题
    2. 开发自动化收集信息，并记录的系统 --> CMDB
 


```

## 2. CMDB的目的

```python 
#目的：实现数据的自动化收集和数据的记录           
```

## 3. 开发中收集信息的四种方式(重点)

###   3.1   agent方法

```python 
1.简介：
   可以将服务器上的Agent程序作定时任务，定时将资产信息提交到指定的API记录到数据库中

2. 流程：
   在每一台的服务器上装上agent脚本(主要是利用Python中的subprocess.getoutput()模块，执行系统的命令)，将得到的服务器的数据利用requests模块，传递给API服务器保存到db(数据库)中,还有一个web的界面给用户看。(可以另利用Python中的Django框架进行数据的熏染)。
   
 3.优点：速度块（可以开多个进程，实现数据的传递）
 
 4.缺点：需要在每台服务器上安装agent脚本
 
 5.使用的场景：服务器多的情况下
        
   
```

![](C:\Users\ASUS\Desktop\学习资料\CMDB系统\图片\agent.png)

### 3.2  paramiko的方法

```python
1.简介：paramiko(用Python写的一个模块)，底层也是利用ssh的连接方式，与xshell(软件)类似。于此类似的还有ansible,farbic

2.流程：
   在一台安装有paramiko的中控机服务器上，通过ssh登入到每台服务上的面，可以执行命令得到服务器的信息，并通过requests模块将数据传递给API服务器,并保存到数据库中。还有一个web的界面给用户看。(可以另利用Python中的Django框架进行数据的熏染)。
   
   
3. 优点：不需要载每台服务器上面安装agent脚本。

4. 缺点：受限于网络，速度慢

5. 应用场景：服务器少
```

![](C:\Users\ASUS\Desktop\学习资料\CMDB系统\图片\paramiko.png)

### 3.3  saltstack的方法

```python
1. 简介：saltstack是一个利用python写的一个软件。

 2.流程：首先在中控机上安装saltstack(master)，在每台的服务器上安装 minion（slave）。在         中控机发送命令给服务器执行。服务器将结果放入另一个队列中，中控机获取将服务信息发送         到API进而录入数据库，还有一个web的界面给用户看。(可以另利用Python中的Django框架         进行数据的熏染)。
 
 3.优点：直接使用现有的软件，不需要自己写脚本
 
 4.缺点：需要在每太服务器上安装该软件
 
 5.适应场景：公司以前服务器上装有此软件的
       
```

#### 3.3.1 saltstack的使用

```python
master端：(中控机)
"""
1. 安装salt-master
    yum install salt-master
2. 修改配置文件：/etc/salt/master
    interface: 0.0.0.0    # 表示Master的IP 
3. 授权
     salt-key -A  -->接受所有的 minion-key
4. 启动
    service salt-master start
"""

slave端：(服务器)
"""
1. 安装salt-minion
    yum install salt-minion
    
2. 修改配置文件 /etc/salt/minion
    master: 10.211.55.4           # master的地址
    或
    master:
        - 10.211.55.4
        - 10.211.55.5
    random_master: True
    id: c2.salt.com                    # 客户端在salt-master中显示的唯一ID
3. 启动
    service salt-minion start
"""


授权：
salt-key -L                # 查看已授权和未授权的slave
salt-key -a  salve_id      # 接受指定id的salve
salt-key -r  salve_id      # 拒绝指定id的salve
salt-key -d  salve_id      # 删除指定id的salve



执行命令：
  
  在master上执行命对salve进行远程的操作:   salt 'jxl_1' cmd.run 'ifconfig'
  
  
 
```

![](C:\Users\ASUS\Desktop\学习资料\CMDB系统\图片\saltstack.png)

### 3.4 puppet（了解）

```python
1. 工作的流程和saltstack类似 

2. 是一各比较老的方法，不建议在使用

3. puppet是使用Ruby（日本人开发的一门语言）写的。默认会每隔30分钟发一次数据
```

## 4. AES加密

```python
#前期工作：
        1、pip3 install pycrypto(在windows中装不了)
    
		2. https://github.com/sfbahr/PyCrypto-Wheels
		
        3. 下载与python同版本的代码(在命令行中查看Python中的版本：python3)
        
        4. pip3 install wheel（安装必要的模块）
       
		4. 进入目录(下载的文件目录)：
        
		5. pip3 install pycrypto-2.6.1-cp35-none-win32.whl





#解密函数：
def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) 
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')


#加密函数：
 def encrypt(message):
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    ba_data = bytearray(message,encoding='utf-8')
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):
        ba_data.append(v3)
     # 注：有时候decode可以不用加，看情况
    final_data = ba_data.decode('utf-8')
    msg = cipher.encrypt(final_data) # 要加密的字符串，必须是16个字节或16个字节的倍数
    return msg
```

## 5. Disk内容的录入

```python
import hashlib

import time
from django.shortcuts import render,HttpResponse
import json
from repository import models

from django.conf import settings

key_record = {
    # "3f090e8ea65e84297b4f724401c82b39|1545121938.720341" : 1545121948.720341
}
# AES的解密：
def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg)
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

# 数据的发送和数据的接收
def asset(request):
    if request.method == 'GET':
        token = settings.TOKEN
        # 第三种方式：也是发送一个令牌，但是判断时间，并且把访问过的令牌放入到一个列表中
        client_key, client_ctime = request.META.get('HTTP_TOKEN').split('|')
        client_ctime = float(client_ctime)

        server_ctime = time.time()
        # 判断时间是否已经超过了规定的时间(可以放在redis中设置一个过期时间)
        if server_ctime - client_ctime > 100000:
            return HttpResponse('【第一关】超时了')

        tmp = "%s|%s" % (token, client_ctime)
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        server_key = m.hexdigest()
        # 验证传过来的token信息是否是一样的
        if server_key != client_key:
            return HttpResponse('【第二关】动态令牌验证错误')
        #将多余的数据进行删除
        for k in list(key_record.keys()):
            value = key_record[k]
            if server_ctime > value:
                del key_record[k]

       
        if client_key in key_record:
            return HttpResponse('[第三关] 该令牌已经被别人使用过了')
        else:
            key_record[client_key] = client_ctime + 100000

        return HttpResponse('非常重要的数据...')

    elif request.method == 'POST':

        info = decrypt(request.body)
        
        server_info = json.loads(info)


        hostname = server_info['basic']['data']['hostname']
         # 得到该服务器的对象
        server_obj = models.Server.objects.filter(hostname=hostname).first()

  
        if not server_obj:
            return HttpResponse('当前主机名未录入')
         # 判断数据收集的时候还是否数据收集有错误
        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(asset_obj=server_obj.asset, content=server_info['disk']['data'],title="[%s]硬盘采集错误信息"%hostname)

         # 传过来的disk的数据
        new_disk_list = server_info['disk']['data']

        # 数据库上已经存在的disk的数据
        old_disk_list = server_obj.disk.all()

      
        # 新的槽位列表[1,2,3,4,5]
        new_slot_list = list(new_disk_list.keys())

        # 旧的槽位列表
        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        '''
            1. 删除（差集）：
                   旧的：[1,2,3]
                   新的：[1,2]
                   
            2. 增加 （差集）:
                   旧的：[1,2,3]
                   新的：[1,2,3,4]
                   
            3. 更新 （交集）：[5,4]
                 其实就是相同的部分
                 
        '''

        # 1. 增加 (差集)
        add_list = set(new_slot_list).difference(old_slot_list)

        # 存入数据库表disk
        if add_list:
            disk_res = {}
            record_list = []
            for slot in add_list:
                disk_res = new_disk_list[slot]
                disk_res['server_obj'] = server_obj

                models.Disk.objects.create(**disk_res)

                tmp = "新增硬盘：槽位{slot} 容量{capacity} 型号{model} 类型{pd_type}".format(**disk_res)
                record_list.append(tmp)

            content = ",".join(record_list)
            models.AssetRecord.objects.create(asset_obj = server_obj.asset, content = content)


        # 2. 删除 （差集）
        del_list = set(old_slot_list).difference(new_slot_list)

        # 从表disk删除不存在的数据
        if del_list:
            models.Disk.objects.filter(slot__in=del_list, server_obj=server_obj).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content='删除硬盘:%s' % (",".join(del_list)))


        # 3. 更新（交集）
        update_list = set(old_slot_list).intersection(new_slot_list)
       

        record_list = []
        row_map = {'capacity':'容量', 'pd_type':'类型', 'model':'型号'}
        if update_list:

            for slot in update_list:
                # 新的数据，是一个字典
                new_disk_row = new_disk_list[slot]
                # 数据库中的数据
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()

                for k, new_v in new_disk_row.items():
                    # k: capacity;slot;pd_type;model
                    # v: '476.939''xxies              DXM05B0Q''SATA'
                    old_v = getattr(old_disk_row, k)

                    if new_v != old_v:
                        setattr(old_disk_row, k, new_v)
                        record_list.append("槽位%s, %s由%s变为%s" % (slot, row_map[k], old_v, new_v,))
                old_disk_row.save()

            if record_list:
                models.AssetRecord.objects.create(asset_obj = server_obj.asset, content=";".join(record_list))


    return HttpResponse('.....')
```



## 6.其他知识点的补充

```python
1.定时的执行的脚本：
  crontab:
      分 时 日 月 周 年
      21 17 * *  * *  pyton3 text.py >>（追加）a.txt
        
2. vim 中在命令行模式下： ':! ifconfig' --> 可以直接执行命令


3. 利于画图： （echars, highchars：模块）,(draw.io, processon：网站) 
              阿里的可视化网页(可以观看)


```

