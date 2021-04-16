<template>
    <div>
        <input type="checkbox" id="checkAll" v-model="checked"/><label for="checkAll">全部</label><button>删除</button>
    </div>
</template>

<script>
export default {
    props: {
        checked: Boolean
    }
}
</script>

<style>

</style>
