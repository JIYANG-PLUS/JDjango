<template>
    <div class="inputCtl">
        <div>
            <input type="text"><button>添加</button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        datas: Array
    }
}
</script>

<style>
.inputCtl {
    padding: 12px;
    margin: 12px;
    border: 1px solid black;
}
</style>
