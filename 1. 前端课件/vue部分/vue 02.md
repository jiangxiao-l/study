# Vue

## 八、重要指令

- v-bind

```html
<!-- 值a -->
<div v-bind:class='"a"'></div>

<!-- 变量a -->
<div v-bind:class='a'></div>

<!-- 变量a, b -->
<div v-bind:class='[a, b]'></div>

<!-- a为class值，isA决定a是否存在(ture | false) -->
<div v-bind:class='{a: isA}'></div>

<!-- 多class值，是否存在 -->
<div v-bind:class='{a: isA, b: isB}'></div>

<!-- 多style值，my_color为变量，cyan为普通值 -->
<div :style='{color:my_color, background:"cyan"}'></div>
```

- v-on

```html
<!-- 绑定函数fn1，并将事件event传递过去 -->
<div v-on:click='fn1'></div>

<!-- 绑定函数fn2，并将自定义参数10传递过去 -->
<div v-on:click='fn2(10)'></div>

<!-- 绑定函数fn3，并将事件event与自定义参数10传递过去 -->
<div v-on:click='fn2($event, 10)'></div>
```

- v-model

```html
<!-- 文本输入框：数据的双向绑定 -->
<input type="text" v-model='val' />
<textarea v-model='val'></textarea>

<!-- 单个复选框：选中与否val默认值为true|false -->
<input type="checkbox" v-model='val' />
<!-- 通过true-value|false-value修改默认值为true|false -->
<input type="checkbox" v-model='val' true-value="选中" false-value="未选中" />

<!-- 多个复选框：val作为数组[]来使用，可以存储选中元素的value值，反之数组有对应value代表该选框选中 -->
<input type="checkbox" value="男" v-model='val' />
<input type="checkbox" value="女" v-model='val' />

<!-- 单选框：val存储选中的单选框的value值 -->
<input type="radio" value="男" v-model='val' />
<input type="radio" value="女" v-model='val' />
```

## 九、案例

- v-show

```html
<style type="text/css">
    .btn_wrap {
        width: 660px;
        margin: 0 auto;
    }
    .btn_wrap:after {
        content: '';
        display: block;
        clear: both;
    }
    .btn {
        width: 200px;
        height: 40px;
        border-radius: 5px;
        float: left;
        margin: 0 10px 0;
    }
    .box {
        width: 660px;
        height: 300px;
    }
    .b1 {background-color: red}
    .b2 {background-color: orange}
    .b3 {background-color: cyan}

    .box_wrap {
        width: 660px;
        margin: 10px auto;
    }
</style>

<div id="app">
    <div class="btn_wrap">
        <div class="btn b1" @click='setTag(0)'></div>
        <div class="btn b2" @click='setTag(1)'></div>
        <div class="btn b3" @click='setTag(2)'></div>
    </div>
    <div class="box_wrap">
        <div class="box b1" v-show='isShow(0)'></div>
        <div class="box b2" v-show='isShow(1)'></div>
        <div class="box b3" v-show='isShow(2)'></div>
    </div>
</div>


<script type="text/javascript">
	new Vue({
		el: '#app',
		data: {
			tag: 0
		},
		methods: {
			isShow (index) {
				return this.tag === index;
			},
			setTag (index) {
				this.tag = index;
			}
		}
	})
</script>
```

- v-for

```html
<div id="app">
    <div>
        <input type="text" v-model="inValue">
        <button @click='pushAction'>提交</button>
    </div>
    <ul>
        <li @click='deleteAction(index)' v-for="(item, index) in list" :key="index">{{ item }}</li>
    </ul>
</div>


<script type="text/javascript">
	new Vue({
		el: '#app',
		data: {
			inValue: '',
			list: []
		},
		methods: {
			pushAction: function () {
				this.list.push(this.inValue);
				this.inValue = ''
			},
			deleteAction: function (index) {
				this.list.splice(index, 1);
			}
		}
	})
</script>
```

