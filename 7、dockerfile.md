# dockerfile

## 1. 简介

```
 Docker通过读取Dockerfile里面的内容可以自动build image，Dockerfile是一个包含了build过程中需要执行的所有命令的文本文件。也可以理解为Dockfile是一种被Docker程序解释的脚本，由一条一条的指令组成，每条指令对应Linux系统下面的一条命令，由Docker程序将这些Dockerfile指令翻译成真正的Linux命令。
Dockerfile有自己书写格式和支持的命令，Docker程序解决这些命令间的依赖关系，类似于Makefile。Docker程序将读取Dockerfile，根据指令生成定制的image。相比image这种黑盒子，Dockerfile这种显而易见的脚本更容易被使用者接受，它明确的表明image是怎么产生的。有了Dockerfile，当我们需要定制自己额外的需求时，只需在Dockerfile上添加或者修改指令，重新生成image即可，省去了敲命令的麻烦。
```

## 2. 指令介绍

```Python
# FROM:指定基础镜像
  FROM centos:6.9 
  FROM centos@镜像ID 安全性高(有版本控制)
  
# RUN: 构建镜像过程中运行的命令
  RUN apt-get update && apt-get install -y apt-utils # 执行bash的命令
  RUN ["mysql", "--initialize-insecure", "--user=mysql", "--nasedir=/usr/local/mysql", "--datadir=/data/mysql/data "] # 执行非bash的命令
  
# ADD:拷贝本地文件到容器里面(如果是压缩文件会自动解压tar.gz tar.xz 只拷贝目录下的子目录)
   ADD bbs.tar(宿主机的文件) /var/www/html/(容器的目录, 目录不存在会自动创建)
   ADD “文件的源” /tmp

# COPY:拷贝本地文件到容器里面(拷贝的文件需要和dockerfile同一目录，只拷贝目录下的子目录)
   COPY index.py(宿主机的文件) /var/www/html/(容器的目录)
 
# VOLUME:挂载功能
   VOLUME ['apache2','/var/log/apache2']

# WORKDIR:切换设置工作的目 类似于cd 
   WOKRDIR /path/app

# ENV:系统环境
   ENV BASE_DIR /var/ap
 
# USER:切换用户
 
# EXPOSE：向外暴露的端口
	EXPOSE 20
 
# CMD:使用镜像启动容器时运行的命令 【“执行的命名”,“参数”】可以被替代
  CMD ['/usr/sbin/sshd' , "-D"]
  CMD ['/bin/bash' , "/init.sh"]
  
# ENTRYPORT:使用镜像启动容器时运行的命令，不可以被替代
 ENTRYPOINT ["apache2ctl", "-D", "FOREGROUND"]
  
# 应用dockerfile
docker images build -t "jxl/test:v1" ./
```