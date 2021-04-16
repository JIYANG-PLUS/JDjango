<template>
    <div id="sub">
        <h1>组件复用演示</h1>
        <p>事件监听流程：父组件负责编写事件函数和相关变量，并通过@name=name的方式传入子组件；子组件通过@emit()接收响应事件。</p>


        <span>从父组件获取传递过来的列表值：</span>
        <ul>
            <li v-for="data of listData" :key="data.id">{{ data.name }}</li>
        </ul>

        <span>从父组件获取传递过来的字典值：</span>
        <p>标题：{{ dictData.title }}、内容：{{ dictData.content }}、评论：{{ dictData.remark }}、阅览数：{{ dictData.views }}</p>

        <span>子组件向父组件传递事件，并又父组件执行其add函数：</span><br>
        <button @click="$emit('add')">加1</button><span>{{ value }}</span>

        <slot></slot>
    </div>
</template>


<script>
export default {
    name: 'Sub',
    data() {
        return {
            
        }
    },
    props: [
        'listData',
        'dictData',
        'value',
    ]
}
</script>


<style>
div#sub { border: 6px solid rgb(214, 108, 21); border-radius: 10px; padding: 3px 6px; margin: 6px 0; }
div#sub > h1 { text-align: center; border-bottom: 3px solid black; }
</style>