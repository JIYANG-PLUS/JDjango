<template>
    <li>
        <input type="checkbox" v-model="d.checked"/> {{ d.name }}
        <button @click="deleteItem(index)">删除</button>
    </li>
</template>

<script>
export default {
    props: {
        d: Object,
        index: Number,
        deleteItem: Function,
    }
}
</script>

<style>

</style>
