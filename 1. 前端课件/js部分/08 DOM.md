# DOM

## 一、JS中标签关系

```html
<div class="sup">
    <div class="sub1"></div>
    <div class="sub2"></div>
    <div class="sub3"></div>
</div>

<script>
	var sub2 = document.querySelector('.sub2');
    // 父级标签
	console.log(sub2.parentElement);
    // 上一个标签
	console.log(sub2.previousElementSibling);
    // 下一个标签
	console.log(sub2.nextElementSibling);

	var sup = document.querySelector('.sup');
    // 所有子标签
	console.log(sup.children);
    // 第一个子标签
	console.log(sup.firstElementChild);
    // 最后一个子标签
	console.log(sup.lastElementChild);
</script>
```

## 二、JS操作页面标签

```js
// 创建一个div标签
var div = document.createElement("div");
// 添加到body末尾，返回自身
div = body.appendChild(div);
// 插入到body中box标签前，返回自身
div = body.insertBefore(div, box);
// 替换掉body中box标签，返回box
box = body.replaceChild(div, box);
// 在body中移除div，返回自身
div = body.removeChild(div);
```

## 三、JS操作DOM一般步骤

#### 1、创建标签

#### 2、设置标签样式文本

#### 3、添加到页面指定位置