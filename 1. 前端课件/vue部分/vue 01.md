# vue

## 一、认识Vue

定义：一个构建数据驱动的 web 界面的渐进式框架

优点：

1、可以完全通过客户端浏览器渲染页面，服务器端只提供数据

2、方便构建单页面应用程序（SPA）

## 二、引入Vue

```html
<div id="app">
	<p title="p"></p>
	<p v-bind:title='title'></p>
</div>
<script type="text/javascript" src="vue.js"></script>
<script>
    new Vue({
    	el: '#app',
   		data: {
    		title: 'vue-p'
    	}
    })
</script>
```

## 三、Vue实例

- 实例：el

```html
<div id='app'>
    
</div>
<script>
    new Vue({
    	el: '#app'
    })
</script>
```

- 数据：data

```html
<div id='app'>
    <p v-text='msg1'></p>
    <p>{{ msg2 }}</p>
</div>
<script>
    new Vue({
    	el: '#app',
    	data: {
    		msg1: '段落1',
    		msg2: '段落2'
    	}
    })
</script>
```

- 方法：methods

```html
<div id='app'>
    <p v-on:click='func'>{{ msg }}</p>
</div>
<script>
    new Vue({
    	el: '#app',
    	data: {
    		msg: '段落'
    	},
        methods: {
            func: function() {
                alert(this.msg)
            }
        }
    })
</script>
```

- 计算属性：computed

```html
<div id='app'>
    <div>
        姓：<input type='text' v-model='first_name'>
    </div>
    <div>
        名：<input type='text' v-model='last_name'>
    </div>
    <div>
        全名：<input type='text' v-model='full_name'>
    </div>
</div>
<script>
    new Vue({
    	el: '#app',
    	data: {
    		first_name: '',
            last_name: ''
    	},
        computed: {
            full_name: function() {
            	return this.first_name + this.last_name
        	}
        }
    })
</script>
```

- 监听器：watch

```html
<div id='app'>
    <div>
        姓名：<input type='text' v-model='full_name'>
    </div>
    <p>姓：{{ first_name }}</p>
    <p>名：{{ last_name }}</p>
</div>
<script>
    new Vue({
    	el: '#app',
    	data: {
    		full_name: '',
            first_name: '',
            last_name: ''
    	},
        watch: {
            full_name: function() {
            	this.first_name = this.full_name.split(' ')[0];
                this.last_name = this.full_name.split(' ')[1];
        	}
        }
    })
</script>
```

- 分隔符：delimiters

```html
<div id='app'>
    ${ msg }
</div>
<script>
    new Vue({
    	el: '#app',
    	data: {
    		msg: 'message'
    	},
        delimiters: ['${', '}']
    })
</script>
```

- 实例对象使用成员属性与方法

```html
<script>
    var app = new Vue({
    	el: '#app',
    	data: {
    		msg: 'message'
    	}
    })
    console.log(app)
    console.log(app.$el)
    console.log(app.$data.msg)
    console.log(app.msg)
</script>
```

## 四、实例生命周期钩子

- 定义

```html
每个 Vue 实例在被创建时都要经过一系列的初始化过程——例如，需要设置数据监听、编译模板、将实例挂载到 DOM 并在数据变化时更新 DOM 等。同时在这个过程中也会运行一些叫做生命周期钩子的函数，这给了用户在不同阶段添加自己的代码的机会。
```

- 钩子方法

```html
beforeCreate：在实例初始化之后，数据观测 (data observer) 和 event/watcher 事件配置之前被调用。

created：在实例创建完成后被立即调用。在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。然而，挂载阶段还没开始，$el 属性目前不可见。

beforeMount：在挂载开始之前被调用：相关的 render 函数首次被调用。

mounted：el被新创建的vm.$el替换，并挂载到实例上去之后调用该钩子。

beforeUpdate：数据更新时调用，发生在虚拟 DOM 打补丁之前。

updated：数据更新时调用，发生在虚拟 DOM 打补丁之前。

activated：keep-alive 组件激活时调用。

deactivated：keep-alive 组件停用时调用。

beforeDestroy：实例销毁之前调用。在这一步，实例仍然完全可用。

destroyed：Vue实例销毁后调用。调用后，Vue实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。

errorCaptured：2.5.0+ 新增，当捕获一个来自子孙组件的错误时被调用。此钩子会收到三个参数：错误对象、发生错误的组件实例以及一个包含错误来源信息的字符串。此钩子可以返回 false 以阻止该错误继续向上传播。
```

- 重点钩子

