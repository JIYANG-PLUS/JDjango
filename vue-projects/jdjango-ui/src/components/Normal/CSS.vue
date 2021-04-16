<template>
    <div id="css">
        <h1>CSS样式控制</h1>
        <div>
            <span :class="{red: isRed}">（对象语法--直接传递字典）对象测试文本</span>
            <span :class="isRedObj">（对象语法--传递对象）对象测试文本</span>
            <button @click="changeObj">{{ btn_name }}</button>
            <!-- 下面演示 计算属性 和 侦听器 的使用 -->
            <input v-model="btn_name">
            <input v-model="reverseName">
        </div>
        <div>
            <!-- 数组内可接受三目运算符，即任何表达式 -->
            <!-- 可以在 数组语法 中嵌入 对象语法 -->
            <!-- 组件上使用 CSS样式控制 会自动添加到组件的父级元素上 -->
            <span :class="[varBlue, {blod: isBlod}]">（数组语法--传递变量）数组测试文本</span>
            <button @click="changeBlod">{{ btn_blod_name }}</button>
        </div>
        <div>
            <!-- 驼峰命名法的规则来源于 JS 的原生 DOM 语法 -->
            <!-- 键值对形式的值可以是一个【表达式】 -->
            <!-- 可传入数组传递多个对象 -->
            <span :style="{color: green, fontWeight: blod}">（内联样式语法--使用原生 JS 的 CSS dom语法）</span>
            <span :style="styleObj">（内联样式语法--直接传递对象管理）</span>
        </div>
    </div>
</template>


<script>
export default {
    name: "CSS",
    data() {
        return {
            btn_name: 'black',
            btn_blod_name: 'not blod',
            isRed: false,
            isRedObj: {
                red: false
            }, // 推荐对象的方式设置 CSS 样式
            varBlue: 'blue',
            isBlod: false,
            green: 'green',
            blod: 700,
            styleObj: {
                color: 'orange',
                fontWeight: 700,
            }
        }
    },
    methods: {
        changeObj: function() {
            this.btn_name = 'black' === this.btn_name ? 'red' : 'black'
            this.isRed = !this.isRed
            this.isRedObj.red = !this.isRedObj.red // 为方便管理，正常使用这种方式控制样式的显示和隐藏
        },
        changeBlod: function() {
            this.btn_blod_name = 'not blod' === this.btn_blod_name ? 'blod' : 'not blod'
            this.isBlod = !this.isBlod
        }
    },
    computed: {
        reverseName: function() {
            return this.btn_name.split('').reverse().join('')
        }
    }, // 计算属性仅在监听值变化时才会计算，减少内存占用
}
</script>


<style>
div#css { border: 6px solid olivedrab; border-radius: 10px; padding: 3px 6px; margin: 6px 0; }
div#css > div { margin-bottom: 6px; border-bottom: 2px solid orangered; padding-bottom: 6px; }
div#css > h1 { text-align: center; border-bottom: 3px solid black; }
button { margin: 3px 6px; }
span { border: 1px dotted blue; margin: 0 6px; padding: 3px 6px; }
.red { color: red; }
.blue { color: blue; }
.blod { font-weight: 700; }
</style>
