# Git

## 一、控制版器的介绍即分类

```
---介绍：
控制版本器：控制程序员协同工作的一个工具


--分类：
1. CVS(90年代 收费)

2. SVN：集中式版本控制器(所有的代码发布到听同一个服务器上)
		缺点：万一断电了，就得不到最新的代码

3. Git：分布式版本控制器
        本机上和服务器上都要一个最新的代码
        
        
Git与SVN的区别：Git服务器是提供开发者交换代码的，服务器的数据丢了，没关系（在本机上也有最新的代码）
```

## 二、Git的安装

```
https://www.git-for-windows.github.io/ 下载软件，双击，一路“Next”完毕，安装成功！
```

## 三、Git的使用

```
----- 将代码上传到远程库中


1. Git的配置

	$git config --global user.name jxl
	$git config --global user.emali 1915735292@qq.com 
	
2.创建本地创库

		--先进入一个事先创建好的文件夹（madir text | cd text ）
		--git init (会创建一个Git的隐藏文件)
		
3. 添加文件

		--在text文件夹中添加一个py文件
	
4. 查看文件的状态
		
	 -- Git status（ 此时，Git发现有一个新的文件，但是并没有将该文件纳入管理）
	 
5. 将文件保存到暂存区

      -- Git add index.py
 
 6.将文件提交到版本库
      
       --Git commit-m '备注的内容' index.py
       
  7.为本地仓库添加远程库
  
        --Git remove add origin  https://gitee.com/jxl951017/text.git（码云的地址）
       
  8. 先得到最新的代码
  
  		--git pull origin master
  		
  9. 将最新的代码上传到远程库中
  
  		--Git push origin master -f(强行上传)
  		
  	
  ----开始协同开发
  
   10.clone 一份代码到自己的本地
   
      -- 先进入一个事先创建好的文件夹
      -- git clone https://gitee.com/jxl951017/text.git（别人码云的地址）
      
   11.拉下所有的代码
    
    	--git pull origin master
    	再按照上面的步骤操作
    	
   
    	
  	 -----分支的创建与使用
     
     12. 查看分支
     	
     		Git	branch
     	
     13. 创建分支
      
          git branch dev(分支的名字)
         
      14. 切换分支
      
           git chechout dev(分支的名字)
  
       15. 合并分支
       
          git merge dev(分支的名字)
          
          
  
  
       
       
		 
		
	


```

