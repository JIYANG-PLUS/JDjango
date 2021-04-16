<template>
    <div id="events">
        <h1>组件事件的传递和捕获</h1>
        <div>
            <button @click="sampleClick">简单点击</button>
            <input type="text" v-model="sampleInput">
        </div>
        <div>
            <input type="text" placeholder="这里输入要传递的值" v-model="deliver">
            <button @click="argsClick(deliver, $event)">参数传递值</button>
            <input type="text" v-model="argsInput">
        </div>
        <div>
            <button @click=" expressionValue ++ ">简单表达式点击响应</button>
            <span>{{ expressionValue }}</span>
        </div>
        <div>
            <h2 style="color: orange; ">事件修饰符大全</h2>
            <ul style="color: white;">
                <li>[.stop] 如：v-on:click.stop="" 表示阻止单击事件继续传播。（不会向父组件传播事件）</li>
                <li>[.prevent] 如：v-on:submit.prevent="" 表示提交事件不再重载页面，v-on:submit.prevent可单独用作修饰符。（阻止事件的默认行为）</li>
                <li>[.capture] 如：v-on:click.capture="" 表示父元素捕获子元素的点击事件，父元素先处理，子元素后处理。</li>
                <li>[.self] 如：v-on:click.self="" 表示只有在 event.target 是当前元素自身时触发处理函数，子元素的点击事件不会触发当前元素事件响应。</li>
                <li>[.once] 如：v-on:click.once="" 表示点击事件只会触发一次。</li>
                <li>[.passive] 如：v-on:scroll.passive="" 表示滚动事件的默认行为 (即滚动行为) 将会立即触发。</li>
                <li>[组合使用] 如：v-on:click.stop.prevent=""</li>
                <li>注意：v-on:click.prevent.self 会阻止所有的点击，v-on:click.self.prevent 只会阻止对元素自身的点击。</li>
                <li>注意：[.once] 可加在组件事件上。</li>
                <li>注意：[.passive] 会提升在移动端的性能。</li>
            </ul>
        </div>
    </div>
</template>


<script>
export default {
    name: 'Events',
    data() {
        return {
            sampleInput: '',
            deliver: '',
            argsInput: '',
            expressionValue: 0,
        }
    },
    methods: {
        sampleClick: function() {
            this.sampleInput = '简单点击事件演示'
        },
        argsClick: function(arg1, event) {
            this.argsInput = arg1
            event.preventDefault() // 阻止事件传递
        },
    },
}
</script>


<style>
div#events { border: 6px solid rgb(221, 45, 177); border-radius: 10px; padding: 3px 6px; margin: 6px 0; }
div#events > h1 { text-align: center; border-bottom: 3px solid black; }
div#events > div {
    margin: 6px 12px;
    padding: 6px 12px;
    background: #456789;
}
div#events > div > span {
    color: white;
}
</style>
