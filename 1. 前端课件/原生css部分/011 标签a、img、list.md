# 标签a、img、list

## 一、a标签

#### 1、常用用法

```html
<a href="https://www.baidu.com">前往百度</a>
<a href="./index.html">前往主页</a>
```

#### 2、相对路径

```
以当前文件作为参考，.代表当前路径，..代表上一级目录
```

#### 3、常用属性

```
title -- 链接说明
target -- _self | _blank -- 目标位置
```

#### 4、其他用法

- mailto：邮件给...
- tel：电话给...
- sms：信息给...

#### 5、a标签reset操作

```css
a {
    color: #333;
    text-decoration: none;
}
```

#### 6、锚点

```html
① <a href="#tag">前往锚点</a> <a name="tag" des="锚点"></a>
② <a href="#tag">前往锚点</a> <i id="tag" des="锚点"></i>
```

#### 7、鼠标样式

```css
{
    cursor: pointer | wait | move;
}
```

## 二、img标签

#### 1、常用用法

```html
<img src="https://image/icon.gif" />
<img src="./icon.gif" />
```

#### 2、常用属性

```
alt -- 异常解释
title -- 图片解释
```

## 三、list列表

#### 1、有序列表

```html
<ol>
	<li></li>
	<li></li>
</ol>
```

#### 2、无序列表

```html
<ul>
	<li></li>
	<li></li>
</ul>
```

#### 3、list的reset操作

```css
ol, ul {
	margin: 0;
    padding: 0;
    list-style:none;
}
```





