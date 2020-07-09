# Vue组件

## 一、组件介绍

- 每一个组件都是一个vue实例
- 每个组件均具有自身的模板template，根组件的模板就是挂载点
- 每个组件模板只能拥有一个根标签
- 子组件的数据具有作用域，以达到组件的复用

## 二、局部组件

```html
<div id="app">
    <local-tag></local-tag>
    <local-tag></local-tag>
</div>
<script>
    var localTag = {
        data () {
            return {
                count: 0
            }
        },
        template: '<button @click="btnAction">局部{{ count }}</button>',
        methods: {
            btnAction () {
                this.count ++
            }
        }
    }
    new Vue({
        el: "#app",
        components: {
            'local-tag': localTag
        }
    })
</script>
```

## 三、全局组件

```html
<div id="app">
    <global-tag></global-tag>
    <global-tag></global-tag>
</div>
<script>
	Vue.component('global-tag', {
		data () {
			return {
				count: 0
			}
		},
		template: '<button @click="btnAction">全局{{ count }}</button>',
		methods: {
			btnAction () {
				this.count ++
			}
		}
	})
    new Vue({
        el: "#app"
    })
</script>
```

## 四、父组件传递数据给子组件

- 通过绑定属性的方式进行数据传递

```html
<div id="app">
    <global-tag :sup_data1='sup_data1' :supData2='sup_data2'></global-tag>
</div>
<script type="text/javascript">
	Vue.component('global-tag', {
		props:['sup_data1', 'supdata2'],
		template: '<div>{{ sup_data1 }} {{ supdata2 }}</div>'
	})
	new Vue({
		el: '#app',
		data: {
			sup_data1: '数据1',
			sup_data2: '数据2'
		}
	})
</script>
```

## 五、子组件传递数据给父组件

- 通过发送事件请求的方式进行数据传递

```html
<div id="app">
    <global-tag @send_action='receiveAction'></global-tag>
</div>
<script type="text/javascript">
	Vue.component('global-tag', {
		data () {
			return {
				sub_data1: "数据1",
				sub_data2: '数据2'
			}
		},
		template: '<div @click="clickAction">发生</div>',
		methods: {
			clickAction () {
				this.$emit('send_action', this.sub_data1, this.sub_data2)
			}
		}
	})
	new Vue({
		el: '#app',
		methods: {
			receiveAction (v1, v2) {
				console.log(v1, v2)
			}
		}
	})
</script>
```

## 六、父子组件实现todoList

```html
<div id="app">
    <div>
        <input type="text" v-model='value'>
        <button @click='click'>提交</button>
    </div>
    <ul>
        <item
              v-for='(e, i) in list'
              :key='i'
              :ele='e'
              :index='i'
              @delete='deleteAction'
              ></item>
    </ul>
</div>
<script type="text/javascript">
	Vue.component('item', {
		props: ['ele', 'index'],
		template: '<li @click="item_click">{{ ele }}</li>',
		methods: {
			item_click: function () {
				this.$emit('delete', this.index)
			}
		}
	})
	new Vue({
		el: '#app',
		data: {
			value: '',
			list: [],
		},
		methods: {
			click: function () {
				this.list.push(this.value)
				this.value = ''
			},
			deleteAction: function (index) {
				this.list.splice(index, 1)
			}
		}
	})
</script>
```

## 七、搭建Vue开发环境

#### 1、安装nodeJS

- 官网下载安装：https://nodejs.org/zh-cn/

#### 2、安装脚手架

- vue[官网](https://cn.vuejs.org/) => 学习 => 教程 => 安装 => 命令行工具(CLI)

```html
安装全局vue：cnpm install -g @vue/cli

在指定目录创建vue项目：vue create my-project

进入项目目录启动项目：npm run serve

通过指定服务器路径访问项目页面：http://localhost:8080/
```

#### 3、项目创建

```html
babel：是一个 JavaScript 编译器。
eslint：是一个语法规则和代码风格的检查工具，可以用来保证写出语法正确、风格统一的代码。
```

#### 4、vue基础模板

```html
<template>
	
</template>
<script>
    export default {
        
    }
</script>
<style scoped>
</style>
```

