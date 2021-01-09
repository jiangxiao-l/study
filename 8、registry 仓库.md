# registry 仓库

# 构建私有的registry

## 1. 启动registry容器

```Python
# --restart=always 重启docker的时候可以自启动***
docker run -d -p 5000:5000 --restart=always --name registry -v /opt/registry:/var/lib/registry registry
```

## 2. 修改配置文件

```python
# 修改配置文件 nsecure-registries：本地的地址和暴露的端口
{
   "registry-mirrors": ["https://68rmyzg7.mirror.aliyuncs.com"],
   "insecure-registries": ["10.0.0.100:5000"]
}
# 重启服务
systemctl  restart docker
```

## 3. 制作本地镜像并push

```python 
# 命名一个新的images IP地址：端口/jxl(项目名)/nginx:v1
docker tag nginx:latest 10.0.0.100:5000/jxl/nginx:v1
# 上传镜像
docker push 10.0.0.100:5000/jxl/nginx:v1
```

## 4. 异地进行pull镜像

```python
docker pull 10.0.0.100:5000/jxl/nginx:v1
```

## 5. 本地方库加安全认证

```python
# 安装HTTP的工具包
yum install httpd-tools -y
# 生成密钥目录
mkdir -p /opt/registry-auth/ 
# 写入账号和密码
htpasswd -Bbn jxl(账号) 123(密码) > /opt/registry-auth/htpasswd
```

## 6.重新启动带有秘钥功能的registry容器

```python
# 删除所有的容器
docker container rm -f `docker container ls -a -q`
# 启动一个新的容器
docker run -d -p 5000:5000 -v /opt/registry-auth/:/auth/ -v /opt/registry:/var/lib/registry  --name register-auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" registry 
```

## 7.push镜像,需要进行login

```python
# 登入
docker login 10.0.0.100:500(jxl 123)
# 打tag
# 推送镜像
docker push 10.0.0.100:500/jxl/centos:v1
```

## 8.habor实现图形化register

```Python
# 安装docker和docker-compose
 yum install -y docker-compose 
# 下载harbor-offline-installer-vxxx.tgz
# 上传到/opt,并解压
# 修改harbor.cfg配置文件
  hostname = 10.0.0.11
  harbor_admin_password = 123456
# 执行install.sh
```

