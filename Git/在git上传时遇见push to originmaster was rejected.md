#### 在git上传时遇见Push to origin/master was rejected

```
首先是你的项目中有和和历史不符的东西 
Push rejected: Push to origin/master was rejected 
推拒绝：推送到起源/主人被拒绝 
直接是解决办法，直接打开你要上传代码的文件夹位置鼠标右键git Bash Here然后直接下面两行命令解决问题

git pull origin master –allow-unrelated-histories 

git push -u origin master -f
```

