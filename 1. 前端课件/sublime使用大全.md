# Sublime使用大全

## 一、sublime快捷键

- 复制行

```
win -- ctrl + shift + d
mac -- cmd + shift + d
```

- 剪切行 \| 删除行 

```
win -- ctrl + x | ctrl + shift + k
mac -- cmd + x | ctrl + shift + k
```

- 移动行

```
win -- ctrl + shift + ↑ 或 ctrl + shift + ↓
mac -- cmd + ctrl + ↑ 或 cmd + ctrl + ↓
```

- 注释

```
win -- ctrl + /
mac -- cmd + /
```

## 二、插件

#### 1、package control（插件管理器）

- 安装

```
1.打开控制台：ctrl + `
2.粘贴官网安装指令：https://packagecontrol.io/ -> Install Now
3.回车执行
```

```
import urllib.request,os,hashlib; h = '6f4c264a24d933ce70df5dedcf1dcaee' + 'ebe013ee18cced0ef93d5f746d80ef60'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```

- 使用

```
1.打开全局命令：ctrl + shift + p | cmd + shift + p
2.安装指令：install package -> 搜索指定插件 -> 回车安装
3.卸载指令：remove package -> 选取指定插件 -> 回车卸载
```

#### 2、emmet（快捷Tap）

- 使用

```
输入指定语法格式，tap补全
父子 >
兄弟 +
编号 $
重复 *n
内容 {}
属性 []
支持标签、class、id选择器语法
```

#### 3、SideBarEnhancements(工具栏)

- 使用

```
① 增强右键
② 浏览器快捷打开
Preferences -> Key Bindings -> json语法数据
win
[
	// Chrome
    { "keys": ["control+1"], "command": "side_bar_files_open_with",
        "args": {
            "paths": [],
            "application": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "extensions":".*"
        }
    }
]
mac
[
	// Chrome
    { "keys": ["command+1"], "command": "side_bar_files_open_with",
        "args": {
            "paths": [],
            "application": "/Applications/Google Chrome.app",
            "extensions":".*"
        }
    }
]
```

#### 4、Material Theme（主题）

#### 5、A File Icon（图标）

#### 6、HTML-CSS-JS Prettify（代码格式化）

```
需要NodeJS环境
登录Node官网安装Node环境
```

#### 7、JavaScript & NodeJS Snippets（代码片段）

#### 8、AutoFileName（文件路径提示）

#### 9、TrailingSpaces（高亮多余空格）



