<template>
    <div>
        <!-- 第一种传值方式 -->
        <!-- 传值，可加引号可不加引号，效果一样 -->
        <Sub 
            :listData = "listData"
            :dictData = dictData
            @add = add
            :value = value
        >
        <p>【【我是父组件插进来的内容】】</p>
        </Sub>

        <!-- 第二种传值方式 -->
        <component 
            :is="component_name"
            :listData = "listData"
            :dictData = dictData
            @add = add
            :value = value
        ></component>
    </div>
    
</template>


<script>
import Sub from './Sub.vue'
export default {
    name: 'UseSub',
    components: {
        Sub,
    },
    data() {
        return {
            listData: [
                {id: 1, name: '父级传值1'},
                {id: 2, name: '父级传值2'}
            ],
            dictData: {
                title: 'just ok',
                content: 'jhjhjyuxczvhjwfeysahdashfsasvfhjsfhsdfuys',
                remark: 'uyzxcsjh',
                views: 0,
            },
            value: 0,
            component_name: 'Sub',
        }
    },
    methods: {
        add: function() {
            this.value += 1
        }
    },
}
</script>


<style>
    
</style>