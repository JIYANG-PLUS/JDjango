<template>
    <div class="liCtl">
        <ul>
            <liCtl
                v-for="d, index in datas" :key="index"
                :d = "d"
                :index = "index"
                :deleteItem="deleteItem"
            />
        </ul>
    </div>
</template>

<script>
import liCtl from './liCtl'
export default {
    props: {
        datas: Array,
        deleteItem: Function,
    },
    components: {
        liCtl,
    }
}
</script>

<style>
.liCtl {
    padding: 12px;
    margin: 12px;
    border: 1px solid black;
}
</style>
