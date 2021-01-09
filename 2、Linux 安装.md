# Linux 下docker的安装

## 1. 环境准备

```
curl  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo

wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

## 2. 安装依赖包

```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum list docker-ce.x86_64 --showduplicates | sort -r
```

## 3.安装docker-ce

```
yum install -y --setopt=obsoletes=0 \
docker-ce-17.03.2.ce-1.el7.centos.x86_64 \
docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch
```

## 4.配置镜像加速

```
阿里云Docker-hub

https://cr.console.aliyun.com/cn-hangzhou/mirrors
mkdir -p /etc/docker

tee /etc/docker/daemon.json <<-'EOF'
{
   "registry-mirrors": ["https://68rmyzg7.mirror.aliyuncs.com"]
}
EOF   
          
或者:
vim   /etc/docker/daemon.json

    {
         "registry-mirrors": ["https://68rmyzg7.mirror.aliyuncs.com"]
    }
```

## 5. 启动docker服务

```
systemctl daemon-reload
systemctl restart docker
docker version
docker  info
```

