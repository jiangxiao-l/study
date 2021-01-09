# 本地yum源优化

## 1. 安装vsftp软件

```
yun install -y vsftpd
```

## 2. 启动ftp

```
systemctl enable vsftpd
systemctl start vsftpd
```

## 3. 配置yum仓库

```
mkdir -p /var/ftp/centos.6.9
mkdir -p /var/ftp/centos.7.5
cat >/yum.repo.d/ftp.repo <<EOF
[ftp]
name=ftpbasde
baserurl=ftp://10.0.0.100/centos.6.9
enabled=1https://zhuanlan.zhihu.com/p/31895797https://www.wenmi.com/niandugerenzongjiebaogao/
gpgcheck=0
EOF
```

## 4. 系统盘的挂载

```
mount -o loop /mnt/Centos.6.9.iso  /var/ftp/centos.6.9
```