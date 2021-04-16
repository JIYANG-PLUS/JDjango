<template>
    <div id="list">
        <h1>列表渲染及列表相关操作功能演示</h1>
        <ul>
            <li v-for="person, index in persons" :key="person.id">
                数组内索引：{{ index }}、内码：{{ person.id }}、名字：{{ person.name }}、年龄：{{ person.age }}
            </li>
        </ul>
        
        <div class="ops">
            <button @click="usePush">push（尾插元素）</button>
            <button @click="usePop">pop（尾删元素）</button>
            <button @click="useShift">shift（首删元素）</button>
            <button @click="useUnshift">unshift（首插元素）</button>
            <button @click="useSplice">splice（删除并插入）</button>
            <button @click="useSort">sort（排序）</button>
            <button @click="useReverse">reverse（倒序）</button>
        </div>
    </div>
</template>


<script>
export default {
    name: "List", // 组件名称
    props: ["todos"], // 属性传值
    data() {
        return {
            persons: [
                { id: 1,  name: 'A', age: 18 },
                { id: 2, name: 'B', age: 16 }
            ],
            id: 3
        }
    }, // 界面渲染数据集
    methods: {
        usePush: function() {
            var objs = this.persons.push({id: this.id++, name: 'new', age: this.id})
            console.log(objs) // 当前的数据集总行数
        },
        usePop: function() {
            var objs = this.persons.pop()
            console.log(objs) // 弹出对象
        },
        useShift: function() {
            var objs = this.persons.shift()
            console.log(objs) // 弹出对象
        },
        useUnshift: function() {
            var objs = this.persons.unshift({id: this.id++, name: 'new', age: this.id})
            console.log(objs) // 当前的数据集总行数
        },
        useSplice: function() {
            var objs = this.persons.splice(1, 0, {id: this.id++, name: 'new', age: this.id}) // 在索引为1处插入新元素
            console.log(objs) // 返回删除的行数，第二个参数0表示不删除，第三个参数可选
        },
        useSort: function() {
            var objs = this.persons.sort((x,y)=>x.age>y.age) // 改变自身
            console.log(objs)
        },
        useReverse: function() {
            var objs = this.persons.reverse() // 改变自身
            console.log(objs)
        }
    }, // 关于列表的一系列封装操作
}
</script>


<style>
div#list {
    border: 6px solid orange;
    border-radius: 10px;
    padding: 3px 6px;
    margin: 6px 0;
}
div#list > h1 {
    text-align: center;
    border-bottom: 3px solid black;
}
div#list > ul {
    background: rgb(10, 98, 150);
    list-style-position: inside;
    padding: 6px 8px;
    margin-bottom: 16px;
    color: white;
}
div.ops {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}
div.ops > button {
    margin: 6px;
    font-size: 18px;
}
</style>