```html
created：实例完全创建完毕(属性与方法都准备就绪)。可以进行数据操作(请求后台数据，重新渲染最新数据)

mounted：虚拟DOM构建完毕，并完成实例的el挂载。可以重新操作页面DOM
```

## 五、视图常规操作

- v-text：文本变量

```html
<p v-text='msg'></p>
<p>{{ msg }}</p>
```

- v-once：一次性文本赋值

```html
<p v-once>{{ msg }}</p>
```

- v-html：html文本变量

```html
<p v-html='msg'></p>
<script>
    new Vue({
        el: '#app',
        data: {
            msg: '<b>文本</b>'
        }
    })
</script>
```

- v-bind：属性绑定

```html
<div id="app">
	<img v-bind:src='imgSrc' />
    <!-- 简写 -->
    <img :src='imgSrc' />
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            imgSrc: 'https://www.baidu.com/favicon.ico'
        }
    })
</script>
```

- v-model：双向数据绑定

```html
<div id="app">
	<input type="text" v-model='msg'>
	<p>{{ msg }}</p>
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            msg: ''
        }
    })
</script>
```

- v-cloak：避免页面加载闪烁

```html
<style>
    [v-cloak] {
        display: none;
    }
</style>
<div id="app" v-cloak>
    
</div>
```

- 视图自身运算

```html
<div id="app" v-cloak>
    <p>{{ 1 + 1 }}</p>
    <p>{{ [1, 2, 3].join('@') }}</p>
</div>
```

## 六、条件渲染

- v-if：值true会被渲染，值false不会被渲染

```html
<div id="app">
	<div v-if='isShow'>div div div</div>
    <button @click='isShow = !isShow'>改变</button>
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            isShow: true
        }
    })
</script>
```

- v-else：与v-if结合使用形成对立面

```html
<div id="app">
	<div v-if='isShow'>div div div</div>
    <div v-else='isShow'>DIV DIV DIV</div>
    <button @click='isShow = !isShow'>改变</button>
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            isShow: true
        }
    })
</script>
```

- v-else-if：变量的多情况值判断

```html
<div id="app">
	<div v-if='tag == 0'>if if if</div>
    <div v-else-if='tag == 1'>else if else</div>
    <div v-else='tag == 2'>else else else</div>
    <input type='number' min='0' max='2' v-model='tag' />
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            tag: 0
        }
    })
</script>
```

- template：不被渲染的vue结构标签

```html
<template v-if="isShow">
    <p>用template嵌套</p>
    <p>可以为多行文本</p>
    <p>同时显隐</p>
    <p>且template标签不会被vue渲染到页面</p>
</template>
```

- v-show：一定会被渲染到页面，以display属性控制显隐
- key：为v-if方式的显隐创建缓存，提高效率

```html
<div id="app">
	<div v-if='tag == 0' key='0'>if if if</div>
    <div v-else-if='tag == 1' key='1'>else if else</div>
    <div v-else='tag == 2' key='2'>else else else</div>
    <input type='number' min='0' max='2' v-model='tag' />
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            tag: 0
        }
    })
</script>
```

## 七、列表渲染

- v-for：循环渲染列表

```html
<div id="app">
	<ul>
		<li v-for='item in items'>{{ item }}</li>
	</ul>
    <button @click='click'>改变</button>
</div>
<script>
    new Vue({
        el: '#app',
        data: {
            items: ['张三', '李四', '王五']
        }，
        methods: {
        	click: function () {
        		this.items.splice(1, 1, '李大大');
        		this.items.pop();
        		this.items.push('赵六')
        	}
        }
    })
</script>
```

- 遍历数组

```html
// items: ['张三', '李四', '王五']

// 值
<ul>
    <li v-for='item in items'>{{ item }}</li>
</ul>
// 值, 索引
<ul>
    <li v-for='(item, index) in items'>{{ index }} - {{ item }}</li>
</ul>
```

- 遍历对象

```html
// {'name': '张三', 'age': 18, 'sex': '男'}

// 值
<div v-for="value in object">
  {{ value }}
</div>
// 值, 键
<div v-for="(value, key) in object">
  {{ key }}: {{ value }}
</div>
// 值, 键, 索引
<div v-for="(value, key, index) in object">
  {{ index }}. {{ key }}: {{ value }}
</div>

```

- 复杂数据渲染

```html
// items: [{'name': '张三'}, {'age': 18}, {'sex': '男'}]
<div>
    <div>{{ items[0].name }}</div>
    <div>{{ items[1].age }}</div>
    <div>{{ items[2].sex }}</div>
</div>
```

